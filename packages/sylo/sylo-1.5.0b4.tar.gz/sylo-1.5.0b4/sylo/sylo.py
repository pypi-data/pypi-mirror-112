#!/usr/bin/env python
import sys
import logging
import time
import simpleaudio
from beepy import beep
from tqdm import tqdm
from colorama import Fore
from typing import List
import csv
from sylo.models import Durations, DataPersistence
from sylo.definitions import (
    TASK_FILE_LOCATION,
    TODAY_STR,
    YESTERDAY_STR,
    WELCOME_CHOICES,
    COUNTDOWN_INCREMENTS,
    DATA_FILE_LOCATION,
    METRICS_BAR,
    METRICS_HEAT,
    DATA_FILE_CREATE,
    TASK_FILE_CREATE,
    HOME_DIR_CREATE,
    ONE_WEEK_AGO,
    ONE_YEAR_AGO,
    print_message,
    print_update,
    print_header_small,
)
from sylo.utils import (
    clear_screen,
    mins_to_secs,
    flip_mode,
    get_input,
    run_subprocess,
    check_for_file,
)

logger = logging.getLogger(__name__)

is_speed_mode = False
timer_mode = "work"
data_file = DataPersistence()
cursor = print_message("cursor")
initial_boot_flag = False


class Timer:
    def __init__(self, mode: str, durations: Durations, increments: int):
        self.durations = durations
        self.mode: str = mode
        self.increments = increments
        self.mins_passed = 0

        if self.mode == "work":
            self.mins = self.durations.work.mins
            self.secs = self.durations.work.secs
            self.bar_color = self.durations.work.bar_color
        else:
            self.mins = self.durations.rest.mins
            self.secs = self.durations.rest.secs
            self.bar_color = self.durations.rest.bar_color

    def _start_timer(self):
        timer_iterator = tqdm(
            total=self.secs,
            position=0,
            leave=False,
            desc=print_message(f"{self.mode}_start", self.mins),
            unit=" seconds",
            bar_format="{l_bar}%s{bar}%s{r_bar}" % (self.bar_color, Fore.RESET),
            smoothing=True,
            ncols=70,
        )
        try:
            while self.secs > 0:
                time.sleep(1)
                self.secs -= self.increments
                timer_iterator.update(self.increments)
                if self.secs % 60 == 0:
                    self.mins_passed += 1
                    logger.debug(f"{self.mode} Timer loop: secs remaining: {self.secs}")
        except KeyboardInterrupt:
            print("\nQuitting early..")
            logger.info(f"Ctrl-C quit with {self.secs} remaining")
            timer_iterator.close()
            return False, self.mins_passed
            pass
        logger.info(f"{self.mode} timer loop finished")
        timer_iterator.close()
        return True, self.mins_passed

    def start_countdown(self):
        logger.info(f"{self.mode} timer started")
        complete, mins_passed = self._start_timer()
        return complete, mins_passed


class Sound:
    def __init__(self, audio_path: str = "dummy"):
        self.sound_file = audio_path
        self.beep_needed = False
        self.initialised_file = None

    def initialise(self):
        logger.info(f"Initialising audio: {self.sound_file}")
        try:
            self.initialised_file = simpleaudio.WaveObject.from_wave_file(
                self.sound_file
            )
            logger.info(f"Custom audio successfully initialised: {self.sound_file}")
        except FileNotFoundError:
            logger.info(f"Custom audio not found: {self.sound_file}")
            self.beep_needed = True

    def play_sound(self):
        if self.beep_needed is False:
            play_obj = self.initialised_file.play()
            logger.info("Played audio file")
            play_obj.wait_done()
            logger.info("Waiting audio file")

        else:
            logger.info("Playing beep")
            beep("ready")


class Insights:
    def __init__(self):
        self.data_file = DATA_FILE_LOCATION
        self.heatmap_start_date = ONE_YEAR_AGO
        self.bar_start_date = ONE_WEEK_AGO

    def print_bar(self):
        global initial_boot_flag
        if initial_boot_flag is False:
            logger.info(f"Running ${self._bar_chart()}")
            print_message("bar_header")
            run_subprocess(self._bar_chart())
        else:
            print_message("bar_header")
            print("No data available, complete some segments and check later.")

    def print_heat(self):
        logger.info(f"Running ${self._heat_map()}")
        print_message("heat_header")
        run_subprocess(self._heat_map())

    def _bar_chart(self):
        return METRICS_BAR % (self.data_file, self.bar_start_date)

    def _heat_map(self):
        return METRICS_HEAT % (self.heatmap_start_date, self.data_file)


class Task:

    def __init__(self):
        self.description = None
        self.date = TODAY_STR
        self.complete = False

    def write_task_to_file(self):
        fields = [
            self.date,
            self.description,
            self.complete
        ]
        with open(TASK_FILE_LOCATION, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(fields)


def get_tasks(date: str = None):
    with open(TASK_FILE_LOCATION, 'r') as read_obj:
        csv_reader = csv.reader(read_obj)
        if date:
            return [row[1] for row in csv_reader if row[0] == date]
        else:
            return [row[1] for row in csv_reader]


def print_tasks(date: str = None):
    tasks = get_tasks(date)
    for t in tasks:
        print_message('task', text=t)


class Sylo:
    def __init__(
        self,
        durations: Durations,
        sound_obj: any,
        mode: str,
        show_options: bool,
        show_tasks: bool = False,
        tasks: List = None,
        speed_mode: bool = is_speed_mode,
    ):
        self.durations = durations
        self.sound_obj = sound_obj
        self.mode = mode
        self.show_options = show_options
        self.show_tasks = show_tasks
        self.tasks = tasks
        self.speed_mode = speed_mode
        self.increments = 1

    def on_boot(self):
        clear_screen()
        if self.speed_mode is True:
            self.increments = 30
        else:
            self.increments = COUNTDOWN_INCREMENTS
        logger.debug(f"Running in {self.increments} second increments")

    def splash(self, timer: Timer):
        print_header_small(double=self.speed_mode)
        print_update(
            timer.durations,
            mode=self.mode,
            show_options=self.show_options,
            show_tasks=self.show_tasks,
            tasks=self.tasks
        )


def virgin_boostrap():
    global initial_boot_flag
    initial_boot_flag = True
    logger.info("First boot")
    logger.info(f"No data file found, creating at {DATA_FILE_LOCATION}")
    run_subprocess(HOME_DIR_CREATE)
    run_subprocess(DATA_FILE_CREATE)
    run_subprocess(TASK_FILE_CREATE)


def task_menu(sylo, date: str = None):
    sylo.show_tasks ^= True
    logger.info("Show tasks requested")
    sylo.tasks = get_tasks(date)
    input_loop(sylo)


def new_task_menu(sylo):
    clear_screen()
    task = Task()
    task.description = input('Description of task > ')
    task.write_task_to_file()
    another_yn = input('Input another y/n? >')
    if another_yn == 'y':
        new_task_menu(sylo)
    else:
        input_loop(sylo)


def switch_modes(sylo):
    logger.info("Switch requested")
    sylo.mode = flip_mode(sylo.mode)
    input_loop(sylo)


def show_help_menu(sylo):
    logger.info("Help requested")
    sylo.show_options = True
    input_loop(sylo)


def show_insights_menu(sylo):
    clear_screen()
    metrics = Insights()
    metrics.print_bar()
    metrics.print_heat()
    print_message("show_insights")
    input(cursor)
    input_loop(sylo)


def timer_loop(sylo: Sylo, timer: Timer):
    clear_screen()
    global initial_boot_flag
    logger.info("User pressed ENTER")
    if sylo.mode == "rest":
        complete, secs_passed = timer.start_countdown()
        if complete is True:
            sylo.sound_obj.play_sound()
            sylo.durations.total_rest_mins += secs_passed
        else:
            sylo.durations.total_rest_mins += secs_passed
        sylo.mode = flip_mode(sylo.mode)
        data_file.data_refresh(sylo.durations)
        clear_screen()
    else:
        complete, secs_passed = timer.start_countdown()
        if complete is True:
            sylo.sound_obj.play_sound()
            sylo.durations.total_work_mins += sylo.durations.work.mins
        else:
            sylo.durations.total_work_mins += secs_passed
        sylo.mode = flip_mode(sylo.mode)
        data_file.data_refresh(sylo.durations)
        clear_screen()
    logger.info("Durations model set")
    logger.info(f"Work time: {sylo.durations.total_work_mins}")
    logger.info(f"Work time: {sylo.durations.total_rest_mins}")
    initial_boot_flag = False
    input_loop(sylo)


def quit_app():
    logger.info("Quit requested")
    clear_screen()
    sys.exit()


def input_loop(sylo: Sylo):
    sylo.on_boot()
    timer = Timer(sylo.mode, sylo.durations, sylo.increments)
    sylo.splash(timer)
    response = get_input(cursor)
    logger.info(f"User response: {response}")
    while response.lower() not in WELCOME_CHOICES:
        sylo.show_options = True
        logger.info(f"Rejected user response of {response}")
        input_loop(sylo)
    while response.lower() == "q":
        quit_app()
    while response.lower() == "i":
        show_insights_menu(sylo)
    while response.lower() == "s":
        switch_modes(sylo)
    while response.lower() == "h":
        show_help_menu(sylo)
    while response.lower() == 't':
        task_menu(sylo, TODAY_STR)
    while response.lower() == 'y':
        task_menu(sylo, YESTERDAY_STR)
    while response.lower() == 'a':
        task_menu(sylo)
    while response.lower() == 'n':
        new_task_menu(sylo)
    while response == "":
        timer_loop(sylo, timer)


def run(args):
    global is_speed_mode, timer_mode
    print("THIS IS MY NEW VERSION")
    if check_for_file(DATA_FILE_LOCATION) is False:
        virgin_boostrap()
    clear_screen()

    durations_data = Durations()
    data_file.data_load_on_boot(durations_data)

    if args.work_time:
        durations_data.work.mins = args.work_time
        durations_data.work.secs = mins_to_secs(args.work_time)
    if args.rest_time:
        durations_data.rest.mins = args.rest_time
        durations_data.rest.secs = mins_to_secs(args.rest_time)

    logger.info("Durations model set")
    logger.info(f"Work time: {durations_data.work.mins}")
    logger.info(f"Work time: {durations_data.work.secs}")
    logger.info(f"Work time: {durations_data.rest.mins}")
    logger.info(f"Work time: {durations_data.rest.secs}")

    if args.speed_mode is True:
        is_speed_mode = True
    logger.info(f"Speed mode set to {is_speed_mode}")

    if args.audio_file:
        sound = Sound(audio_path=args.audio_file)
        logger.debug(f"Custom audio file path specified {sound}")
    else:
        sound = Sound()
        logger.debug("Using default audio")
    sound.initialise()
    logger.debug("Sound initialised")
    sylo = Sylo(
        durations=durations_data,
        sound_obj=sound,
        mode=timer_mode,
        show_options=False,
        speed_mode=is_speed_mode,
    )
    input_loop(sylo)
