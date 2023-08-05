import logging
from dataclasses import dataclass
from colorama import Fore
from sylo.definitions import TIMER_DEFAULTS, DATA_FILE_LOCATION, TODAY_STR
import pandas as pd

logger = logging.getLogger(__name__)


@dataclass
class Rest:
    mins: int = TIMER_DEFAULTS["rest"]["mins"]
    secs: int = TIMER_DEFAULTS["rest"]["secs"]
    bar_color: str = Fore.GREEN


@dataclass
class Work:
    mins: int = TIMER_DEFAULTS["work"]["mins"]
    secs: int = TIMER_DEFAULTS["work"]["secs"]
    bar_color: str = Fore.RED


@dataclass
class Durations:
    work = Work
    rest = Rest
    total_work_mins: float = 0
    total_rest_mins: float = 0

    def __post_init__(self):
        self.work = Work()
        self.rest = Rest()


class DataPersistence:

    def __init__(self, data_file: str = DATA_FILE_LOCATION):
        self.data_file = data_file
        self.file_cols = ["date", "time_worked", "time_rested"]

    def data_refresh(self, durations: Durations):
        new_df = self.fetch_and_update_values(durations, TODAY_STR)
        new_df.to_csv(DATA_FILE_LOCATION, sep=',', mode='w', header=False)

    def data_load_on_boot(self, durations: Durations):
        df = self._read_file()
        try:
            filtered_dates = df.loc[TODAY_STR]
            logger.info('data_load_on_boot Found data for today')
            work_time_today = float(filtered_dates['time_worked'])
            rest_time_today = float(filtered_dates['time_rested'])
            logger.info(f'Work time loaded on boot: {work_time_today}')
            logger.info(f'Rest time loaded on boot: {rest_time_today}')
            durations.total_work_mins = work_time_today
            durations.total_rest_mins = rest_time_today
        except Exception:
            logger.info('data_load_on_boot NO DATA for today')
            filtered_dates = None
        if filtered_dates is None:
            durations.total_rest_mins = 0
            durations.total_work_mins = 0

    def _read_file(self):
        df = pd.read_csv(self.data_file, header=None, sep=',')
        df.columns = self.file_cols
        df.set_index('date', inplace=True, drop=True)
        return df

    def fetch_and_update_values(self, durations: Durations, date: str = TODAY_STR):
        df = self._read_file()
        new_df = pd.DataFrame({
            'date': [date],
            'time_worked': [durations.total_work_mins],
            'time_rested': [durations.total_rest_mins]
        }, columns=self.file_cols, dtype='float')
        new_df.set_index('date', inplace=True, drop=True)
        out = new_df.combine_first(df)
        return out
