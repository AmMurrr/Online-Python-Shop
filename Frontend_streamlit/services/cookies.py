import jwt
from http.cookies import SimpleCookie
import streamlit as st
import datetime

import logging
import log_config


SECRET_KEY = "YOUR_SECRET_KEY"

def generate_jwt(user_id,role):
    expiration = datetime.timedelta(days=30)
    payload = {
        "user_id": user_id,
        "role": role,
        "exp": datetime.datetime.utcnow() + expiration,
        "iat":  datetime.datetime.utcnow()
    }
    logging.info(f"Создан jwt для {user_id}")
    return jwt.encode(payload,SECRET_KEY,algorithm="HS256")

def set_cookie(key, value):
    st.query_params.key = value
    logging.info("Установили куки")

def get_cookie(key):

    cookie_str = st.query_params.key
    if cookie_str:

        return cookie_str
    logging.warning("Не получили куки")
    return None
    
def verify_jwt(token):
    try:
        payload = jwt.decode(token, SECRET_KEY,algorithms=["HS256"])
        return payload['user_id'], payload['role']
    except jwt.ExpiredSignatureError:
        logging.info("Токен просрочен")
    except jwt.InvalidTokenError:
        logging.warning("Недействительный токен")
    except:
        logging.error("Возникла проблема при получении куки")
    return None, None


