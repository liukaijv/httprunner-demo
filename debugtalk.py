import logging
import time
from hashlib import md5
from json import dumps

from httprunner import __version__
from httprunner.response import ResponseObject


def get_httprunner_version():
    return __version__


def sleep(n_secs):
    time.sleep(n_secs)


# 生成签名
def generate_sign(timestamp, secret_key="3L9CJddHs@M2zbl3S6@e44KE6EXcwHPL", token="", usercode=""):
    if token != "":
        return md5(
            ("timestamp:" + timestamp + ";usercode:" + usercode + ";fixedstring:" + secret_key + ";token:" + token)
                .encode("utf-8")).hexdigest()
    return md5(("timestamp:" + timestamp + ";fixedstring:" + secret_key).encode("utf-8")).hexdigest()


# test_generate_sign
def test_generate_sign():
    timestamp = '1598508289'
    sign = generate_sign(timestamp)
    logging.info("sign: " + sign)


def set_sms_code_token(response: ResponseObject):
    res_data = response.resp_obj.json()
    logging.info('set_token' + dumps(res_data))

    if res_data['code'] == 0 and res_data['data']:
        return res_data['data']['token']
    return ''


# test setup_hook
def setup_hook():
    logging.info("setup_hook")
    pass
