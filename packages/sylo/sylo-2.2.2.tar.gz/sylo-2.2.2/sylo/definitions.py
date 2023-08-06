import os
import datetime
from pathlib import Path


HOME_DIR = home = str(Path.home())
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

TODAY = datetime.datetime.now().date()
YESTERDAY = (datetime.datetime.now() - datetime.timedelta(days=1)).date()

TODAY_STR = TODAY.strftime("%Y-%m-%d")
YESTERDAY_STR = YESTERDAY.strftime("%Y-%m-%d")

FORTNIGHT_AGO = (datetime.datetime.now() - datetime.timedelta(days=14)).date()
ONE_YEAR_AGO = (datetime.datetime.now() - datetime.timedelta(days=364)).date()

DATA_FILE_LOCATION = f"{HOME_DIR}/.sylo/sessions.dat"
TASK_FILE_LOCATION = f"{HOME_DIR}/.sylo/tasks.dat"
CONFIG_FILE_LOCATION = f"{HOME_DIR}/.sylo/sylo.cfg"
POMS_DATA_FILE_LOCATION = f"{HOME_DIR}/.sylo/poms.dat"

HOME_DIR_CREATE = f"mkdir {HOME_DIR}/.sylo"
DATA_FILE_CREATE = f'echo "{TODAY_STR},0,0" > {DATA_FILE_LOCATION}'
TASK_FILE_CREATE = f"touch {TASK_FILE_LOCATION}"
POMS_DATA_FILE_CREATE = f'echo "{TODAY_STR},0" > {POMS_DATA_FILE_LOCATION}'

WELCOME_CHOICES = ("", "h", "q", "s", "i", "t", "y", "a")

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

METRICS_HEAT = 'termgraph --calendar --color magenta --start-dt "%s" %s 2>/dev/null'

METRICS_BAR = 'termgraph %s --color {red,green} --start-dt "%s" 2>/dev/null'

POMS_METRICS_BAR = 'termgraph %s --color magenta --start-dt "%s" 2>/dev/null'
