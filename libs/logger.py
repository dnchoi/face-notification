import logging
import os
import sys
from datetime import datetime
from logging import handlers

import colorlog


class Logger:
    """class path finding logger"""

    def __init__(
        self,
        class_name,
        level: str = "INFO",
        file_path: str = "logs",
        save: bool = False,
    ):
        self.file_path = file_path
        os.makedirs(self.file_path, exist_ok=True)

        self.settings = {
            "LEVEL": self.lookup_table(level),
            "FILENAME": class_name,
            "MAYBYTES": 15 * 1024 * 1024,
            "BACKUPCOUNT": 100,
            "FORMAT": "%(log_color)s[%(levelname)-8s]%(reset)s <%(name)s>: %(module)s:%(lineno)d:  %(message)s",
            "SAVE": save,
        }
        self.logger_initialize()

    def lookup_table(self, idx):
        lvl = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL,
        }

        return lvl.get(idx, "INFO")

    def logger_initialize(self):
        self.logger = logging.getLogger(self.settings["FILENAME"])
        if len(self.logger.handlers) > 0:
            return self.logger
        stream_formatter = colorlog.ColoredFormatter(self.settings["FORMAT"])
        file_formatter = logging.Formatter(
            "%(asctime)s [%(levelname)-8s] <%(name)s>: %(module)s:%(lineno)d: %(message)s"
        )

        stream_handler = colorlog.StreamHandler(sys.stdout)
        now_date_time = "{:%Y-%m-%d}".format(datetime.now())
        file_handler = handlers.TimedRotatingFileHandler(
            os.path.abspath(
                f"{self.file_path}/{now_date_time}-{self.settings['FILENAME']}.log"
            ),
            when="midnight",
            interval=1,
            backupCount=self.settings["BACKUPCOUNT"],
            encoding="utf-8",
        )
        stream_handler.setFormatter(stream_formatter)
        self.logger.addHandler(stream_handler)
        if self.settings["SAVE"]:
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(file_handler)

        self.logger.setLevel(self.settings["LEVEL"])

        return self.logger