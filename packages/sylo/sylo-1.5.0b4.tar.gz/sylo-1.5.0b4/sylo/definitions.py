import os
import datetime
from pathlib import Path
from colorama import Fore, Style
import sys
import logging
from pyfiglet import figlet_format, FigletFont
from random import sample
from typing import List

logger = logging.getLogger(__name__)

HOME_DIR = home = str(Path.home())
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

TODAY = datetime.datetime.now().date()
YESTERDAY = (datetime.datetime.now() - datetime.timedelta(days=1)).date()

TODAY_STR = TODAY.strftime("%Y-%m-%d")
YESTERDAY_STR = YESTERDAY.strftime("%Y-%m-%d")

ONE_WEEK_AGO = (datetime.datetime.now() - datetime.timedelta(days=7)).date()
ONE_YEAR_AGO = (datetime.datetime.now() - datetime.timedelta(days=364)).date()

DATA_FILE_LOCATION = f"{HOME_DIR}/.sylo/sessions.dat"
TASK_FILE_LOCATION = f"{HOME_DIR}/.sylo/tasks.dat"

HOME_DIR_CREATE = f"mkdir {HOME_DIR}/.sylo"
DATA_FILE_CREATE = f'echo "{TODAY_STR},0,0" > {HOME_DIR}/.sylo/sessions.dat'
TASK_FILE_CREATE = f'touch {HOME_DIR}/.sylo/tasks.dat'


WELCOME_CHOICES = ("", "q", "s", "i", "t", "n", "y", "a")

TIMER_DEFAULTS = {
    "work": {
        "mins": 25,
        "secs": 1500,
    },
    "rest": {
        "mins": 5,
        "secs": 300,
    },
}

COUNTDOWN_INCREMENTS = 1

METRICS_HEAT = 'termgraph --calendar --start-dt "%s" %s '

METRICS_BAR = 'termgraph %s --color {red,green} --start-dt "%s"'

RANDOM_FONTS = False

THEME = Fore.BLUE


def set_theme(color: str = "blue"):
    global THEME
    colors = {
        "red": Fore.RED,
        "lred": Fore.LIGHTRED_EX,
        "blue": Fore.BLUE,
        "lblue": Fore.LIGHTBLUE_EX,
        "green": Fore.GREEN,
        "lgreen": Fore.LIGHTGREEN_EX,
        "yellow": Fore.YELLOW,
        "magenta": Fore.MAGENTA,
        "white": Fore.WHITE,
        "black": Fore.BLACK,
    }
    logger.info("The theme is" + THEME)
    THEME = colors[color]


def print_message(message: str, timer_val: int = None, text: str = None):
    logger.debug(f"Printing message: {message} with a timer_val of {timer_val}")
    if message == "work_start":
        print(
            f"""{THEME}Ctrl-C to stop timer early{Style.RESET_ALL}
{Fore.RED}WORK{Style.RESET_ALL} for {Fore.YELLOW}{timer_val}{Style.RESET_ALL} minutes"""
        )
    elif message == "rest_start":
        print(
            f"""{THEME}Ctrl-C to stop timer early{Style.RESET_ALL}
{Fore.GREEN}REST{Style.RESET_ALL} for {Fore.YELLOW}{timer_val}{Style.RESET_ALL} minutes"""
        )
    elif message == "summary_and_quit":
        sys.stdout.write("\033[K")
        print(
            f"{THEME}Press {Fore.YELLOW}ENTER{Style.RESET_ALL}{THEME} to stop timer.{Style.RESET_ALL}",
        )
    elif message == "show_insights":
        print(f"\n{THEME}Press {Fore.YELLOW}ENTER{Style.RESET_ALL}{THEME} to return to main menu{Style.RESET_ALL}")
    elif message == "bar_header":
        print(f"{Fore.YELLOW}Weekly minutes{Style.RESET_ALL}")
    elif message == "heat_header":
        print(f"{Fore.YELLOW}Work heatmap{Style.RESET_ALL}")
    elif message == "task":
        print(f"{text}")
    elif message == "cursor":
        return ">> "


def options():
    return f"""Additional commands;
{Fore.YELLOW}S{Style.RESET_ALL}{THEME}       --    Swap upcoming timer{Style.RESET_ALL}
{Fore.YELLOW}N{Style.RESET_ALL}{THEME}       --    Add a new task for today{Style.RESET_ALL}
{Fore.YELLOW}T{Style.RESET_ALL}{THEME}       --    Toggle display of today's tasks{Style.RESET_ALL}
{Fore.YELLOW}Y{Style.RESET_ALL} {THEME}      --    Toggle display of yesterday's tasks{Style.RESET_ALL}
{Fore.YELLOW}I{Style.RESET_ALL} {THEME}      --    Insights tab{Style.RESET_ALL}
{Fore.YELLOW}Q{Style.RESET_ALL}  {THEME}     --    Quit SYLO{Style.RESET_ALL}
"""


def print_update(
    durations, mode: str, show_options: bool = False, show_tasks: bool = False, tasks: List = None
):
    logger.debug(f"Printing update: {mode} with show_options {show_options}")
    if mode == "rest":
        upcoming_timer_color = durations.rest.bar_color
    else:
        upcoming_timer_color = durations.work.bar_color

    if show_options:
        print_ops = options()
    else:
        print_ops = ".. or chose an optional command (H for help)"

    if show_tasks:
        if tasks:
            print_task_welcome = f'{THEME}My Tasks{Style.RESET_ALL}'
            print_task = '\n'.join(''.join(map(str, t)) for t in tasks)
        else:
            print_task = '\r'
            print_task_welcome = '\r'
    else:
        print_task = '\r'
        print_task_welcome = '\r'

    print(
        f"""Total {Fore.RED}work{Style.RESET_ALL} today:           {Fore.YELLOW}{int(durations.total_work_mins)} minutes{Style.RESET_ALL}
Total {Fore.GREEN}rest{Style.RESET_ALL} today:           {Fore.YELLOW}{int(durations.total_rest_mins)} minutes{Style.RESET_ALL}

Upcoming timer:     {upcoming_timer_color}{mode.upper()}{Style.RESET_ALL}

{print_task_welcome}

{print_task}

{THEME}Press {Style.RESET_ALL}{Fore.YELLOW}ENTER {Style.RESET_ALL}{THEME}to start the next timer{Style.RESET_ALL}

{THEME}{print_ops}{Style.RESET_ALL}
    """)


def ascii_header(font: str):
    return figlet_format("Sort Your Life Out", font=font, width=40)


def print_header_small(double: bool):
    if RANDOM_FONTS is True:
        font = random_ascii_header()
    else:
        font = ascii_header_small(font="alligator")
    if double is True:
        double_message = ">>>>>>>>>>>> DOUBLE SPEED MODE >>>>>>>>>>>>"
    else:
        double_message = ""
    print(f"{double_message}")
    print(f"""{THEME}{font}{Style.RESET_ALL}""")


def ascii_header_small(font: str):
    return figlet_format("SYLO", font=font, width=60)


def random_ascii_header():
    fonts = FigletFont.getFonts()
    random_fonts = sample(fonts, int(len(fonts) / 2))
    for f in random_fonts:
        try:
            logger.debug(f"Output of shuffled fonts: {f}")
            return figlet_format("SYLO", font=f, width=40)
        except Exception as e:
            logger.debug(f"Output of shuffled fonts: {f} {e}")
            pass
