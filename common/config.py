import os
import json
from common.logger import logger


class Config:
    @logger.catch
    def __init__(self, config_file=r"../config/config.json"):
        example = os.path.abspath("../config/config_example.json")
        os.chdir(os.path.dirname(__file__))
        self._path = os.path.abspath(config_file)
        if not os.path.exists(self._path):
            logger.error(f"No such file [{self._path}]")
            if os.path.exists(example):
                logger.error(f"Please rename [{example}] to [{self._path}]")
            raise FileNotFoundError(f"No such file [{self._path}]")
        self.raw = {}
        self._json_read()

    @logger.catch
    def _json_read(self):
        with open(self._path, 'r', encoding='utf-8') as f:
            self.raw = json.load(f)
        logger.debug(f"Loaded [{self._path}]")

    @logger.catch
    def config(self, pointer, func):
        if pointer[0] != "/":
            pointer = f"/{pointer}"
        keys = pointer.split("/")[1:]
        ret = self.raw
        try:
            for i in keys:
                ret = ret[str(i)]
        except Exception as e:
            logger.error(e)
            ret = ""
        if keys[-1] in ["email_pwd", "api"]:
            logger.debug(f'[{func}] Json pointer [{pointer}]:"*******"')
        else:
            logger.debug(f'[{func}] Json pointer [{pointer}]:"{ret}"')
        return ret

    @logger.catch
    def refresh(self):
        self._json_read()
        logger.debug(f"Refreshed [{self._path}]")


config = Config(r"../config/config.json")
