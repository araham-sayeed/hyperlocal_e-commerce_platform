from datetime import UTC, datetime

from sqlalchemy.orm import Session, joinedload

from app.core.exceptions import BadRequestError, ForbiddenError, NotFoundError
from app.orders.models import Order
from app.products.models import Product
from app.categories.models import SubCategory
from app.returns.models import ReturnRequest
from app.returns import policy
from app.users.customer.models import Customer


def _order_age_days(order: Order) -> float:
    created = order.created_at
    if created.tzinfo is None:
        created = created.replace(tzinfo=UTC)
    return (datetime.now(UTC) - created).total_seconds() / 86400


def initiate_return(db: Session, customer: Customer, order_id: int, reason: str) -> ReturnRequest:
    order = db.query(Order).options(joinedload(Order.items)).filter(Order.id == order_id).first()
    if not order:
        raise NotFoundError("Order not found")
    if order.customer_id != customer.id:
        raise ForbiddenError("Not your order")
    if order.status not in ("delivered", "placed", "confirmed"):
        raise BadRequestError("Return not allowed for this order status")

    first_item = order.items[0] if order.items else None
    if not first_item:
        raise BadRequestError("Order has no line items")
    product = db.get(Product, first_item.product_id)
    if not product:
        raise BadRequestError("Product missing")
    sub = db.get(SubCategory, product.subcategory_id)
    slug = sub.slug if sub else "general"
    window = policy.return_window_days_for_subcategory_slug(slug)
    if _order_age_days(order) > window:
        raise BadRequestError(f"Return window expired ({window} days for this category)")

    existing = db.query(ReturnRequest).filter(ReturnRequest.order_id == order_id).first()
    if existing:
        raise BadRequestError("Return already requested for this order")

    r = ReturnRequest(order_id=order_id, customer_id=customer.id, reason=reason, status="requested")
    db.add(r)
    db.commit()
    db.refresh(r)
    return r


def approve_return(db: Session, return_id: int, approve: bool) -> ReturnRequest:
    r = db.get(ReturnRequest, return_id)
    if not r:
        raise NotFoundError("Return not found")
    r.status = "approved" if approve else "rejected"
    db.add(r)
    db.commit()
    db.refresh(r)
    return r


def get_return(db: Session, customer: Customer, return_id: int) -> ReturnRequest:
    r = db.get(ReturnRequest, return_id)
    if not r:
        raise NotFoundError("Return not found")
    if r.customer_id != customer.id:
        raise ForbiddenError("Not your return request")
    return r
