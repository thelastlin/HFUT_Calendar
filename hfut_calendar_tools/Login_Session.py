from .urls import URL
import requests
import hashlib


def get_login_sessions(userinfo: dict):
    login_session = requests.Session()
    salt_res = login_session.get(URL.salt)
    salt_res.raise_for_status()
    login_sha1ed_password = hashlib.sha1(
        ('{0}-{1}'.format(str(salt_res.content, encoding='utf8'), userinfo["password"])).encode('utf8'))
    login_post_json = {
        "username": userinfo["username"],
        "password": login_sha1ed_password.hexdigest(),
        "captcha": ""
    }
    # It will get a 500 when I use session login to System.
    login_step = requests.post(URL.login, cookies=login_session.cookies, json=login_post_json)
    login_step.raise_for_status()
    return login_session
