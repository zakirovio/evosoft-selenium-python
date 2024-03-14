from apps.elonmusk.data import (common, confirm_data, check_data, csrf_change_data, domain, headers, flow_data, json_data, login_data,
                                password_data, elon_params)
from config import settings
import json
import requests
import time


def get_auth_tokens():
    """Аутентификация осуществляется в несколько 'flows'"""
    session = requests.session()
    session.get(url="https://twitter.com/i/flow/login", headers=common,
                proxies=settings.requests_proxies
                )  # set guest_id cookie

    # Update gt token
    time.sleep(1)
    guest = session.post(
        "https://api.twitter.com/1.1/guest/activate.json", headers=headers,
        proxies=settings.requests_proxies
    )
    gt = guest.json().get("guest_token")
    headers["x-guest-token"] = gt

    time.sleep(1)
    session.post(
        "https://api.twitter.com/1.1/onboarding/task.json?flow_name=login", headers=headers,
        json=flow_data, proxies=settings.requests_proxies
    )  # set att cookie

    time.sleep(1)
    session.get("https://twitter.com/i/js_inst?c_name=ui_metrics", headers=common,
                proxies=settings.requests_proxies
                )  # set session_id cookie

    time.sleep(1)
    # Auth flows
    task_1 = session.post(
        'https://api.twitter.com/1.1/onboarding/task.json', params={'flow_name': 'login'},
        headers=headers, json=flow_data, proxies=settings.requests_proxies
    )  # init
    flow_token = task_1.json()["flow_token"]
    json_data["flow_token"] = flow_token
    settings.stream_logger.debug(msg=flow_token)

    time.sleep(1)
    task_2 = session.post('https://api.twitter.com/1.1/onboarding/task.json', headers=headers,
                          json=json_data, proxies=settings.requests_proxies
                          )
    flow_token = task_2.json()["flow_token"]
    login_data["flow_token"] = flow_token
    settings.stream_logger.debug(msg=flow_token)

    time.sleep(1)
    task_3 = session.post('https://api.twitter.com/1.1/onboarding/task.json', headers=headers,
                          json=login_data, proxies=settings.requests_proxies
                          )
    flow_token = task_3.json()["flow_token"]
    password_data["flow_token"] = flow_token
    settings.stream_logger.debug(msg=flow_token)

    time.sleep(1)
    task_4 = session.post('https://api.twitter.com/1.1/onboarding/task.json', headers=headers,
                          json=password_data, proxies=settings.requests_proxies
                          )
    flow_token = task_4.json()["flow_token"]
    check_data["flow_token"] = flow_token
    settings.stream_logger.debug(msg=flow_token)

    time.sleep(1)
    task_5 = session.post(
        'https://api.twitter.com/1.1/onboarding/task.json', headers=headers,
        json=check_data, proxies=settings.requests_proxies
    )  # by default set short c0t and auth token, but to be exceptions
    flow_token = task_5.json()["flow_token"]
    settings.stream_logger.debug(msg=flow_token)

    # При попытке войти в профиль с другого прокси, обычно требуется двухфакторка
    if task_5.cookies.get("auth_token") is None:
        confirm_data["flow_token"] = flow_token
        # Нужно будет ввести код из письма, как можно быстрее, так ивент имеет срок годности
        code = input("Введите код подтверждения из письма: ")
        confirm_data["subtask_inputs"][0]["enter_text"]["text"] = code
        confirm_task = session.post(
            "https://api.twitter.com/1.1/onboarding/task.json", headers=headers,
            json=confirm_data, proxies=settings.requests_proxies
        )
        print("OK", confirm_task.cookies.get("c0t"))

    time.sleep(1)
    session.get('https://api.twitter.com/graphql/W62NnYgkgziw9bwyoVht0g/Viewer', params=csrf_change_data,
                headers=headers,proxies=settings.requests_proxies
                )  # set full csrf cookie

    # Update main headers
    headers.update({'x-csrf-token': session.cookies.get("ct0")})
    return session, headers


def parse_json(data: list[dict]):
    for tweet in data:
        if "tweet" in tweet["entryId"] and "promoted" not in tweet["entryId"]:
            legacy = tweet["content"]["itemContent"]["tweet_results"]["result"].get("legacy")
            if legacy:
                text = legacy["full_text"].split("\n")[0].split("https")[0]
                settings.file_logger.info(msg=text)


def get_user_data(s: requests.Session, auth: dict) -> list:
    response = s.get(
        'https://twitter.com/i/api/graphql/eS7LO5Jy3xgmd3dbL044EA/UserTweets',
        params=elon_params,
        headers=auth,
        proxies=settings.requests_proxies
    )
    if settings.WRITE_TO:
        with open("temp.json", 'w', encoding='utf-8') as file:
            json.dump(response.json(), file, indent=4, ensure_ascii=False)

    tweets = response.json()["data"]["user"]["result"]["timeline_v2"]["timeline"]["instructions"][1]["entries"]
    return tweets


def check_proxy():
    r = requests.get(domain, headers=common, proxies=settings.requests_proxies)
    settings.stream_logger.debug(msg=f"PROXY STATUS {r.status_code}")


def main():
    check_proxy()
    s, h = get_auth_tokens()
    raw_data = get_user_data(s, h)
    parse_json(data=raw_data)
