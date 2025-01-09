from backend_fstapi.sales_api import Sales, Sales_details, Product
import pandas as pd
from prediction_model import predict_price_for_requested_data
import sqlalchemy.orm

def fetch_and_predict_product_data(session, product_id):
    """
    Запрашивает данные и предсказывает цену товара.

    :param session: Активная сессия SQLAlchemy.
    :param product_id: ID товара.
    :return: Предсказанная цена товара.
    """

    # Получаем данные о продажах и деталях продаж
    query = (
        session.query(Sales.sale_date, Sales_details.amount, Product.price)
        .join(Sales_details, Sales.id == Sales_details.sale_id)
        .join(Product, Product.id == Sales_details.product_id)
        .filter(Product.id == product_id)
    )

    # Преобразуем результат запроса в Pandas DataFrame
    data = pd.DataFrame(query.all(), columns=["sale_date", "sold_quantity", "product_price"])
    
    # Используем модель для предсказания цены
    predicted_price = predict_price_for_requested_data(data)
    
    return predicted_price
