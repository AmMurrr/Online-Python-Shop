from fastapi import APIRouter, Depends, Query, status
from app.core.database import get_db
from app.services.recommendations import RecService
from sqlalchemy.orm import Session
# from app.schemas.carts import RecOut
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials

router = APIRouter(tags=["Recommendation"], prefix="/rec")
auth_scheme = HTTPBearer()


# Get recommendation
@router.get("/{item_name}", status_code=status.HTTP_200_OK)#, response_model=RecOut)
def get_cart(
        item_name: str,
        db: Session = Depends(get_db)
):
    return RecService.get_recommendation( db,item_name)