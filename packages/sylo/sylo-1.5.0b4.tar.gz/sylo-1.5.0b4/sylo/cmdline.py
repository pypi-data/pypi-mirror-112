import logging
from sylo.sylo import run
from sylo.args import get_arguments
from sylo.logging import logging_config
from sylo.definitions import set_theme

logger = logging.getLogger(__name__)


def main():
    args = get_arguments()
    logging_config(args.log)
    set_theme(args.theme)
    run(args)
    logger.info("Started from cli")
