from fastapi import APIRouter, Depends, Query, status
from app.core.database import get_db
from app.services.sales import SaleService
from sqlalchemy.orm import Session
from app.schemas.sales import SaleCreate, SalesOut,SaleOut, SaleOutDelete
# from app.core.security import check_admin_role


router = APIRouter(tags=["Sales"], prefix="/sales")

# ,
    # dependencies=[Depends(check_admin_role)]

# Get All Sales
@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=SalesOut)
def get_all_sales(
    db: Session = Depends(get_db),
):
    return SaleService.get_all_sales(db)



# Create New Sale
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=SaleOut)
def create_user(sale: SaleCreate, db: Session = Depends(get_db)):
    return SaleService.create_sale(db, sale)


# Delete Sale By ID
@router.delete(
    "/{sale_id}",
    status_code=status.HTTP_200_OK,
    response_model=SaleOutDelete)
def delete_user(sale_id: int, db: Session = Depends(get_db)):
    return SaleService.delete_sale(db, sale_id)
