import pandas as pd 
import streamlit as st 
from datetime import date
import repositories.products
from services.recommendations import *
# from repositories.cart import add_to_cart,check_cart_amount
from repositories.recommendations import *

import logging
import log_config

@st.dialog("Добавление товара")
def adding_product():

    category = st.text_input("Тип товара")
    product_title = st.text_input("Название товара")
    brand = st.text_input("Компания-производитель товара")
    price = st.text_input("Цена товара")
    discount = st.text_input("Скидка товара")
    stock = st.text_input("Доступное количество товара")
    description = st.text_input("Описание товара")
    product_image = st.file_uploader("Загрузите изображение товара", type = ["png","jpg","jpeg"])
    
    if st.button("Добавить товар"):
        categories = repositories.products.get_categories()  
        category_id = check_category(categories,category)
        
        if category_id<0:
            category_id = repositories.products.add_category(category)["id"]

        product_id = repositories.products.add_product(category_id,product_title,brand,price,discount,stock,description)["id"]

        rec_id = add_item_to_rec(product_title, category)
        if not rec_id:
            logging.waring("Не добавили товар в рекомендации")
        logging.info(f"Добавили товар {product_id}")

        st.rerun()
    
def check_category(categories,new_category):
    for category in categories:
        if category["name"] == new_category:
            return category["id"]
    return -1

def get_products():
    logging.info("Получаем список товаров")
    return repositories.products.get_products()

def delete_product(product_id):
    logging.info(f"Удаление товара с ID {product_id}")
    repositories.products.remove_from_goods(product_id)
    st.rerun()

# def get_cart_amount(user_id,product_id):
#     cart_amount = check_cart_amount(user_id,product_id) 
    
#     if not cart_amount:
#         logging.info(f"Товара {product_id} нет в корзине {user_id}")
#         return 0
#     else:
#         logging.info(f"Получили количество товара {product_id} в корзине {user_id}")
#         return cart_amount[0]['amount']


# def get_amount(product_id): # получаем количество товара на данный момент
#     return next((row['amount'] for row in st.session_state.products if row["product_id"] == product_id),None)

def product_to_cart(product):
    if product["stock"] == 0:
        st.write("Товар закончился")
        return False

    cart_products = repositories.cart.get_cart_products(st.session_state.logged_in)
    if not cart_products:
        cart_create(st.session_state.logged_in)

    add_to_cart(st.session_state.logged_in,product_id["id"])
    st.session_state.cart_counter += 1
    logging.info(f"Товар {product_id} добавлен в корзину {st.session_state.logged_in}")
    st.write(f"В корзину добавлено {st.session_state.cart_counter} товара")
    

def search_ckeck(search,product_name):  
    if product_name.lower().find(search.lower()) >= 0:
        return True
    else:
        return False

# def tag_check(tag, product_type):
#     if tag == product_type:
#         return True
#     else:
#         return False

# def get_images():
#     logging.info("Получаем изображения товаров")
#     return repositories.media.get_all_images()

# def find_image(product_id,images):
#     for image in images:
#         if image["product_id"] == product_id:
#             return bytes(image["picture"])
#     return None

def find_product(search_product,products):
    for product in products:
        if product["title"] == search_product:
            return product
    return None

@st.dialog("Похожие товары",width="large")
def show_recommendations(name):
    rec_products = get_recommendations(name)

    if not rec_products:
        st.write("Ошибка рекомендаций")

    for rec_product in rec_products:
        recommendation = find_product(rec_product,st.session_state.products)
        if recommendation:
            with st.container(border=True):
                cols = st.columns([1,2])

                with cols[0]:
                    # img = find_image(product["product_id"],products_images)
                    # if img:
                    #     st.image(img)
                    # else:
                    #     logging.info(f"Изображение " + str(product["product_id"]) + " не найдено")
                        st.warning("Изображение не найдено")

                with cols[1]:
                    st.subheader(recommendation["title"])
                    st.write(recommendation["brand"])
                    st.write(recommendation["description"])
                    st.write("#### Цена: " + str(recommendation["price"]) + " ₽")
                    if st.button("В корзину",key=recommendation["id"]+999999):

                        if st.session_state.logged_in > 0:
                            logging.info("Вызвано добавление в корзину")
                            product_to_cart(recommendation)

    if st.button("OK"):
        st.rerun()

if "products" not in st.session_state:
    st.session_state.products = get_products()
 

def show_selling_page():
    st.session_state.products = get_products()
    st.title("Каталог Товаров")
    
    # st.write(st.session_state.products)

    if "cart_counter" not in st.session_state:
        st.session_state.cart_counter = 0

    if "is_admin" in st.session_state and st.session_state.is_admin == True:
        if st.button("+Добавить товар"):
            logging.info("Вызвано добавление товара")
            adding_product()
    
    # tag_options = set([row["type"] for row in st.session_state.products])
    search = st.text_input("🔍 Поиск товара по названию:")
    # tag = st.pills("Тип товара",tag_options)

    # products_images = get_images()
    k = 0
    for product in st.session_state.products:
        # k+=1

        # if k == 30:
        #     break
        if not search.isspace() or len(search) > 3:
            if not search_ckeck(search, product["title"]):
                continue
        
        # if tag:
        #     if not tag_check(tag,product["type"]):
        #         continue

        with st.container(border=True):
            cols = st.columns([1,2])

            with cols[0]:
                # img = find_image(product["product_id"],products_images)
                # if img:
                #     st.image(img)
                # else:
                #     logging.info(f"Изображение " + str(product["product_id"]) + " не найдено")
                    st.warning("Изображение не найдено")

            with cols[1]:
                st.subheader(product["title"])
                st.write(product["brand"])
                st.write(product["description"])
                st.write("#### Цена: " + str(product["price"]) + " ₽")
                if st.button("В корзину",key=product["id"]):

                    if st.session_state.logged_in > 0:
                        logging.info("Вызвано добавление в корзину")
                        product_to_cart(product)
                        show_recommendations(product["title"])
                    else:
                        logging.info("You have no power here!")
                        st.write("Войдите в аккаунт или зарегистрируйтесь для покупки")

                if "is_admin" in st.session_state and st.session_state.is_admin == True:
                    if st.button("❌ Убрать товар", key = "del_" + str(product["id"])):
                        logging.info("Удаляем товар")
                        delete_product(product["id"])

                

