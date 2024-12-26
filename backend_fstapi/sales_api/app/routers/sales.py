from fastapi import APIRouter, Depends, Query, status
from app.core.database import get_db
from app.services.sales import SaleService
from sqlalchemy.orm import Session
from app.schemas.sales import SaleCreate, SalesOut,SaleOut, SaleOutDelete
from app.core.security import check_admin_role


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
    # page: int = Query(1, ge=1, description="Page number"),
    # limit: int = Query(10, ge=1, le=100, description="Items per page"),
    # search: str | None = Query("", description="Search based username"),
):
    return SaleService.get_all_sales(db)



# Create New Sale
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=SaleOut,
    dependencies=[Depends(check_admin_role)])
def create_user(sale: SaleCreate, db: Session = Depends(get_db)):
    return SaleService.create_sale(db, sale)


# Delete Sale By ID
@router.delete(
    "/{sale_id}",
    status_code=status.HTTP_200_OK,
    response_model=SaleOutDelete,
    dependencies=[Depends(check_admin_role)])
def delete_user(sale_id: int, db: Session = Depends(get_db)):
    return SaleService.delete_user(db, sale_id)
