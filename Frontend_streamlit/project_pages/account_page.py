import streamlit as st
import repositories.account
from services.cookies import set_cookie




import logging
import log_config





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


def log_out():
    logging.info(f"{st.session_state.logged_in} вышел из аккаунта")
    set_cookie("auth_token","0")
    st.session_state.logged_in = -1
    st.session_state.is_admin = False
    st.rerun()


        

def show_account_page():

    user_info = repositories.account.get_user_info(st.session_state.logged_in)
    login = user_info["username"]
    mail = user_info["email"]
    fullname = user_info["full_name"]
    st.title(f"Аккаунт пользователя {login}")

    cols = st.columns([2,1])

    with cols[0]:
        st.write(f"### ID: {st.session_state.logged_in}")
        st.write(f"### Почта: {mail}")
        st.write(f"### Имя: {fullname}")

    with cols[1]:


        if st.button("Выйти из аккаунта"):
            log_out()

        st.markdown("---")
        if "is_admin" in st.session_state and st.session_state.is_admin != True:
            if st.button("Удалить аккаунт"):
                user_delete()
        
