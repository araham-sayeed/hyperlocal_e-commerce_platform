from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_customer
from app.returns.schemas import ReturnCreate, ReturnOut
from app.returns import service
from app.users.customer.models import Customer

router = APIRouter(prefix="/returns", tags=["Returns"])


@router.post("", response_model=ReturnOut)
def initiate_return(
    body: ReturnCreate,
    customer: Customer = Depends(get_current_customer),
    db: Session = Depends(get_db),
):
    return service.initiate_return(db, customer, body.order_id, body.reason)


@router.post("/{return_id}/approve", response_model=ReturnOut)
def approve_return(return_id: int, approve: bool = True, db: Session = Depends(get_db)):
    """Demo shop/admin endpoint."""
    return service.approve_return(db, return_id, approve)


@router.get("/{return_id}", response_model=ReturnOut)
def get_return(
    return_id: int,
    customer: Customer = Depends(get_current_customer),
    db: Session = Depends(get_db),
):
    return service.get_return(db, customer, return_id)
