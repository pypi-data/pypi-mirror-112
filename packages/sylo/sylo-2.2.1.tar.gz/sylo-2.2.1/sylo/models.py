import logging
from dataclasses import dataclass
import pandas as pd
from sylo.definitions import (
    TIMER_DEFAULTS,
    DATA_FILE_LOCATION,
    TODAY_STR,
    TASK_FILE_LOCATION,
    CONFIG_FILE_LOCATION,
    POMS_DATA_FILE_LOCATION,
)
from sylo.utils import check_for_file, mins_to_secs
import tomli
import csv
from typing import List


logger = logging.getLogger(__name__)


@dataclass
class Rest:
    mins: int = TIMER_DEFAULTS["rest"]["mins"]
    secs: int = TIMER_DEFAULTS["rest"]["secs"]
    bar_color: str = "green"


@dataclass
class Work:
    mins: int = TIMER_DEFAULTS["work"]["mins"]
    secs: int = TIMER_DEFAULTS["work"]["secs"]
    bar_color: str = "red"


@dataclass
class Durations:
    work = Work
    rest = Rest
    total_work_mins: float = 0
    total_rest_mins: float = 0
    poms = float = 0

    def __post_init__(self):
        self.work = Work()
        self.rest = Rest()


@dataclass
class Config:
    theme_color = "blue"
    audio_file = None
    work_time = 25
    rest_time = 5
    pom_name = "Pomodoro"


class ConfigFile:
    def __init__(self):
        self.config_file = CONFIG_FILE_LOCATION
        self.is_config = check_for_file(self.config_file)

    def load_config(self):
        with open(self.config_file, encoding="utf-8") as f:
            return tomli.load(f)

    def set_config(self, config: Config, durations_model: Durations):
        if self.is_config is True:
            config_file = self.load_config()
            logger.info(config_file)
            try:
                general = config_file["general"]
                logger.info(f"CONFIG: general from file: {general}")
                config.theme_color = general["theme"]
                logger.info(f"CONFIG:set theme_color to {config.theme_color}")

            except KeyError as k:
                logger.info(k)
                pass
            try:
                general = config_file["general"]
                config.audio_file = general["audio_file"]
                logger.info(f"CONFIG:set audio_file to {config.audio_file}")
            except KeyError as k:
                logger.info(k)
                pass
            try:
                general = config_file["general"]
                config.pom_name = general["time_segment_name"]
                logger.info(f"CONFIG:set pom_name to {config.pom_name}")
            except KeyError as k:
                logger.info(k)
                pass

            try:
                durations = config_file["durations"]
                logger.info(f"CONFIG: durations from file: {durations}")
                durations_model.work.mins = durations["work"]
                durations_model.work.secs = mins_to_secs(durations["work"])
                durations_model.rest.mins = durations["work"]
                durations_model.rest.secs = mins_to_secs(durations["rest"])
            except KeyError as k:
                logger.info(k)
                pass


class DataPersistence:
    def __init__(
        self,
        data_file: str = DATA_FILE_LOCATION,
        poms_data_file: str = POMS_DATA_FILE_LOCATION,
    ):
        self.data_file = data_file
        self.poms_data_file = poms_data_file
        self.file_cols = ["date", "time_worked", "time_rested"]
        self.pom_file_cols = ["date", "poms"]

    def data_refresh(self, durations: Durations):
        new_df = self.fetch_and_update_values(durations, TODAY_STR)
        new_df.to_csv(DATA_FILE_LOCATION, sep=",", mode="w", header=False)
        new_df_poms = self.fetch_and_update_values_poms(durations, TODAY_STR)
        new_df_poms.to_csv(POMS_DATA_FILE_LOCATION, sep=",", mode="w", header=False)

    def data_load_on_boot(self, durations: Durations):
        df = self._read_file_to_df(self.data_file, self.file_cols)
        poms_df = self._read_file_to_df(self.poms_data_file, self.pom_file_cols)
        try:
            filtered_dates = df.loc[TODAY_STR]
            logger.info("data_load_on_boot Found data for today")
            work_time_today = float(filtered_dates["time_worked"])
            rest_time_today = float(filtered_dates["time_rested"])
            logger.info(f"Work time loaded on boot: {work_time_today}")
            logger.info(f"Rest time loaded on boot: {rest_time_today}")
            durations.total_work_mins = work_time_today
            durations.total_rest_mins = rest_time_today
        except Exception:
            logger.info("data_load_on_boot NO DATA for today")
            filtered_dates = None
        if filtered_dates is None:
            durations.total_rest_mins = 0
            durations.total_work_mins = 0

        try:
            filtered_dates = poms_df.loc[TODAY_STR]
            logger.info("data_load_on_boot Found data for today")
            poms_today = float(filtered_dates["poms"])
            logger.info(f"Rest time loaded on boot: {poms_today}")
            durations.poms = poms_today
        except Exception:
            logger.info("data_load_on_boot NO DATA for today")
            filtered_dates = None
        if filtered_dates is None:
            durations.poms = 0

    @staticmethod
    def _read_file_to_df(data_file: str, cols: List):
        df = pd.read_csv(data_file, header=None, sep=",")
        df.columns = cols
        df.set_index("date", inplace=True, drop=True)
        return df

    def fetch_and_update_values(self, durations: Durations, date: str = TODAY_STR):
        df = self._read_file_to_df(self.data_file, self.file_cols)
        new_df = pd.DataFrame(
            {
                "date": [date],
                "time_worked": [durations.total_work_mins],
                "time_rested": [durations.total_rest_mins],
            },
            columns=self.file_cols,
            dtype="float",
        )
        new_df.set_index("date", inplace=True, drop=True)
        out = new_df.combine_first(df)
        return out

    def fetch_and_update_values_poms(self, durations: Durations, date: str = TODAY_STR):
        df = self._read_file_to_df(self.poms_data_file, self.pom_file_cols)
        new_df = pd.DataFrame(
            {"date": [date], "poms": [durations.poms]},
            columns=self.pom_file_cols,
            dtype="float",
        )
        new_df.set_index("date", inplace=True, drop=True)
        out = new_df.combine_first(df)
        return out


def get_tasks(date: str = None):
    try:
        with open(TASK_FILE_LOCATION, "r") as read_obj:
            csv_reader = csv.reader(read_obj)
            logger.info(f"Returning tasks for {date}")
            if date:
                return [row for row in csv_reader if row[1] == date]
            else:
                return [row for row in csv_reader]
    except Exception as e:
        print(e)


def get_max_id_in_csv(tasks: List):
    if tasks:
        return max(t[0] for t in tasks)
    else:
        return 0


def complete_task(task_id: str):
    row_list = []
    with open(TASK_FILE_LOCATION, "r") as readFile:
        reader = csv.reader(readFile)
        for row in reader:
            row_list.append(row)
            if row[0] == task_id:
                if row[4] == "1":
                    row[4] = "0"
                else:
                    row[4] = "1"
    with open(TASK_FILE_LOCATION, "w") as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(row_list)


def remove_task(task_id: str):
    row_list = []
    with open(TASK_FILE_LOCATION, "r") as readFile:
        reader = csv.reader(readFile)
        for row in reader:
            row_list.append(row)
            if row[0] == task_id:
                row_list.remove(row)
    with open(TASK_FILE_LOCATION, "w") as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(row_list)
