import time
import argparse
import sys
import os
import logging

from watchdog.observers import Observer

from .handler import Handler

logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--log-level', type=str, default="INFO", help="defines log level of adapter")
    parser.add_argument('--config-path', type=str, required=True, dest="config_path", help="defines the base value")
    args = parser.parse_args()

    if not os.path.isfile(args.config_path):
        logger.error(f"No such file exists: {args.config_path}")
        sys.exit()

    observer = Observer()
    observer.schedule(Handler(), path=args.config_path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
            logger.info("Run iteration!")
    except KeyboardInterrupt:
        observer.stop()
        observer.join()