# import streamlit as st 
# import repositories.cart
# from services.sales import SaleService
# from datetime import date
# from repositories.media import get_image

# import logging
# import log_config

# @st.cache_data
# def find_product_by_id(product_id,products):
#     for product in products:
#         if product["product_id"] == product_id:
#             return product
#     return None

# def get_cart_products():
#     logging.info(f"Получаем товары в корзине пользователя {st.session_state.logged_in}")
#     return repositories.cart.get_cart_products(st.session_state.logged_in)

# def cart_clearing():
#     logging.info(f"Чистка корзины пользователя {st.session_state.logged_in}")
#     repositories.cart.clear_cart(st.session_state.logged_in)

# def create_sale(cart_products,total_cost):
#     sale_date = date.today()
#     sale_id = SaleService.process_sale(st.session_state.logged_in, cart_products,sale_date,total_cost)
#     return sale_id

# def update_cart_product(product_id,change):
#     user_id = st.session_state.logged_in
#     match change:
#         case 1:
#             logging.info(f"Увеличиваем количество товара {product_id} в корзине пользователя {user_id}")
#             repositories.cart.add_to_cart(user_id,product_id)
#         case -1:
#             logging.info(f"Уменьшаем количество товара {product_id} в корзине пользователя {user_id}")
#             repositories.cart.take_from_cart(user_id,product_id)
#         case 0:
#             logging.info(f"исключаем товар {product_id} из корзины пользователя {user_id}")
#             repositories.cart.remove_from_cart(user_id,product_id)


# def get_product_image(product_id):
#     image = get_image(product_id)
    
#     if image:
#         logging.info(f"Получили изображение товара {product_id}")
#         return bytes(image[0]["picture"])
#     else:
#         logging.info(f"Изображение товара {product_id} не найдено")
#         return None

# @st.dialog("Покупка прошла успешно!")
# def success_sale(sale_id):
#     st.header("Спасибо, что выбрали наш онлайн-магазин!")
#     st.success(f"Ваш чек №{sale_id}")
#     st.balloons()
#     if st.button("Закрыть"):
#         st.rerun()

# def show_cart_page():
#     st.title("🛒 Корзина товаров")
#     total_cost = 0

#     # Получаем данные о товарах в корзине
#     cart_products = get_cart_products()

#     if not cart_products:
#         st.write("Ваша корзина пуста.")
#         return

#     # Отображаем товары в корзине
#     for item in cart_products:
#         with st.container(border=True):
#             product_id = item["product_id"]
#             amount = item["amount"]
#             product = find_product_by_id(product_id,st.session_state.products)
#             if not product:
#                 st.warning(f"Товар с ID {product_id} не найден в каталоге")
#                 continue

#             product_name = product["product_name"]
#             cost = product["cost"]
#             stored_amount = product["amount"]
#             product_image = get_product_image(product_id)

#             total_cost += cost * amount

#             col1, col2, col3 = st.columns([1, 3, 1])

#             with col1:
#                 # Загружаем и отображаем изображение товара
#                 if product_image:
#                     st.image(product_image)
#                 else:
#                     st.warning("Изображение не найдено")

#             with col2:
#                 # Информация о товаре
#                 st.subheader(product_name)
#                 st.write(f"Цена: {cost} ₽")
#                 st.write(f"Количество: {amount}")


#                 # Кнопки для изменения количества
#                 if st.button("➖ Уменьшить", key=f"decrease-{product_id}"):
#                     if amount > 1:
#                         update_cart_product( product_id, -1)
#                     else:
#                         update_cart_product( product_id, 0) 
#                     st.rerun()

#                 if st.button("➕ Увеличить", key=f"increase-{product_id}"):
#                     if stored_amount - amount > 0:
#                         update_cart_product( product_id, 1)
#                         st.rerun()
#                     else:
#                         st.warning("Превышено число товара на складе")

#             with col3:
#                 # Кнопка удаления товара
#                 if st.button("❌ Удалить", key=f"delete-{product_id}"):
#                     update_cart_product( product_id, 0)
#                     st.rerun()

#     # Общая стоимость корзины
#     st.write(f"### Общая стоимость: {total_cost} ₽")
#     sale_btn = st.button("Купить")
#     # оформелние? 
#     if sale_btn:
#         logging.info("Инициализация покупки")
#         sale_id = create_sale(cart_products,total_cost)
#         if sale_id != -1: 
#             cart_clearing()
#             logging.info(f"Покупка {sale_id} прошла успешно!")
#             success_sale(sale_id)
#         else:
#             logging.info("Покупка не прошла")
#             st.warning("Проблемы с оформлением покупки. Пожалуйста попробуйте позже.")