from colorama import Fore, Style
import sys
import logging
from sylo.models import Durations
from sylo.definitions import RANDOM_FONTS
from pyfiglet import figlet_format, FigletFont
from random import sample
logger = logging.getLogger(__name__)


def print_message(message: str, timer_val: int = None):
    logger.debug(f'Printing message: {message} with a timer_val of {timer_val}')
    if message == "work_start":
        print(f"""{Fore.BLUE}Ctrl-C to stop timer early{Style.RESET_ALL}
{Fore.RED}WORK{Style.RESET_ALL} for {Fore.YELLOW}{timer_val}{Style.RESET_ALL} minutes""")
    elif message == "rest_start":
        print(f"""{Fore.BLUE}Ctrl-C to stop timer early{Style.RESET_ALL}
{Fore.GREEN}REST{Style.RESET_ALL} for {Fore.YELLOW}{timer_val}{Style.RESET_ALL} minutes""")
    elif message == "summary_and_quit":
        sys.stdout.write("\033[K")
        print(
            f"{Fore.BLUE}Press ENTER to stop timer.{Style.RESET_ALL}",
        )
    elif message == "show_insights":
        print(f"\n{Fore.BLUE}Press ENTER to return to main menu{Style.RESET_ALL}")
    elif message == "bar_header":
        print(f"{Fore.YELLOW}Weekly minutes{Style.RESET_ALL}")
    elif message == "heat_header":
        print(f"{Fore.YELLOW}Work heatmap{Style.RESET_ALL}")
    elif message == "cursor":
        return f"{Fore.MAGENTA}>> {Style.RESET_ALL}"


def options():
    return """Additional commands;
S       --    Swap upcoming timer
I       --    Show the insights tab
Q       --    Quit SYLO
"""


def print_update(durations: Durations, mode: str, show_options: bool = False, show_graphs: bool = False):
    logger.debug(f'Printing update: {mode} with show_options {show_options}')
    if mode == 'rest':
        upcoming_timer_color = durations.rest.bar_color
    else:
        upcoming_timer_color = durations.work.bar_color

    if show_options:
        print_ops = options()
    else:
        print_ops = '.. or chose an optional command (H for help)'

    print(
        f"""Total {Fore.RED}work{Style.RESET_ALL} today:           {Fore.YELLOW}{int(durations.total_work_mins)} minutes{Style.RESET_ALL}
Total {Fore.GREEN}rest{Style.RESET_ALL} today:           {Fore.YELLOW}{int(durations.total_rest_mins)} minutes{Style.RESET_ALL}

Upcoming timer:     {upcoming_timer_color}{mode.upper()}{Style.RESET_ALL}

{Fore.BLUE}Press {Style.RESET_ALL}{Fore.YELLOW}ENTER {Style.RESET_ALL}{Fore.BLUE}to start the next timer{Style.RESET_ALL}

{Fore.BLUE}{print_ops}{Style.RESET_ALL}

    """)


def ascii_header(font: str):
    return figlet_format('Sort Your Life Out', font=font, width=40)


def print_header_small(double: bool):
    if RANDOM_FONTS is True:
        font = random_ascii_header()
    else:
        font = ascii_header_small(font='alligator')
    if double is True:
        color = Fore.RED
        double_message = '>>>>>>>>>>>> DOUBLE SPEED MODE >>>>>>>>>>>>'
    else:
        color = Fore.BLUE
        double_message = ''
    print(f"{double_message}")
    print(f"""{color}{font}{Style.RESET_ALL}""")


def ascii_header_small(font: str):
    return figlet_format('SYLO', font=font, width=60)


def random_ascii_header():
    fonts = FigletFont.getFonts()
    random_fonts = sample(fonts, int(len(fonts)/2))
    for f in random_fonts:
        try:
            logger.debug(f'Output of shuffled fonts: {f}')
            return figlet_format('SYLO', font=f, width=40)
        except Exception as e:
            logger.debug(f'Output of shuffled fonts: {f} {e}')
            pass
