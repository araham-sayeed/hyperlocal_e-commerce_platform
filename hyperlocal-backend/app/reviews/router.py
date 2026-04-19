from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_customer
from app.reviews.schemas import ReviewCreate, ReviewOut
from app.reviews import service
from app.users.customer.models import Customer

router = APIRouter(prefix="/reviews", tags=["Reviews"])


@router.post("", response_model=ReviewOut)
def submit_review(
    body: ReviewCreate,
    customer: Customer = Depends(get_current_customer),
    db: Session = Depends(get_db),
):
    return service.submit_review(db, customer, body)


@router.patch("/{review_id}/moderate", response_model=ReviewOut)
def moderate_review(review_id: int, visible: bool = True, db: Session = Depends(get_db)):
    """Demo moderator endpoint — add admin auth later."""
    return service.moderate_review(db, review_id, visible)


@router.get("/product/{product_id}", response_model=list[ReviewOut])
def reviews_for_product(product_id: int, db: Session = Depends(get_db)):
    return service.list_for_product(db, product_id)
