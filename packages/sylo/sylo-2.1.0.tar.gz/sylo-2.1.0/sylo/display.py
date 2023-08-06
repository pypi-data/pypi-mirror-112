from pyfiglet import figlet_format
from typing import List
from colorama import Fore, Style
import sys
import logging
from sylo.models import Durations, Config


logger = logging.getLogger(__name__)


config = Config()


class Display:
    def __init__(self, theme_color: str = config.theme_color):
        self.theme = self.color_map(theme_color)

    def col(self, string: str, color: str = None):
        if color:
            return f"{self.color_map(color)}{string}{Style.RESET_ALL}"
        else:
            return f"{self.theme}{string}{Style.RESET_ALL}"

    def print_timer(self, mode: str, timer_val: int, tasks: List = None):
        if mode == "work":
            self.print_header_small()
            self.print_tasks(tasks)
            print(
                f"{self.col('Press')} {self.col('Ctrl-C', 'yellow')} {self.col('to stop timer early.')}"
                "\n"
                f"\n{self.col('WORK', 'red')} "
                f"for {self.col(str(timer_val), 'yellow')} minutes"
            )
        else:
            self.print_header_small()
            print(
                f"Ctrl-C to stop timer early."
                f"\n{self.col('REST', 'green')} "
                f"for {self.col(str(timer_val), 'yellow')} minutes"
            )

    def print_summary_and_quit(self):
        sys.stdout.write("\033[K")
        print(
            f"{self.col('Press')} "
            f"{self.col('ENTER', 'yellow')}"
            f"{self.col('to stop timer.')}",
        )

    def print_insights(self):
        print(
            f"\n{self.col('Press')} "
            f"{self.col('ENTER', 'yellow')} "
            f"{self.col('to return to main menu.')}"
        )

    def print_bar_header(self):
        print(f"{self.col('Weekly Minutes', 'yellow')}")

    def print_heat_header(self):
        print(f"{self.col('Work Heatmap', 'yellow')}")

    def cursor(self):
        return self.col(">> ", "yellow")

    def print_options(self):
        print(
            f"{self.col('Additional commands;')}"
            f"\n{self.col('S', 'yellow')}{self.col('       --    Swap upcoming timer')}"
            f"\n{self.col('T', 'yellow')}{self.col('       --    Show task view')}"
            f"\n{self.col('I', 'yellow')}{self.col('       --    Show insights view')}"
            f"\n{self.col('Q', 'yellow')}{self.col('       --    Quit')}"
        )

    def print_splash_prompt(self):
        print(
            f"{self.col('Press')} "
            f"{self.col('ENTER', 'yellow')} "
            f"{self.col('to start the next timer.')}"
        )

    def print_today_yesterday_tasks(self, day: str):
        print(f"{self.col(day)}")

    def print_offer_options(self):
        print(f"{self.col('Press')} {self.col('H', 'yellow')} {self.col('for Help.')}")

    def print_add_task_or_quit(self):
        print(
            f"{self.col('Press')} "
            f"{self.col('ENTER', 'yellow')} "
            f"{self.col('to go back')} "
            f"\n{self.col('Press')} {self.col('N', 'yellow')} "
            f"{self.col('to add a new task')}"
            f"\n{self.col('Press')} {self.col('C', 'yellow')} "
            f"{self.col('to toggle completion of a task')}"
        )

    def print_new_task(self):
        print(f"{self.col('Input a new task')}")

    def print_edit_task(self):
        print(f"{self.col('Pick a task to complete/put back')}")

    def print_splash(self, durations: Durations, mode: str):
        print(
            f"Total {self.col('work', 'red')} today:            "
            f"{str(int(durations.total_work_mins))} minutes"
            f"\nTotal {self.col('rest', 'green')} today:            "
            f"{str(int(durations.total_rest_mins))} minutes"
            f"\nUpcoming timer:              "
            f"{self.col(mode.upper(), self._set_mode_color(mode, durations))}"
            f"\n"
        )

    def print_splash_variants(
        self,
        durations: Durations,
        mode: str,
        is_options: bool = None,
        is_tasks: bool = None,
        tasks: List = None,
    ):
        logger.info(f"Splash. is_options: {is_options} is_tasks: {is_tasks}")
        self.print_header_small()
        self.print_splash(durations, mode)
        if is_options is True and is_tasks is False:
            self.print_options()
            self.print_splash_prompt()
        elif is_options is False and is_tasks is True:
            self.print_tasks(tasks)
            self.print_splash_prompt()
            self.print_offer_options()
        elif is_options is True and is_tasks is True:
            self.print_tasks(tasks)
            self.print_options()
            self.print_splash_prompt()
        else:
            self.print_splash_prompt()
            self.print_offer_options()

    def print_tasks(self, tasks: List = None):
        if tasks:
            print(f'{self.col(f"Completed tasks")}')
            print(
                "\n".join("".join(map(str,
                                      f"{self.col(t[0], 'yellow')}   "
                                      f"{self.col(t[1],'green')}   --  "
                                      f"{self.col(t[2],'green')}"))
                          for t in tasks if t[3] == '1'))
            print("\n")
            print(f'{self.col(f"Incomplete tasks")}')
            print("\n".join("".join(map(str,
                                        f"{self.col(t[0], 'yellow')}   "
                                        f"{t[1]}   --  "
                                        f"{t[2]}"))
                            for t in tasks if t[3] == '0'))
            print("\n")

    def print_header_small(self):
        print(self.col(self.ascii_header(string="SYLO", font="alligator", width=60)))

    @staticmethod
    def color_map(color: str):
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
        return colors[color]

    @staticmethod
    def ascii_header(string: str, font: str, width: int):
        return figlet_format(string, font=font, width=width)

    @staticmethod
    def _set_mode_color(mode: str, durations: Durations):
        if mode == "rest":
            return durations.rest.bar_color
        else:
            return durations.work.bar_color
