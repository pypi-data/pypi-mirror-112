import os
import datetime
from pathlib import Path

HOME_DIR = home = str(Path.home())
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# TODAY = (datetime.datetime.now() + datetime.timedelta(days=1)).date()
TODAY = datetime.datetime.now().date()
TODAY_STR = TODAY.strftime("%Y-%m-%d")
ONE_WEEK_AGO = (datetime.datetime.now() - datetime.timedelta(days=7)).date()
ONE_YEAR_AGO = (datetime.datetime.now() - datetime.timedelta(days=364)).date()

DATA_FILE_LOCATION = f'{HOME_DIR}/.sylo/sessions.dat'
HOME_DIR_CREATE = f'mkdir {HOME_DIR}/.sylo'
DATA_FILE_CREATE = f'echo "{TODAY_STR},0,0" > {HOME_DIR}/.sylo/sessions.dat'


WELCOME_CHOICES = (
    "",
    "q",
    "s",
    "i"
)

TIMER_DEFAULTS = {
    "work": {
        "mins": 25,
        "secs": 1500,
    },
    "rest": {
        "mins": 5,
        "secs": 300,
    }
}

COUNTDOWN_INCREMENTS = 1


# Experimental Features

RANDOM_FONTS = False

METRICS_HEAT = 'termgraph --calendar --start-dt "%s" %s '

METRICS_BAR = 'termgraph %s --color {red,green} --start-dt "%s"'
