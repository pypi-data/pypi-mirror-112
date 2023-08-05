import logging
from sylo.args import get_arguments
from sylo.timer import run
from sylo.logging import logging_config
logger = logging.getLogger(__name__)


def main():
    args = get_arguments()
    logging_config(args.log)
    run(args)
    logger.info('Started from __main__')


if __name__ == "__main__":

    main()
