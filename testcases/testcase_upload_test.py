import pytest
from httprunner import HttpRunner, Step, RunRequest
from .util import merge_headers, setup_config


@pytest.mark.filterwarnings("ignore: .*Unverified HTTPS.*")
class TestcaseMustAuth(HttpRunner):
    config = (
        setup_config()
    )

    teststeps = [
        Step(
            RunRequest("获取登录短信验证码")
                .post("/sendMessage")
                .with_headers(**merge_headers())
                .with_json({"type": 1, "mobile": "13982050830"})
                .extract()
                .with_jmespath("body.data.token", "code_token")
                .validate()
                .assert_equal("body.code", 0)
                .assert_not_equal("body.data.token", None)
            # .teardown_hook("${set_sms_code_token($response)}", 'code_token')
        ),
        Step(RunRequest("用户登陆")
             .post("/login")
             .with_headers(**merge_headers())
             .with_json({
            "code": 111111,
            "codeToken": "$code_token",
            "headimgurl": "",
            "mobile": "13982050830",
            "nickname": "",
            "pushId": "",
            "thirdSystemId": "",
            "type": 1,
            "unionid": ""
        })
             .extract()
             .with_jmespath('body.data.token.token', 'auth_token')
             .with_jmespath('body.data.token.usercode', 'usercode')
             .validate()
             .assert_equal("body.code", 0)
             .assert_not_equal("body.data.token.token", None)
             ),
        Step(RunRequest("获取上传token")
             .post("/getQiniuToken")
             .with_headers(**merge_headers())
             .with_json({'type': 1})
             .extract()
             .with_jmespath('body.data', 'qiniu_token')
             .validate()
             .assert_not_equal('body.data', None)
             ),
        Step(RunRequest("测试上传图片")
             .post("https://upload-z2.qiniup.com/")
             .upload(**{
            "file": "demo.png",
            'token': '${qiniu_token}'
        })
             .validate()
             .assert_not_equal('body.hash', None)
             )
    ]


if __name__ == "__main__":
    TestcaseMustAuth().test_start()
