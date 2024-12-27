from repositories.api_connection import *

REC_API_URL = "http://127.0.0.1:8100/rec/"


def  get_recommendations(name):
    answer = send_get(f"{REC_API_URL}{name}")
    answer_json = answer.json()
    return answer_json["same_filter_recommendations"]

def add_item_to_rec(name, category):
    data = f"?item_name={name}&item_category={category}"
    answer = send_post(f"{REC_API_URL}{data}")
    answer_json = answer.json()
    return answer_json["new_item_id"]