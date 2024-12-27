# from repositories.db_connection import execute_query
import requests
from repositories.api_connection import *
from datetime import datetime

PRODUCTS_API_URL = "http://127.0.0.1:8060/products/"
CATEGORY_API_URL = "http://127.0.0.1:8060/categories/"


def add_product(category_id,product_title,brand,price,discount,stock,description):


    data = {
        "title": product_title,
        "description": description,
        "price": price,
        "discount_percentage": int(discount),
        "stock": stock,
        "brand": brand,
        "images": [
        "string"
    ],
        "created_at": datetime.now().isoformat(),
        "category_id": category_id
    } 

    headers = {"Content-Type": "application/json"}
    answer = send_post(PRODUCTS_API_URL,json_data=data, headers=headers)
    answer_json = answer.json()
    return answer_json["data"]

# def get_products():
#     request = requests.get(f"{PRODUCTS_API_URL}")
#     answer = request.json()
    
#     return answer["data"]

def get_products():
    answer = send_get(PRODUCTS_API_URL)
    answer_json = answer.json()
    return answer_json["data"]


def get_categories():
    answer = send_get(CATEGORY_API_URL)
    answer_json = answer.json()
    return answer_json["data"]


def add_category(category):
    data = {
        "name": category
    }

    answer = send_post(CATEGORY_API_URL,data)
    answer_json = answer.json()
    return answer_json["data"]

def remove_from_goods(product_id):
    answer = send_delete(f"{PRODUCTS_API_URL}{product_id}")
    answer_json = answer.json()
    return answer_json["data"]


# def get_product_name(product_id):
#     query = """
#         SELECT product_name FROM goods WHERE product_id = %s
#     """
#     return execute_query(query,(product_id,),True)[0]["product_name"]


