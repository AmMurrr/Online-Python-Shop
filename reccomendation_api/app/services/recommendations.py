from sqlalchemy.orm import Session
from app.models.models import  Item,Category
from app.utils.responses import ResponseHandler
from sqlalchemy.orm import joinedload
from app.core.recommendations import get_recommendations

class RecService:
    # Get recommendation
    @staticmethod
    def get_recommendation( db: Session,item_name: str):
        item = db.query(Item).filter(Item.item_name == item_name).first()
        if not item:
            return {"error": "Товар не найден"}
        
        category = db.query(Category).filter(Category.item_category_id == item.item_category_id).first()
        if not category:
            return {"error": "Категория не найдена"}
        
        same_filter_recommendations = get_recommendations(db,item.item_id)

        response = {
            "same_filter_recommendations": same_filter_recommendations
           
        }

        return response


    @staticmethod
    def add_item(db: Session, item_name: str, item_category: str):

        item = db.query(Item).filter(Item.item_name == item_name).first()
        if item:
            return {"error": "Товар уже есть в таблице"}

        category = db.query(Category).filter(Category.item_category_name == item_category).first()
        if not category:
            category_db = Category(item_category_id=None,item_category_name=item_category)
            db.add(category_db)
            db.commit()
            db.refresh(category_db)

            item_db = Item(item_id=None,item_name=item_name,item_category_id=category_db.item_category_id)
        else:   
            item_db = Item(item_id=None,item_name=item_name,item_category_id=category.item_category_id)

        db.add(item_db)
        db.commit()
        db.refresh(item_db)

        response = {
            "new_item_id": item_db.item_id
        }

        return response