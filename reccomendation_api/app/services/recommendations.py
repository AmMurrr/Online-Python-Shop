from sqlalchemy.orm import Session
from app.models.models import  Item,Category
# from app.schemas.carts import CartUpdate, CartCreate
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
        
        same_filter_recommendations, similar_recommendations = get_recommendations(item.item_id)

        response = {
            "same_filter_recommendations": same_filter_recommendations
            # "similar_recommendations": similar_recommendations
        }

        return response