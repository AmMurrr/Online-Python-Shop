from project_pages.selling_page import show_selling_page
from project_pages.cart_page import show_cart_page
# from project_pages.admin_page import show_admin_page
from project_pages.account_page import show_account_page
import repositories.account
import streamlit as st


import services.cookies

import logging
import log_config

# Admin_ids =[1] # ID всех админов
# st.session_state.is_admin = True
# st.session_state.logged_in = 1


st.set_page_config("TerraVentura",page_icon='random')

def sign_in(username, password):# 
    

    user_id = repositories.account.login(username,password)

    if not user_id:
        logging.info("Проблемы со входом")
        return -1

    if user_id["role"] == "admin":
        logging.info(f"Администратор вошел в аккаунт")
        st.session_state.is_admin = True

    return user_id
    

# def password_hashing(password):
#     salt = bcrypt.gensalt()
#     hashed_password = bcrypt.hashpw(password.encode('utf-8'),salt)
#     logging.info("Пароль захэширован")
#     return hashed_password

# def is_mail_used(mail):
#     mails = repositories.account.get_mails()
#     for mail_item in mails:
#         if mail == mail_item["mail"]:
#             logging.info(f"Пользователь с почтой {mail} уже есть")
#             return True
#     return False

def sign_up(login, mail, password,fullname):
    # if is_mail_used(mail):
    #     logging.info(f"Аккаунт с почтой {mail} уже зарегистрирован")
    #     return -1

    new_user = repositories.account.add_user(login,mail,fullname,password)

    # hashed_password = password_hashing(password)
    # repositories.account.add_hash(new_user_id,hashed_password.decode('utf-8'))
    return new_user

def check_input(login,password, mail):
    logging.info("Проверяем пароль, почту и логин")
    check_counter = 0
    if len(login) >= 3 and not login.isspace():
        check_counter += 1
    if len(mail) >= 5 and mail.find("@") > 0:
        check_counter += 1
    if len(password) > 4 and not password.isdigit():
        check_counter += 1
    
    if check_counter == 3:
        return True
    else:
        return False

@st.dialog("Регистрация")
def signing_up():

    st.write("Введите логин")
    login = st.text_input("  ")
    st.write("Введите почту")
    mail = st.text_input(" ")
    st.write("Введите пароль")
    password = st.text_input("Пароль ",type="password" )
    fullname = st.text_input("Введите своё полное имя")

    if st.button("Подтвердить "):
        if check_input(login,password,mail): 

            valid_user_check = sign_up(login,mail,password,fullname)
            if valid_user_check:
                logging.info(f"Зарегистрирован пользователь ")
                st.session_state.logged_in = valid_user_check["id"]

                user_id = valid_user_check["id"]
                user_role = valid_user_check["role"]

                token = services.cookies.generate_jwt(user_id,user_role) 
                services.cookies.set_cookie("auth_token",token) # creating cookie

                st.rerun()
            else:
                logging.info("Не получилось создать аккаунт")
                st.write("Неправильные данные для аккаунта")
            
            
        else:
            st.write("Некоторые данные некорректно заполнены")


@st.dialog("Вход")
def signing_in():

    st.write("Введите логин")
    login = st.text_input(" ",key = -1)
    st.write("Введите пароль")
    password = st.text_input(" ",key = -2,type="password")

    if st.button(" Подтвердить",):
        valid_user_check = sign_in(login,password)
        if valid_user_check:
            logging.info(f"Пользователь {valid_user_check} вошел в аккаунт")
            st.session_state.logged_in = valid_user_check["id"]

            user_id = valid_user_check["id"]
            user_role = valid_user_check["role"]

            token = services.cookies.generate_jwt(user_id,user_role)
            services.cookies.set_cookie("auth_token",token) # creating cookie

            st.rerun()
        else:
            logging.info("Не удалось войти")
            st.write("Почта или пароль неверны")


if "logged_in" not in st.session_state:
    st.session_state.logged_in = -1    

if "is_admin" not in st.session_state:
    st.session_state.is_admin = False 

if "key" not in st.query_params:
    st.query_params.key="0"

def main():
    st.sidebar.title("TerraVentura")
    # st.sidebar.subheader("Магазин туристического снаряжения")
    st.sidebar.write("Ad astra per aspera!")

    if st.session_state.logged_in < 0 :
        token = services.cookies.get_cookie("auth_token") # check for cookie
        if token:
            user_id, role = services.cookies.verify_jwt(token)
            if user_id:
                logging.info(f"{user_id} Вошёл в аккаунт по куки")
                st.session_state.logged_in = user_id
                st.session_state.is_admin = True if role == "admin" else False
                    

    if st.session_state.logged_in < 0:
        if st.sidebar.button("🔼 Зарегистрироваться"):
            logging.info("Выбрана регистрация")
            signing_up()
        if st.sidebar.button("🔽 Войти"):
            logging.info("Выбран вход")
            signing_in()

    pages = ["Каталог товаров","Корзина","Аккаунт"]
    if "is_admin" in st.session_state and st.session_state.is_admin == True:
        pages.append("Панель Администратора")
    

    page = st.sidebar.radio("Выбранная страница",pages)

    if page == "Каталог товаров":
        logging.info(f"Выбрана страница {page}")
        show_selling_page()
    if page == "Корзина":
        if st.session_state.logged_in > 0:
            logging.info(f"Выбрана страница {page}")
            show_cart_page()
        else:
            st.write("## Войдите в аккаунт")
    if page == "Аккаунт":
        if st.session_state.logged_in > 0:
            logging.info(f"Выбрана страница {page}")
            show_account_page()
        else:
            st.write("## Войдите в аккаунт")
    if page == "Панель Администратора":
            logging.info(f"Выбрана страница {page}")
            show_admin_page()
    
        
            


if __name__=="__main__":
    main()

# ad4fb8d1 - пароль для айди 1

