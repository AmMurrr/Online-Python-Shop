import requests

from repositories.api_connection import *

ACCOUNTS_API_URL = "http://127.0.0.1:8080/me/"
AUTH_API_URL = "http://127.0.0.1:8080/auth/"
USERS_API_URL = "http://127.0.0.1:8080/users/"


def add_user(login,mail,fullname, password):
    data = {
        "full_name": fullname,
        "username": login,
        "email": mail,
        "password": password
    }

    headers = {"Content-Type": "application/json"}
    answer = send_post(USERS_API_URL,json_data=data, headers=headers)
    answer_json = answer.json()
    return answer_json["data"]

def login(username,password):
    data = f"login?username={username}&password={password}"
    answer = send_post(f"{AUTH_API_URL}{data}")
    answer_json = answer.json()
    return answer_json["data"]


def get_user_info(user_id):

    answer = send_get(f"{ACCOUNTS_API_URL}?user_id={user_id}")
    answer_json = answer.json()
    return answer_json["data"]