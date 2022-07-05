from datetime import datetime
from time import sleep, time
from common.utils import utils
from common.logger import logger
from common.config import config
from common.account import account
from common.report import report
from common.push import push


class Service:
    @logger.catch
    def __init__(self):
        self._str_now_time = "0.1"
        self._account_cnt = account.row
        self._email_switch = None
        self._timer_switch = None
        self._all_departure_date = None
        self._all_date_ticket_info = None
        self.fetch_param()

    @logger.catch
    def fetch_param(self):
        self._email_switch = config.config('/setting/push/email/switch', utils.get_call_loc())
        self._timer_switch = config.config('/setting/timer/switch', utils.get_call_loc())
        logger.debug("Fetched [ReportService] params.")

    @logger.catch
    def _get_now_time(self):
        now = datetime.now()
        self._str_now_time = now.strftime("%H.%M")
        return self._str_now_time

    @logger.catch
    def _sort_departure_date(self):
        self._all_departure_date = []
        for i in range(self._account_cnt):
            self._all_departure_date.append(account.sail_date(i))
        self._all_departure_date = list(set(self._all_departure_date))

    @logger.catch
    def _task1(self):
        """
        出发日期分类，并按分类日期查询
        """
        self._sort_departure_date()
        self._all_date_ticket_info = {}
        dates_num = len(self._all_departure_date)
        for i in range(dates_num):
            log_info = f"[{i + 1}/{dates_num}] Checking date:{self._all_departure_date[i]}".center(46, '-')
            logger.info(log_info)
            ret = report.main(self._all_departure_date[i])
            self._all_date_ticket_info[self._all_departure_date[i]] = ret
            sleep(1)
        logger.info("Tickets info for all dates are checked.")

    @logger.catch
    def _task2(self):
        """
        分类日期群发通知
        """
        all_date_userid = {}
        for i in self._all_departure_date:
            all_date_userid[i] = ""
        for i in range(self._account_cnt):
            all_date_userid[account.sail_date(i)] += f"|{account.userid(i)}"
        for i in range(len(self._all_departure_date)):
            log_info = f"[{i + 1}/{len(self._all_departure_date)}] Date:{self._all_departure_date[i]}".center(46, '-')
            logger.info(log_info)
            all_date_userid[self._all_departure_date[i]] = all_date_userid[self._all_departure_date[i]][1:]
            push.push(self._all_date_ticket_info[self._all_departure_date[i]], "Hi", account.wechat_push(i),
                      account.email_push(i), account.sendkey(i),
                      all_date_userid[self._all_departure_date[i]], account.email(i))
            sleep(0.5)

    @logger.catch
    def _gen(self):
        start_time = time()
        if self._account_cnt == 0:
            logger.error("Account does not exist.")
        else:
            if self._email_switch == "on":
                push.bot_email.login()
            self._task1()
            self._task2()
        end_time = time()
        cost = f"{(end_time - start_time):.2f}"
        logger.info(f"Reports are completed. Cost time:{cost}(s)".center(50, '-'))

    @logger.catch
    def start(self):
        if self._timer_switch == "on":
            logger.info("Timer is enabled.")
            while True:
                config.refresh()
                str_set_time = str(config.config('/setting/timer/set_time', utils.get_call_loc()))
                str_now_time = self._get_now_time()
                logger.info(f"Now time:{str_now_time}. Set time:{str_set_time}.")
                while True:
                    config.refresh()
                    if str_set_time != str(config.config('/setting/timer/set_time', utils.get_call_loc())):
                        str_set_time = str(config.config('/setting/timer/set_time', utils.get_call_loc()))
                        logger.info(f"New set time:{str_set_time}.")
                    str_now_time = self._get_now_time()
                    if str_now_time != str_set_time:
                        sleep(1)
                    else:
                        logger.info("Time arrived. Start to report.")
                        account.refresh()
                        utils.refresh_param()
                        self._gen()
                        # avoid running twice in 1 minute
                        logger.info("Cleaning... Estimated:1 min")
                        sleep(60)
                        break
        else:
            logger.info("Timer is disabled.")
            logger.info("Start to report.")
            self._gen()


service = Service()
