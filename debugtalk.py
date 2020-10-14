import concurrent
import logging
import time
from hashlib import md5
from json import dumps

from httprunner import __version__
from httprunner.response import ResponseObject
import concurrent.futures

import requests
import uuid
from typing import Dict, List


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


def upload_file(file, token) -> Dict:
    file_key = 'dev_test' + uuid.uuid4().hex
    files = {
        "file": open(file, 'rb'),
    }
    resp = requests.post('https://upload-z2.qiniup.com/', data={'token': token, 'key': file_key}, files=files)
    return resp.json()


def multi_upload(files: List, token) -> List:
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:

        upload_futures = {executor.submit(upload_file, f, token): f for f in files}

        uploaded_files: List = []
        for future in concurrent.futures.as_completed(upload_futures):
            f = upload_futures[future]
            try:
                data = future.result()
                if 'key' in data:
                    uploaded_files.append(data['key'])
            except Exception as ex:
                print('上传' + f + '出错了:' + ex)
        return uploaded_files


def build_upload_data(file_keys: List, codes: List):
    post_data = dict()
    post_data['codeList'] = codes
    post_data['infoList'] = [{'uri': uri, 'title': uri, 'type': 1} for uri in file_keys]
    return post_data;


def test_build_upload_img():
    data = build_upload_data(['fafafaf'], [])
    print(data)


def test_multi_upload():
    files = ['demo.png']
    token = 'dmFonkLdUNhfdz9zFjdUOtrK5ktrMt86yic_iEYB:V6pCHKBaBl2q-OgpdnKOJDE-DQc=:eyJzY29wZSI6ImdlbmVyYWxyZXNvdXJjZXMiLCJkZWFkbGluZSI6MTYwMjU4NjY3Nn0='
    ret = multi_upload(files, token)
    print(ret)
