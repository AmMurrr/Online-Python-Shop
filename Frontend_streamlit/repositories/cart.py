
from repositories.api_connection import *
from datetime import date


CARTS_API_URL = "http://127.0.0.1:8050/carts/"

# def remove_from_cart(user_id,product_id):
#     query = """
#         DELETE FROM cart
#         WHERE user_id = %s AND product_id = %s
#     """
#     return execute_query(query,(user_id, product_id))

# def take_from_cart(user_id, product_id):
#     query = """
#         UPDATE cart
#         SET amount = cart.amount - 1
#         WHERE user_id = %s AND product_id = %s
#     """

#     return execute_query(query,(user_id, product_id))

def add_to_cart(user_id, product_id):
    data = ""
    answer = send_post(f"{CARTS_API_URL}{data}")
    answer_json = answer.json()
    return answer_json


def cart_create(user_id):
    
    data = f"?user_id={user_id}"
    json_data ={"cart_items": []
    }
    headers = {"Content-Type": "application/json"}
    answer = send_post(f"{CARTS_API_URL}{data}",json_data=json_data,headers=headers)
    answer_json = answer.json()
    return answer_json

# def check_cart_amount(user_id,product_id):
#     query = """
#     SELECT amount FROM cart WHERE user_id = %s AND product_id = %s
#     """
#     return execute_query(query,(user_id,product_id),True)

def get_cart_products(user_id):
    answer = send_get(f"{CARTS_API_URL}{user_id}")
    if not answer:
        return None
    answer_json = answer.json()
    return answer_json["new_item_id"]

# def clear_cart(user_id):
#     query = """
#     DELETE FROM cart WHERE user_id = %s
#     """
#     return execute_query(query,(user_id,))