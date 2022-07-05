import os
import sys

from common.logger import logger
from fake_useragent import UserAgent


class Utils:
    @logger.catch
    def __init__(self):
        self._ua = UserAgent(verify_ssl=False)

    @logger.catch
    def get_random_useragent(self):
        random_ua = self._ua.random
        logger.debug(f"User Agent:{random_ua}")
        return random_ua

    @staticmethod
    @logger.catch
    def version(version):
        num, stage = version.split("|")
        if os.path.exists("../.git"):
            logger.debug(f'Founded [{os.path.abspath("../.git")}]')
            commit_id = (os.popen("git rev-parse --short HEAD").read()).replace("\n", "")
            commit_id = "." + commit_id
        else:
            commit_id = ""
        if stage != "":
            stage = f"({stage})"
        info = f"{num}{commit_id}{stage}"
        logger.info(f"Version:{info}")

    @staticmethod
    def get_call_loc(func=False):
        file_name = os.path.basename(sys._getframe().f_back.f_code.co_filename)
        line = sys._getframe().f_back.f_lineno
        if func:
            func_name = sys._getframe().f_back.f_code.co_name
            return f"{file_name}:{func_name}:{line}"
        else:
            return f"{file_name}:{line}"

    @logger.catch
    def refresh_param(self):
        from common.service import service
        service.fetch_param()
        from common.report import report
        report.fetch_param()
        from common.push import push
        push.fetch_param()
        push.bot_email.fetch_param()


utils = Utils()
