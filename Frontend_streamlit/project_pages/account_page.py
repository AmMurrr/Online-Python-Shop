# import streamlit as st
# # import repositories.account
# # from services.cookies import set_cookie
# # import bcrypt



# import logging
# import log_config

# # def check_password(password):
# #     hashed_password = repositories.account.get_hash(st.session_state.logged_in) # получаем хэш из БД

# #     if not bcrypt.checkpw(password.encode('utf-8'),hashed_password.encode('utf-8')): # проверка пароля 
# #         logging.info("При изменении пароля пароли не совпали")
# #         return False
# #     logging.info("Пароль совпал!")
# #     return True

# # def password_hashing(password):
# #     salt = bcrypt.gensalt()
# #     hashed_password = bcrypt.hashpw(password.encode('utf-8'),salt)
# #     logging.info("Пароль захэширован")
# #     return hashed_password



# # @st.dialog("Удаление аккаунта")
# # def user_delete():
# #     st.title("Вы уверены, что хотите удалить ваш аккаунт?")
# #     st.write("#### Вы не сможете восстановить его после удаления")

# #     flag = st.checkbox("Я даю своё согласие на удаление своих данных")

# #     if st.button("😱 Подтвердить") and flag:
# #         repositories.account.delete_user(st.session_state.logged_in)
# #         set_cookie("auth_token","0")
# #         st.session_state.logged_in = -1
# #         st.session_state.is_admin = False
# #         st.rerun()

# #     if st.button("😄 Я передумал"):
# #         st.rerun()


# # def log_out():
# #     logging.info(f"{st.session_state.logged_in} вышел из аккаунта")
# #     set_cookie("auth_token","0")
# #     st.session_state.logged_in = -1
# #     st.session_state.is_admin = False
# #     st.rerun()

# # @st.dialog("Обновление пароля")
# # def change_password():
# #     password = st.text_input("### Введите текущий пароль", type="password")
# #     new_password = st.text_input("### Введите новый пароль", type="password")
# #     if st.button("Обновить пароль"):
# #         if check_password(password):
# #             hashed_password = password_hashing(new_password)
# #             repositories.account.change_password(st.session_state.logged_in,hashed_password)
# #             logging.info(f"Пользователь {st.session_state.logged_in} сменил пароль")
# #             st.rerun()
# #         else:
# #             logging.info(f"Пользователь {st.session_state.logged_in} неправильно ввёл пароль")
# #             st.warning("Пароли не совпадают")

# # @st.dialog("Введите новый логин")
# # def change_login():
# #     new_info = st.text_input("   ")
# #     if st.button("Обновить "):
# #         repositories.account.change_login(st.session_state.logged_in, new_info)
# #         st.rerun()
        

# # @st.dialog("Введите новую почту")
# # def change_mail():
# #     new_info = st.text_input("    ")
# #     if st.button("Обновить"):
# #         repositories.account.change_mail(st.session_state.logged_in, new_info)
# #         st.rerun()
        

# def show_account_page():

#     # user_info = repositories.account.get_user_info(st.session_state.logged_in)
#     login = user_info["login"]
#     mail = user_info["mail"]
#     birth_date = user_info["birth_date"]
#     st.title(f"Аккаунт пользователя {login}")

#     cols = st.columns([2,1])

#     with cols[0]:
#         st.write(f"### ID: {st.session_state.logged_in}")
#         st.write(f"### Почта: {mail}")
#         st.write(f"### Дата Рождения: {birth_date}")

#     with cols[1]:

#         if st.button("Изменить логин"):
#             logging.info(f"Изменение логина {st.session_state.logged_in}")
#             change_login()


#         if st.button("Изменить почту"):
#             logging.info(f"Изменение почты {st.session_state.logged_in}")
#             change_mail()

#         if st.button("Изменить пароль"):
#             logging.info(f"Изменение пароля{st.session_state.logged_in}")
#             change_password()


#         if st.button("Выйти из аккаунта"):
#             log_out()

#         st.markdown("---")
#         if "is_admin" in st.session_state and st.session_state.is_admin != True:
#             if st.button("Удалить аккаунт"):
#                 user_delete()
        
