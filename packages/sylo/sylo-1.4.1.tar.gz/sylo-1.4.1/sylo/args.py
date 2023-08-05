import argparse


def get_arguments():
    parser = argparse.ArgumentParser(
        description="Sort Your Life Out! Python Pomodoro Timer"
    )
    parser.add_argument(
        "-w",
        "--work_time",
        help="Set the work time length",
        type=int)
    parser.add_argument(
        "-r",
        "--rest_time",
        help="Set the rest time length",
        type=int
    )
    parser.add_argument(
        "-a",
        "--audio_file",
        help="""Set the full path to an audio \
        file you want to be played on completion of a timer""",
        type=str
    )
    parser.add_argument(
        "-l",
        "--log",
        help="Set the log level",
        type=str,
        choices=[
            'DEBUG',
            'INFO',
        ]
    )
    parser.add_argument(
        "-d",
        '--double_speed',
        dest='double_speed',
        action='store_true'
    )
    parser.set_defaults(
        double_speed=False,
    )
    return parser.parse_args()
