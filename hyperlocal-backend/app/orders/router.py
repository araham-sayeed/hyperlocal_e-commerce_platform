from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_customer
from app.orders.schemas import OrderCreate, OrderOut
from app.orders import service
from app.users.customer.models import Customer

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("", response_model=OrderOut)
def place_order(
    body: OrderCreate,
    customer: Customer = Depends(get_current_customer),
    db: Session = Depends(get_db),
):
    return service.place_order(db, customer, body)


@router.get("/{order_id}", response_model=OrderOut)
def get_order(
    order_id: int,
    customer: Customer = Depends(get_current_customer),
    db: Session = Depends(get_db),
):
    return service.get_order(db, customer, order_id)


@router.post("/{order_id}/cancel", response_model=OrderOut)
def cancel_order(
    order_id: int,
    customer: Customer = Depends(get_current_customer),
    db: Session = Depends(get_db),
):
    return service.cancel_order(db, customer, order_id)
