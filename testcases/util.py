import time
from math import floor
from typing import Dict
from httprunner import Config
from .config import BASE_URL


# 一些工具方法

def merge_dict(dict_1, *dict_n):
    temp = {**dict_1}
    for item in dict_n:
        temp = {**temp, **item}
    return temp


def test_merge_dict():
    dict_1 = {"a": 1}
    dict_2 = {"b": 2}
    out_dict = merge_dict(dict_1, dict_2)
    assert out_dict["a"] == 1
    assert out_dict["b"] == 2


def merge_headers(data: Dict = {}) -> Dict:
    return merge_dict({
        "Content-Type": "application/json",
        "timestamp": '$now_timestamp',
        "sign": "${generate_sign($now_timestamp,$secret_key,$auth_token,$usercode)}",
        "token": "$auth_token"
    }, data)


def setup_config() -> Config:
    now_timestamp = str(floor(time.time()))

    return Config("pass").variables(**{
        "now_timestamp": now_timestamp,
        "code_token": "",
        "secret_key": '*LCJK1JHs@M2zbl3S6@essKE6EXcwHPL',
        "auth_token": '',
        "usercode": '',
    }).base_url(BASE_URL).verify(False)
