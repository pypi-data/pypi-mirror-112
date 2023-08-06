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

CONFIG_FILE_LOCATION = f"{HOME_DIR}/.sylo/sylo.cfg"
HOME_DIR_CREATE = f"mkdir {HOME_DIR}/.sylo"
SYLO_HOME = f"{HOME_DIR}/.sylo"


WELCOME_CHOICES = ("", "h", "q", "s", "t", "y", "a")  # "i",

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

SQLITE_DB = f"{HOME_DIR}/.sylo/_sylo.db"

BOOTSTRAP_SQL = f"{ROOT_DIR}/database_interactions/bootstrap.sql"
