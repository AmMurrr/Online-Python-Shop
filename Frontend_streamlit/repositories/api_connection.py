import requests
from requests.exceptions import HTTPError
from typing import Any, Dict, Optional

import logging
import log_config

def send_get(url: str, params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> requests.Response:
    """
    Отправляет GET-запрос.

    :param url: URL для запроса
    :param params: Параметры запроса (query params)
    :param headers: Заголовки запроса
    :return: Ответ от сервера (Response)
    """
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        return response
    except HTTPError as he:
        if he.response.status_code == 404:
            return None
    except requests.RequestException as e:
        print(f"GET запрос не выполнен: {e}")
        raise

def send_post(url: str, json_data: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> requests.Response:
    """
    Отправляет POST-запрос.

    :param url: URL для запроса
    :param json_data: JSON-данные для отправки в теле запроса
    :param headers: Заголовки запроса
    :return: Ответ от сервера (Response)
    """
    try:
        response = requests.post(url, json=json_data, headers=headers)
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        print(f"POST запрос не выполнен: {e}")
        raise

def send_put(url: str, json_data: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> requests.Response:
    """
    Отправляет PUT-запрос.

    :param url: URL для запроса
    :param json_data: JSON-данные для отправки в теле запроса
    :param headers: Заголовки запроса
    :return: Ответ от сервера (Response)
    """
    try:
        response = requests.put(url, json=json_data, headers=headers)
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        print(f"PUT запрос не выполнен: {e}")
        raise

def send_delete(url: str, params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> requests.Response:
    """
    Отправляет DELETE-запрос.

    :param url: URL для запроса
    :param params: Параметры запроса (query params)
    :param headers: Заголовки запроса
    :return: Ответ от сервера (Response)
    """
    try:
        response = requests.delete(url, params=params, headers=headers)
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        print(f"DELETE запрос не выполнен: {e}")
        raise