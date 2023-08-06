import logging
from dataclasses import dataclass
import pandas as pd
from sylo.definitions import (
    TIMER_DEFAULTS,
    TODAY_STR,
    CONFIG_FILE_LOCATION,
    SQLITE_DB,
    BOOTSTRAP_SQL,
    SESSIONS_ALL,
    SESSIONS_COLS,
    SESSIONS_INDEX,
    POMS_ALL,
    POMS_COLS,
    POMS_INDEX,
)
from sylo.utils import check_for_file, mins_to_secs, read_from_file
import tomli
from typing import List
import sqlite3


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
                durations_model.rest.mins = durations["rest"]
                durations_model.rest.secs = mins_to_secs(durations["rest"])
            except KeyError as k:
                logger.info(k)
                pass


class Database:
    def __init__(self):
        self.db_file = SQLITE_DB

    def _connect(self):
        return sqlite3.connect(self.db_file)

    def execute(self, query: str):
        con = self._connect()
        cur = con.cursor()
        cur.execute(query)
        con.commit()
        con.close()

    def execute_script(self, query: str):
        con = self._connect()
        cur = con.cursor()
        cur.executescript(query)
        con.commit()
        con.close()

    def select(self, query: str):
        con = self._connect()
        cur = con.cursor()
        result = cur.execute(query)
        data = result.fetchall()
        cur.close()
        return data

    def execute_from_file(self, file: str):
        with open(file, "r") as read_file:
            query = read_file.read()
        self.execute_script(query)

    def select_from_file(self, file: str):
        with open(file, "r") as read_file:
            query = read_file.read()
        return self.select(query)

    def bootstrap_on_first_boot(self):
        self.execute_from_file(BOOTSTRAP_SQL)

    def sql_to_df(self, sql: str, cols: List, index_col: str = None):
        df = pd.read_sql_query(sql, con=self._connect())
        df.columns = cols
        df.set_index(index_col, inplace=True, drop=True)
        return df

    def initial_data_load(self, durations: Durations):
        df = self.sql_to_df(read_from_file(
            SESSIONS_ALL),
            SESSIONS_COLS,
            SESSIONS_INDEX,
        )
        poms_df = self.sql_to_df(read_from_file(
            POMS_ALL),
            POMS_COLS,
            POMS_INDEX,
        )
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
