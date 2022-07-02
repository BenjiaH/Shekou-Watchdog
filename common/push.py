import json
import smtplib
import requests
import os

from copy import deepcopy
from retrying import retry
from datetime import datetime
from email.mime.text import MIMEText
from common.config import config
from common.logger import logger
from common.utils import utils


class Email:
    @logger.catch
    def __init__(self, mail_user, mail_host, mail_pwd):
        self._email_tmpl_path = None
        self.fetch_param()
        self._mail_host = mail_host
        self._mail_user = mail_user
        self._mail_name = self._mail_user.split("@")[0]
        self._mail_pwd = mail_pwd
        self._is_login = False
        self.smtp = 0
        self._mail_payload = ""

    @logger.catch
    def fetch_param(self):
        self._email_tmpl_path = config.config('/config/path/email_tmpl', utils.get_call_loc())
        logger.debug("Fetched [Push.Email] params.")

    @logger.catch
    def _load_tmpl(self):
        os.chdir(os.path.dirname(__file__))
        with open(self._email_tmpl_path, "r", encoding="utf-8") as f:
            self._mail_payload = f.read()
            logger.debug(f'Loaded [{os.path.abspath(r"../res/email_tmpl.html")}]')

    @logger.catch
    def login(self):
        self._load_tmpl()
        try:
            smtp = smtplib.SMTP_SSL(self._mail_host, 465, timeout=20)
            smtp.login(self._mail_user, self._mail_pwd)
            self._is_login = True
            logger.info("Successful to login the email.")
        except Exception as e:
            logger.error(f"Failed to login the email. [{e}]")
        self.smtp = smtp

    @retry(stop_max_attempt_number=3, wait_fixed=500)
    def send(self, uid, title, msg, receiver: list):
        logger.debug(f"Email receiver:{receiver[0]}.")
        if not self._is_login:
            logger.error("Failed to send the email.[Email not login]")
            self.login()
            raise Exception("Failed to send the email.")
        else:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            mail_msg = self._mail_payload.format(uid=uid, msg=msg, mail_name=self._mail_name, time=now)
            message = MIMEText(mail_msg, "html", "utf-8")
            message['Subject'] = title
            message['From'] = f"{self._mail_name} <{self._mail_user}>"
            message['To'] = receiver[0]
            try:
                self.smtp.sendmail(self._mail_user, receiver, message.as_string())
                logger.info("Successful to send the email.")
            except Exception as e:
                logger.error(f"Failed to send the email.[{e}]")
                logger.error("Retry to send the email.")
                self._is_login = False
                self.login()
                raise Exception("Failed to send the email.")


class Push:
    @logger.catch
    def __init__(self):
        self._wechat_switch = None
        self._email_switch = None
        self._bot_email_user = None
        self._bot_email_host = None
        self._bot_email_pwd = None
        self._errno_msg = None
        self._wechat_v1_url = None
        self._wechat_v2_url = None
        self._wechat_v3_url = None
        self._push_content_existed = None
        self._push_content_success = None
        self._push_content_failed = None
        self._push_content_error = None
        self._wechat_v = None
        self.fetch_param()
        if self._email_switch == "on":
            self.bot_email = Email(self._bot_email_user, self._bot_email_host, self._bot_email_pwd)
            logger.debug("Email is enabled")
        else:
            logger.debug("Email is disabled")

    @logger.catch
    def fetch_param(self):
        self._wechat_switch = config.config('/setting/push/wechat/switch', utils.get_call_loc())
        self._email_switch = config.config('/setting/push/email/switch', utils.get_call_loc())
        self._bot_email_user = config.config('/setting/push/email/bot_email/email_user', utils.get_call_loc())
        self._bot_email_host = config.config('/setting/push/email/bot_email/email_host', utils.get_call_loc())
        self._bot_email_pwd = config.config('/setting/push/email/bot_email/email_pwd', utils.get_call_loc())
        self._errno_msg = config.config('/config/errmsg', utils.get_call_loc())
        self._wechat_v1_url = config.config('/config/push_url/wechat_v1', utils.get_call_loc())
        self._wechat_v2_url = config.config('/config/push_url/wechat_v2', utils.get_call_loc())
        self._wechat_v3_url = config.config('/setting/push/wechat/api', utils.get_call_loc())
        self._push_content_existed = config.config('/config/push_content/existed', utils.get_call_loc())
        self._push_content_success = config.config('/config/push_content/success', utils.get_call_loc())
        self._push_content_failed = config.config('/config/push_content/failed', utils.get_call_loc())
        self._push_content_error = config.config('/config/push_content/error', utils.get_call_loc())
        self._wechat_v = config.config('/setting/push/wechat/version', utils.get_call_loc())
        logger.debug("Fetched [Push] params.")

    def _wechat(self, uid, title, message, sendkey, userid=""):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ps = ""
        space = " " * 18
        msg_title = f'{space}{title}'
        msg_content = f'\n\n{uid}:\n\n{" " * 0}{message}\n{ps}\n\n{now}'
        if self._wechat_v == 1:
            logger.debug("Use WeChat V1 push method.")
            url = f'{self._wechat_v1_url}/{sendkey}.send'
            payload = {
                "text": title,
                "desp": msg_content
            }
            self._wechat_v1(url, payload)
        elif self._wechat_v == 2:
            logger.debug("Use WeChat V2 push method.")
            url = f'{self._wechat_v2_url}/{sendkey}.send'
            payload = {
                "title": title,
                "desp": msg_content
            }
            self._wechat_v2(url, payload)
        elif self._wechat_v == 3:
            logger.debug("Use WeChat V3 push method.")
            url = self._wechat_v3_url
            payload = {
                "sendkey": sendkey,
                "msg_type": "text",
                "msg": msg_title + msg_content,
                "to_user": userid
            }
            self._wechat_v3(url, payload)
        else:
            logger.error(f"Failed to push the WeChat message. [Version error]")

    @retry(stop_max_attempt_number=3, wait_fixed=500)
    def _wechat_v1(self, url, payload):
        res = requests.get(url=url, params=payload)
        log_url = f"{self._wechat_v1_url}/*******.send"
        logger.debug(f"URL:{log_url}. Payload:{payload}. Status code:{res.status_code}")
        res.encoding = "utf-8"
        logger.debug(f"Response:{res.text.rstrip()}")
        dict_res = json.loads(res.text)
        if "errno" in dict_res.keys():
            dict_res["code"] = dict_res.pop("errno")
        if res.status_code != 200 or dict_res["code"] != 0:
            logger.error(f"Failed to push the WeChat message. Status code:{res.status_code}.")
            logger.error("Retry to push the WeChat message.")
            raise Exception("Failed to push the WeChat message.")
        else:
            logger.info("Successful to push the WeChat message.")

    @retry(stop_max_attempt_number=3, wait_fixed=500)
    def _wechat_v2(self, url, payload):
        res = requests.post(url=url, params=payload)
        logger.debug(f'real url :{url}')
        log_url = f'{self._wechat_v2_url}/*******.send'
        logger.debug(f"URL:{log_url}. Payload:{payload}. Status code:{res.status_code}")
        res.encoding = "utf-8"
        logger.debug(f"Response:{res.text.rstrip()}")
        dict_res = json.loads(res.text)
        if res.status_code != 200 or dict_res["code"] != 0:
            logger.error(f"Failed to push the WeChat message. Status code:{res.status_code}.")
            logger.error("Retry to push the WeChat message.")
            raise Exception("Failed to push the WeChat message.")
        else:
            logger.info("Successful to push the WeChat message.")

    @staticmethod
    @retry(stop_max_attempt_number=3, wait_fixed=500)
    def _wechat_v3(url, payload):
        # go_scf V2.0 请求必须为post，且body必须为json
        # 详见文档:https://github.com/riba2534/wecomchan/tree/main/go-scf#%E4%BD%BF%E7%94%A8-post-%E8%BF%9B%E8%A1%8C%E8%AF%B7%E6%B1%82
        log_payload = deepcopy(payload)
        res = requests.post(url=url, data=json.dumps(payload))
        log_payload["sendkey"] = "*******"
        logger.debug(f"URL:{url}. Payload:{log_payload}. Status code:{res.status_code}")
        res.encoding = "utf-8"
        logger.debug(f"Response:{res.text}")
        dict_res = json.loads(res.text)
        if res.status_code != 200 or dict_res["code"] != 0:
            logger.error(f"Failed to push the WeChat message. Status code:{res.status_code}.")
            logger.error("Retry to push the WeChat message.")
            raise Exception("Failed to push the WeChat message.")
        else:
            logger.info("Successful to push the WeChat message.")

    @logger.catch
    def push(self, result, uid, user_wechat_push, user_email_push, sendkey="", userid="", email_rxer=""):
        errno = result[0]
        msg = result[1]
        if errno == 0:
            title = self._push_content_success["title"]
            message = self._push_content_success["message"] + msg
        else:
            title = self._push_content_error["title"]
            errmsg = [i["msg"] for i in self._errno_msg if errno == i["errno"]][0]
            message = f'{self._push_content_error["message"]}[错误信息:"{errmsg}"]'
        logger.debug(f"Title:{title}#Message:{message}#Error code:{errno}")
        if self._wechat_switch == "on":
            if user_wechat_push == "1":
                try:
                    self._wechat(uid, title, message, sendkey, userid)
                except Exception as e:
                    logger.error(e)
        if self._email_switch == "on":
            if user_email_push == "1":
                try:
                    self.bot_email.send(uid, title, message, [email_rxer])
                except Exception as e:
                    logger.error(e)


push = Push()
