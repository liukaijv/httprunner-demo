import pytest
from httprunner import HttpRunner, Step, RunTestCase, Config
from .testcase_must_auth_test import TestcaseMustAuth
from .testcase_no_auth_test import TestcaseNoAuth


# 测试所有
@pytest.mark.filterwarnings("ignore: .*Unverified HTTPS.*")
class TestcaseAll(HttpRunner):
    config = (Config("pass"))

    teststeps = [
        Step(
            RunTestCase("登录相关")
                .call(TestcaseMustAuth)
        ),
        Step(
            RunTestCase("未登录相关测试")
                .call(TestcaseNoAuth)
        )
    ]


if __name__ == "__main__":
    TestcaseAll.test_start()
