import os
import sys

from loguru import logger


class Logger:
    def __init__(self, log_file: str):
        os.chdir(os.path.dirname(__file__))
        self._config_path = os.path.abspath(r"../config/config.json")
        self._log_fmt = "{time:YYYY-MM-DD HH:mm:ss.SSS} [<level>{level:<5}</level>] {file}.{line}: {message}"
        self._debug_fmt = "{time:YYYY-MM-DD HH:mm:ss.SSS} [<level>{level:<5}</level>] {name}:{function}:{line}: {message}"
        self._logger_conf(log_file)
        self.logger = logger

    def _logger_conf(self, log_file):
        self._get_level()
        logger.remove()
        logger.add(sink=sys.stderr, format=self._log_fmt, level="INFO")
        if self._level == "INFO":
            logger.add(sink=log_file, format=self._log_fmt, rotation="1 MB", level=self._level)
        else:
            logger.add(sink=log_file, format=self._debug_fmt, rotation="1 MB", level=self._level)
        logger.info("".center(50, '-'))
        logger.info("The logger is started".center(50, '-'))
        logger.info("".center(50, '-'))
        if self._level == "DEBUG":
            logger.debug("The debug mode is enabled.")

    def _get_level(self):
        level_raw = ""
        try:
            with open(self._config_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
                for i in lines:
                    if "level" in i and ";" != i[0]:
                        level_raw = i
        except:
            level_raw = '"level": "DEBUG",'
        if "DEBUG" in level_raw:
            self._level = "DEBUG"
        else:
            self._level = "INFO"


handlers = Logger("../log/log.log")
logger = handlers.logger
