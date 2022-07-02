import json
import requests
from common.utils import utils
from common.logger import logger
from common.config import config


class Report:
    @logger.catch
    def __init__(self):
        self._error = 0
        self._errno = 0
        self._session = 0
        self._headers = 0
        self._url = None
        self._payload = None
        self._msg_footer = None
        self.fetch_param()

    @logger.catch
    def fetch_param(self):
        self._url = config.config('/config/url', utils.get_call_loc())
        self._payload = config.config('/config/payload', utils.get_call_loc())
        self._msg_footer = config.config('/config/copyright', utils.get_call_loc())
        logger.debug("Fetched [Report] params.")

    @logger.catch
    def _set_error(self, no, flag, func):
        self._errno = no
        logger.debug(f"[{func}] Set the error code: {self._errno}.")
        self._error = flag
        logger.debug(f"[{func}] Set the error flag: {self._error}.")

    @logger.catch
    def _fetch_data(self, date):
        if self._error == 1:
            logger.debug(f"The error flag: {self._error}. Exit the function.")
            return
        payload = self._payload
        payload["toDate"] = date
        payload = f"siteResJson={json.dumps(payload)}"
        res = self._session.post(url=self._url, headers=self._headers, data=payload)
        logger.debug(f"URL:{self._url}. Payload:{payload}. Status code:{res.status_code}")
        if res.status_code != 200:
            logger.error(f"Failed:POST request. URL:{self._url}. Status code:{res.status_code}")
            self._set_error(1, 1, utils.get_call_loc(True))
            return []
        else:
            logger.info(f"Successful to fetch the data")
        res.encoding = "utf-8"
        return json.loads(res.text)

    @logger.catch
    def _parse_data(self, raw):
        if self._error == 1:
            logger.debug(f"The error flag: {self._error}. Exit the function.")
            return
        available = []
        for sail_info in raw["message"]:
            if sail_info["totalRemainVolume"] != "0":
                available.append(sail_info)
        return available

    @logger.catch
    def _format_msg(self, msg, date):
        if self._error == 1:
            logger.debug(f"The error flag: {self._error}. Exit the function.")
            return
        ticket_info = ""
        if not msg:
            header = f"出发日期: {date}\n"
            ticket_info = "\n当前无票\n"
        else:
            header = f"出发日期: {msg[0]['startDate']}\n轮船型号: {msg[0]['shipName']}\n"
            for i in msg:
                seat_detail = [{seatType['seatTypeName']: seatType['num']} for seatType in i['seatList']]
                ticket_info += f"\n出发时间: {i['goTime']}\n剩余船票数量: {i['totalRemainVolume']}\n详情: {seat_detail}\n"
        formatted_msg = header + ticket_info + self._msg_footer
        return formatted_msg

    @logger.catch
    def main(self, departure_date):
        self._error = 0
        self._errno = 0
        self._session = requests.Session()
        self._headers = {
            # 必须添加 Content-Type 字段:[x-www-form-urlencoded]
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            "User-Agent": utils.get_random_useragent()
        }
        msg = self._parse_data(self._fetch_data(departure_date))
        ret = self._format_msg(msg, departure_date)
        if self._error != 1:
            return self._errno, ret
        else:
            return self._errno, ret


report = Report()
