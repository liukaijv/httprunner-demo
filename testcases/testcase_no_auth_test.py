from httprunner import HttpRunner, Step, RunRequest
from .util import setup_config, merge_headers
import pytest


# 不需要登录的接口测试
@pytest.mark.filterwarnings("ignore: .*Unverified HTTPS.*")
class TestcaseNoAuth(HttpRunner):
    config = (setup_config())

    teststeps = [
        Step(
            RunRequest('获取地区')
                .post("/cityNameFuzzySearch")
                .with_headers(**merge_headers())
                .with_json({'cityname': '成都'})
                .validate()
                .assert_equal("body.data.info[0].id", 3334)
        )
    ]


if __name__ == "__main__":
    TestcaseNoAuth().test_start()
