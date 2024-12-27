from sqlalchemy.orm import Session
from app.models.models import Sales, Sales_details, Product
from app.schemas.sales import SaleCreate,SalesOut
from app.utils.responses import ResponseHandler
# from app.core.security import get_password_hash


class SaleService:
    @staticmethod
    def get_all_sales(db: Session):
        sales = db.query(Sales).order_by(Sales.id.asc()).all()
        return {"message": f"All Sales:", "data": sales}


    @staticmethod
    def create_sale(db: Session, sale: SaleCreate):

        sale_dict = sale.model_dump()
        sale_user = sale_dict.pop("user_id")
        total_cost = sale_dict.pop("total_cost")
        sale_items_data = sale_dict.pop("sale_items", [])

        sale_db = Sales(total_cost=total_cost, user_id=sale_user)
        db.add(sale_db)
        db.commit()
        db.refresh(sale_db)

        sale_id = sale_db.id

        
        for item_data in sale_items_data:
            product_id = item_data['product_id']
            sale_amount = item_data['sale_amount']

            product = db.query(Product).filter(Product.id == product_id).first()
            if not product:
                return ResponseHandler.not_found_error("Product", product_id)

           
            sale_item = Sales_details(product_id=product_id, sale_amount=sale_amount)

            details_db = Sales_details(sale_id=sale_id, product_id=product_id, sale_amount=sale_amount)
            db.add(details_db)
            db.commit()
            db.refresh(details_db)

        return ResponseHandler.create_success("Sale", sale_db.id, sale_db)


    @staticmethod
    def delete_sale(db: Session, sale_id: int):
        db_sale = db.query(Sales).filter(Sales.id == sale_id).first()
        if not db_sale:
            ResponseHandler.not_found_error("Sale", sale_id)
        db.delete(db_sale)
        db.commit()
        return ResponseHandler.delete_success(db_sale.id, db_sale)
