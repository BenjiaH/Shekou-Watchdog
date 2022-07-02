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
        self._all_data = []
        self._url = None
        self._payload_fs_s = None
        self._payload = None
        self._bank = None
        self.fetch_param()
        self._msg_footer = "\n数据来源：蛇口邮轮母港|侵权请联系删除"

    @logger.catch
    def fetch_param(self):
        self._url = config.config('/config/url', utils.get_call_loc())
        self._payload = config.config('/config/payload', utils.get_call_loc())
        logger.debug("Fetched [Report] params.")

    @logger.catch
    def _set_error(self, no, flag, func):
        self._errno = no
        logger.debug(f"[{func}] Set the error code: {self._errno}.")
        self._error = flag
        logger.debug(f"[{func}] Set the error flag: {self._error}.")

    @logger.catch
    def _fetch_data(self, sail_date):
        if self._error == 1:
            logger.debug(f"The error flag: {self._error}. Exit the function.")
            return
        url = self._url
        payload = self._payload
        payload["toDate"] = sail_date
        payload = f"siteResJson={json.dumps(payload)}"
        res = self._session.post(url=url, headers=self._headers, data=payload)
        logger.debug(f"URL:{url}. Payload:{payload}. Status code:{res.status_code}")
        if res.status_code != 200:
            logger.error(f"Failed:GET request. URL:{url}. Status code:{res.status_code}")
        res.encoding = "utf-8"
        return json.loads(res.text)

    @logger.catch
    def _parse_data(self, raw):
        available = []
        for sail_info in raw["message"]:
            if sail_info["totalRemainVolume"] != "0":
                available.append(sail_info)
        # print(available)
        return available

    @logger.catch
    def _format_msg(self, msg, sail_date):
        if not msg:
            header = f"出发日期: {sail_date}"
            ticket_info = "\n当前无票"
        else:
            header = f"""
出发日期: {msg[0]['startDate']}
轮船型号: {msg[0]['shipName']}
"""
            ticket_info = ""
            for i in msg:
                ticket_info += f"""
出发时间: {i['goTime']}
剩余船票数量: {i['totalRemainVolume']}
详情: {[{seatType['seatTypeName']: seatType['num']}
      for seatType in i['seatList']]}
                """
        all_ticket = header + ticket_info + self._msg_footer
        return all_ticket

    @logger.catch
    def main(self, sail_date):
        self._error = 0
        self._errno = 0
        self._session = requests.Session()
        self._headers = {
            # 必须添加 Content-Type 字段:[x-www-form-urlencoded]
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            "User-Agent": utils.get_random_useragent()
        }
        msg = self._parse_data(self._fetch_data(sail_date))
        ret = self._format_msg(msg, sail_date)
        return 1, ret


report = Report()
