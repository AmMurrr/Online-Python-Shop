# from repositories.db_connection import execute_query
import requests

PRODUCTS_API_URL = "http://127.0.0.1:8060/products/"
CATEGORY_API_URL = "http://127.0.0.1:8000/categories/"


def add_product(category,product_title,brand,price,discount,stock,description):
    request = requests.post(f"{PRODUCTS_API_URL}")
    answer = request.json()
    #  answer.pop("message")  
    return answer     

def get_products():
    request = requests.get(f"{PRODUCTS_API_URL}")
    answer = request.json()
    
    return answer["data"]

# def remove_from_goods(product_id):
#     query = """
#         DELETE FROM goods WHERE product_id = %s
#     """
#     return execute_query(query,(product_id,))


# def get_product_name(product_id):
#     query = """
#         SELECT product_name FROM goods WHERE product_id = %s
#     """
#     return execute_query(query,(product_id,),True)[0]["product_name"]


