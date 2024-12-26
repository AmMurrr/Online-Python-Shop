import pandas as pd 
import streamlit as st 
from datetime import date
import repositories.products
# from repositories.cart import add_to_cart,check_cart_amount
# import repositories.media 

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
        product_id = repositories.products.add_product(category,product_title,brand,price,discount,stock,description)
        logging.info(f"Добавили товар {product_id}")

        if product_image is not None:
            img_bytes = product_image.read()
            logging.info("Добавляем изображение нового товара")
            repositories.media.add_media(product_id,img_bytes)
        st.rerun()
    


def get_products():
    logging.info("Получаем список товаров")
    return repositories.products.get_products()

# def delete_product(product_id):
#     logging.info(f"Удаление товара с ID {product_id}")
#     repositories.products.remove_from_goods(product_id)
#     st.rerun()

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

# def product_to_cart(product_id):
#     product_amount = get_amount(product_id)
#     logging.info(f"Товара {product_id} на складе {product_amount}")

#     if product_amount == 0:
#         st.write("Товар закончился")
#         return False
#     cart_amount = get_cart_amount(st.session_state.logged_in, product_id)
#     if product_amount - cart_amount > 0:
#         add_to_cart(st.session_state.logged_in,product_id)
#         st.session_state.cart_counter += 1
#         logging.info(f"Товар {product_id} добавлен в корзину {st.session_state.logged_in}")
#         st.write(f"В корзину добавлено {st.session_state.cart_counter} товара")
#     else:
#         st.warning("Больше товара на складе нет!")

# def search_ckeck(search,product_name):  
#     if product_name.lower().find(search.lower()) >= 0:
#         return True
#     else:
#         return False

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

if "products" not in st.session_state:
    st.session_state.products = get_products()
 

def show_selling_page():
    st.session_state.products = get_products()
    st.title("Каталог Товаров")
    
    st.write(st.session_state.products)

    if "cart_counter" not in st.session_state:
        st.session_state.cart_counter = 0

    if "is_admin" in st.session_state and st.session_state.is_admin == True:
        if st.button("+Добавить товар"):
            logging.info("Вызвано добавление товара")
            adding_product()
    
    # tag_options = set([row["type"] for row in st.session_state.products])
    # search = st.text_input("🔍 Поиск товара по названию:")
    # tag = st.pills("Тип товара",tag_options)

    # products_images = get_images()

    for product in st.session_state.products:

        # if not search.isspace() or len(search) > 3:
        #     if not search_ckeck(search, product["product_name"]):
        #         continue
        
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
                if st.button("В корзину",key=product["product_id"]):

                    if st.session_state.logged_in > 0:
                        logging.info("Вызвано добавление в корзину")
                        product_to_cart(product["product_id"])
                    else:
                        logging.info("You have no power here!")
                        st.write("Войдите в аккаунт или зарегистрируйтесь для покупки")

                if "is_admin" in st.session_state and st.session_state.is_admin == True:
                    if st.button("❌ Убрать товар", key = "del_" + str(product["product_id"])):
                        logging.info("Удаляем товар")
                        delete_product(product["product_id"])

                

