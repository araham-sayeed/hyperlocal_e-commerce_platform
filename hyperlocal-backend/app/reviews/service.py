from sqlalchemy.orm import Session

from app.core.exceptions import BadRequestError, NotFoundError
from app.products.models import Product
from app.reviews.models import Review
from app.reviews.schemas import ReviewCreate
from app.users.customer.models import Customer


def submit_review(db: Session, customer: Customer, data: ReviewCreate) -> Review:
    p = db.get(Product, data.product_id)
    if not p:
        raise NotFoundError("Product not found")
    existing = (
        db.query(Review)
        .filter(Review.product_id == data.product_id, Review.customer_id == customer.id)
        .first()
    )
    if existing:
        raise BadRequestError("You already reviewed this product")
    r = Review(
        product_id=data.product_id,
        customer_id=customer.id,
        rating=data.rating,
        comment=data.comment,
        status="visible",
    )
    db.add(r)
    db.commit()
    db.refresh(r)
    return r


def moderate_review(db: Session, review_id: int, visible: bool) -> Review:
    r = db.get(Review, review_id)
    if not r:
        raise NotFoundError("Review not found")
    r.status = "visible" if visible else "hidden"
    db.add(r)
    db.commit()
    db.refresh(r)
    return r


def list_for_product(db: Session, product_id: int):
    return (
        db.query(Review)
        .filter(Review.product_id == product_id, Review.status == "visible")
        .order_by(Review.id.desc())
        .all()
    )
