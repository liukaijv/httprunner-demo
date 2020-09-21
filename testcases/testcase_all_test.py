import pytest
from httprunner import HttpRunner, Step, RunTestCase, Config, Parameters
from .testcase_must_auth_test import TestcaseMustAuth
from .testcase_no_auth_test import TestcaseNoAuth
from .util import parse_cvs_file


def test_parameters_func():
    ret = Parameters({"username": "${parameterize(mobiles.csv)}"})
    a = 2


# 测试所有
@pytest.mark.filterwarnings("ignore: .*Unverified HTTPS.*")
class TestcaseAll(HttpRunner):
    config = (Config("pass"))

    # @pytest.mark.parametrize('params', Parameters({"username": "${parameterize(mobiles.csv)}"}))
    def test_start(self):
        data = parse_cvs_file('mobiles.csv')
        params = {"params": data}
        super().test_start(params)

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
