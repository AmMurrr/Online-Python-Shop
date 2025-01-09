from sqlalchemy.orm import Session
import pandas as pd
import numpy as np
from sklearn.linear_model import Ridge
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from scipy.optimize import minimize
from sqlalchemy import func
from app.models.models import Sales,Sales_details,Product

def prepare_data_for_product(session: Session, product_id: int) -> pd.DataFrame:
    """
    Извлекает и подготавливает данные из базы для указанного продукта.

    :param session: Сессия SQLAlchemy для работы с базой данных.
    :param product_id: ID продукта.
    :return: DataFrame с подготовленными данными.
    """
    # Извлечение данных для конкретного товара
    query = (
        session.query(
            func.date_trunc('day', Sales.sale_date).label("date"),
            Sales_details.sale_amount.label("item_cnt_day"),
            Product.price.label("item_price")
        )
        .join(Sales_details, Sales.id == Sales_details.sale_id)
        .join(Product, Product.id == Sales_details.product_id)
        .filter(Product.id == product_id)
    )

    # Преобразуем результаты запроса в DataFrame
    data = pd.DataFrame(query.all(), columns=["date", "item_cnt_day", "item_price"])

    # Убедимся, что есть данные
    if data.empty:
        raise ValueError(f"Нет данных для продукта с ID {product_id}")

    # Подготовка данных
    data["date"] = pd.to_datetime(data["date"])
    data["day_of_week"] = data["date"].dt.dayofweek
    data["month"] = data["date"].dt.month
    data["year"] = data["date"].dt.year

    return data[["item_price", "day_of_week", "month", "year", "item_cnt_day"]]

def train_demand_model(data: pd.DataFrame):
    """
    Обучает модель спроса для конкретного продукта.

    :param data: DataFrame с подготовленными данными.
    :return: Обученная модель.
    """
    X = data[["item_price", "day_of_week", "month"]]
    y = data["item_cnt_day"]

    # Разделение данных на обучающую и тестовую выборки
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Обучение модели
    model = Ridge(alpha=1.0)
    model.fit(X_train, y_train)

    # Оценка модели
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    print(f"MSE модели спроса для продукта: {mse:.2f}")

    return model

def optimize_price_for_product(demand_model, cost, price_range, day_of_week, month):
    """
    Оптимизирует цену для конкретного продукта, чтобы максимизировать прибыль.

    :param demand_model: Обученная модель спроса.
    :param cost: Себестоимость товара.
    :param price_range: Диапазон цен (min, max).
    :param day_of_week: День недели (int).
    :param month: Месяц (int).
    :return: Оптимальная цена.
    """
    def profit_function(price):
        # Создаем корректный массив для прогнозирования
        features = np.array([[price[0], day_of_week, month]])
        predicted_demand = demand_model.predict(features)[0]  # Прогноз спроса
        profit = (price[0] - cost) * predicted_demand
        return -profit  # Негативное значение для минимизации

    # Оптимизация цены
    result = minimize(profit_function, x0=[(price_range[0] + price_range[1]) / 2], bounds=[price_range])
    return result.x[0]

def pred_main(session: Session, product_id: int):
    """
    Главная функция для загрузки данных, обучения модели и оптимизации цены для продукта.

    :param session: Сессия SQLAlchemy для работы с базой данных.
    :param product_id: ID продукта для анализа.
    """
    # Извлечение и подготовка данных
    try:
        data = prepare_data_for_product(session, product_id)
    except ValueError as e:
        print(e)
        return

    # Обучение модели спроса
    demand_model = train_demand_model(data)

    cost = 50.0
    price_range = (80, 150)  # Диапазон цен
    day_of_week = 2  # Пример дня недели
    month = 1  # Пример месяца

    optimal_price = optimize_price_for_product(demand_model, cost, price_range, day_of_week, month)
    # print(f"Оптимальная цена для продукта с ID {product_id}: {optimal_price:.2f}")
    return optimal_price
