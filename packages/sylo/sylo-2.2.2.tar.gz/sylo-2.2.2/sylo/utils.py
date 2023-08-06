import os
import logging
import subprocess
import sys

logger = logging.getLogger(__name__)


def get_input(text):
    return input(text)


def run_subprocess(script: str):
    if "rm " in script:
        logger.warning("UNSAFE SCRIPT")
        sys.exit()
    try:
        subprocess.run(script, shell=True, check=True, timeout=30)
    except subprocess.CalledProcessError:
        print(
            "Insights panel not loading as there is no data to display. "
            "\nTry working for a few mins then check back later."
        )
        print("\n")


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def mins_to_secs(minutes: int):
    return minutes * 60


def flip_mode(mode: str):
    if mode == "work":
        logger.debug(f"flip_mode took {mode} returned rest")
        return "rest"
    else:
        logger.debug(f"flip_mode took {mode} returned work")
        return "work"


def check_for_file(path):
    is_file = os.path.isfile(path)
    logger.info(f"check_for_file {path} {is_file}")
    return is_file
