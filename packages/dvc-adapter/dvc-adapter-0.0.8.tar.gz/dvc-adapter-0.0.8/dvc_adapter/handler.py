import logging

from watchdog.events import FileSystemEventHandler

logger = logging.getLogger(__name__)

class Handler(FileSystemEventHandler):
    def on_created(self, event):
        logger.info(event)

    def on_modified(self, event):
        logger.info(event)