#!/usr/bin/env python
import sys
import logging
import time
import simpleaudio
from beepy import beep
from tqdm import tqdm
from colorama import Fore
from sylo.messages import (
    print_message,
    print_update,
    print_header_small,
)
from sylo.models import Durations, DataPersistence
from sylo.definitions import (
    WELCOME_CHOICES,
    COUNTDOWN_INCREMENTS,
    DATA_FILE_LOCATION,
    METRICS_BAR,
    METRICS_HEAT,
    DATA_FILE_CREATE,
    HOME_DIR_CREATE,
    ONE_WEEK_AGO,
    ONE_YEAR_AGO,
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

is_double = False
timer_mode = 'work'
data_file = DataPersistence()
cursor = print_message('cursor')
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
            leave=True,
            desc=print_message(f'{self.mode}_start', self.mins),
            unit=" seconds",
            bar_format="{l_bar}%s{bar}%s{r_bar}" % (self.bar_color, Fore.RESET),
            smoothing=True,
            ncols=70
        )
        try:
            while self.secs > 0:
                time.sleep(1)
                self.secs -= self.increments
                timer_iterator.update(self.increments)
                if self.secs % 60 == 0:
                    self.mins_passed += 1
                    logger.debug(f'{self.mode} Timer loop: secs remaining: {self.secs}')
        except KeyboardInterrupt:
            print('\nQuitting early..')
            logger.info(f'Ctrl-C quit with {self.secs} remaining')
            return False, self.mins_passed
            pass
        logger.info(f'{self.mode} timer loop finished')
        timer_iterator.close()
        return True, self.mins_passed

    def start_countdown(self):
        logger.info(f'{self.mode} timer started')
        complete, mins_passed = self._start_timer()
        return complete, mins_passed


class Sound:

    def __init__(self, audio_path: str = 'dummy'):
        self.sound_file = audio_path
        self.beep_needed = False
        self.initialised_file = None

    def initialise(self):
        logger.info(f'Initialising audio: {self.sound_file}')
        try:
            self.initialised_file = simpleaudio.WaveObject.from_wave_file(
                self.sound_file
            )
            logger.info(f'Custom audio successfully initialised: {self.sound_file}')
        except FileNotFoundError:
            logger.info(f'Custom audio not found: {self.sound_file}')
            self.beep_needed = True

    def play_sound(self):
        if self.beep_needed is False:
            play_obj = self.initialised_file.play()
            logger.info('Played audio file')
            play_obj.wait_done()
            logger.info('Waiting audio file')

        else:
            logger.info('Playing beep')
            beep("ready")


class Insights:

    def __init__(self):
        self.data_file = DATA_FILE_LOCATION
        self.heatmap_start_date = ONE_YEAR_AGO
        self.bar_start_date = ONE_WEEK_AGO

    def print_bar(self):
        global initial_boot_flag
        if initial_boot_flag is False:
            logger.info(f'Running ${self._bar_chart()}')
            print_message('bar_header')
            run_subprocess(self._bar_chart())
        else:
            print_message('bar_header')
            print('No data available, complete some segments and check later.')

    def print_heat(self):
        logger.info(f'Running ${self._heat_map()}')
        print_message('heat_header')
        run_subprocess(self._heat_map())

    def _bar_chart(self):
        return METRICS_BAR % (self.data_file, self.bar_start_date)

    def _heat_map(self):
        return METRICS_HEAT % (self.heatmap_start_date, self.data_file)


def sylo(
        durations_model: Durations,
        sound_obj: any,
        mode: str,
        show_options: bool,
        double: bool = is_double,
):
    global initial_boot_flag
    clear_screen()
    if double is True:
        increments = 30
    else:
        increments = COUNTDOWN_INCREMENTS
    logger.debug(f'Running in {increments} second increments')

    timer = Timer(mode, durations_model, increments)
    print_header_small(double=double)

    print_update(timer.durations, mode, show_options)

    response = get_input(cursor)
    logger.info(f'User response: {response}')

    while response.lower() not in WELCOME_CHOICES:
        show_options = True
        logger.info(f'Rejected user response of {response}')
        sylo(
            durations_model=durations_model,
            sound_obj=sound_obj,
            mode=mode,
            show_options=show_options,
            double=double,
        )
    while response.lower() == "q":
        logger.info('Quit requested')
        clear_screen()
        sys.exit()
    while response.lower() == "i":
        clear_screen()
        metrics = Insights()
        metrics.print_bar()
        metrics.print_heat()
        print_message('show_insights')
        input(cursor)
        sylo(
            durations_model=durations_model,
            sound_obj=sound_obj,
            mode=mode,
            show_options=show_options,
            double=double,
        )
    while response.lower() == "s":
        logger.info('Switch requested')
        new_mode = flip_mode(mode)
        sylo(
            durations_model=durations_model,
            sound_obj=sound_obj,
            mode=new_mode,
            show_options=show_options,
            double=double,
        )
    while response.lower() == "h":
        logger.info('Help requested')
        show_options = True
        sylo(durations_model=durations_model,
             sound_obj=sound_obj,
             mode=mode,
             show_options=show_options,
             double=double,
             )
    clear_screen()
    while response == "":
        logger.info('User pressed ENTER')
        if mode == 'rest':
            complete, secs_passed = timer.start_countdown()
            if complete is True:
                sound_obj.play_sound()
                durations_model.total_rest_mins += secs_passed
            else:
                durations_model.total_rest_mins += secs_passed
            next_mode = flip_mode(mode)
            data_file.data_refresh(durations_model)
            clear_screen()
        else:
            complete, secs_passed = timer.start_countdown()
            if complete is True:
                sound_obj.play_sound()
                durations_model.total_work_mins += durations_model.work.mins
            else:
                durations_model.total_work_mins += secs_passed
            next_mode = flip_mode(mode)
            data_file.data_refresh(durations_model)
            clear_screen()
        logger.info('Durations model set')
        logger.info(f'Work time: {durations_model.total_work_mins}')
        logger.info(f'Work time: {durations_model.total_rest_mins}')
        initial_boot_flag = False
        sylo(
            durations_model=durations_model,
            sound_obj=sound_obj,
            mode=next_mode,
            show_options=False,
            double=double,
        )


def initial_boot():
    global initial_boot_flag
    initial_boot_flag = True
    logger.info('First boot')
    logger.info(f'No data file found, creating at {DATA_FILE_LOCATION}')
    run_subprocess(HOME_DIR_CREATE)
    run_subprocess(DATA_FILE_CREATE)


def run(args):
    global is_double, timer_mode
    print('THIS IS MY NEW VERSION')
    if check_for_file(DATA_FILE_LOCATION) is False:
        initial_boot()
    clear_screen()

    durations_data = Durations()
    data_file.data_load_on_boot(durations_data)

    if args.work_time:
        durations_data.work.mins = args.work_time
        durations_data.work.secs = mins_to_secs(args.work_time)
    if args.rest_time:
        durations_data.rest.mins = args.rest_time
        durations_data.rest.secs = mins_to_secs(args.rest_time)

    logger.info('Durations model set')
    logger.info(f'Work time: {durations_data.work.mins}')
    logger.info(f'Work time: {durations_data.work.secs}')
    logger.info(f'Work time: {durations_data.rest.mins}')
    logger.info(f'Work time: {durations_data.rest.secs}')

    if args.double_speed is True:
        is_double = True
    logger.info(f'Double speed set to {is_double}')

    if args.audio_file:
        sound = Sound(audio_path=args.audio_file)
        logger.debug(f'Custom audio file path specified {sound}')
    else:
        sound = Sound()
        logger.debug('Using default audio')
    sound.initialise()
    logger.debug('Sound initialised')

    sylo(
        durations_model=durations_data,
        sound_obj=sound,
        mode=timer_mode,
        show_options=False,
        double=is_double,
    )
