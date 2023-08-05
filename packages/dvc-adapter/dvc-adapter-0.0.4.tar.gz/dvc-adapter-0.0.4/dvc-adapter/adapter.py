import argparse
import sys

import logging.config

import os.path

from .logger import LOGGING_CONFIG

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--log-level', type=str, default="INFO", help="defines log level of adapter")
    parser.add_argument('--config-path', type=str, required=True, dest="config_path", help="defines the base value")
    args = parser.parse_args()

    if not os.path.isfile(args.config_path):
        logger.error(f"No such file exists: {args.config_path}")
        sys.exit()

