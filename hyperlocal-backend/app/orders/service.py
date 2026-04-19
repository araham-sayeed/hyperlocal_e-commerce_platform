from sqlalchemy.orm import Session, joinedload

from app.core.exceptions import BadRequestError, ForbiddenError, NotFoundError
from app.orders.models import Order, OrderItem
from app.orders.schemas import OrderCreate
from app.products.models import Product
from app.users.customer.models import Customer


def place_order(db: Session, customer: Customer, data: OrderCreate) -> Order:
    lines = data.lines
    product_ids = [ln.product_id for ln in lines]
    products = db.query(Product).filter(Product.id.in_(product_ids)).all()
    by_id = {p.id: p for p in products}
    if len(by_id) != len(product_ids):
        raise BadRequestError("One or more products not found")

    for p in by_id.values():
        if p.shop_owner_id != data.shop_owner_id:
            raise BadRequestError("All items must belong to shop_owner_id")

    total = 0.0
    order_items: list[OrderItem] = []
    for ln in lines:
        p = by_id[ln.product_id]
        if not p.is_active:
            raise BadRequestError(f"Product {p.id} is not available")
        if p.stock_quantity < ln.quantity:
            raise BadRequestError(f"Insufficient stock for product {p.id}")
        line_total = float(p.price) * ln.quantity
        total += line_total
        order_items.append(OrderItem(product_id=p.id, quantity=ln.quantity, unit_price=float(p.price)))

    order = Order(
        customer_id=customer.id,
        shop_owner_id=data.shop_owner_id,
        status="placed",
        total_amount=total,
        delivery_latitude=data.delivery_latitude,
        delivery_longitude=data.delivery_longitude,
        items=order_items,
    )
    for ln in lines:
        p = by_id[ln.product_id]
        p.stock_quantity -= ln.quantity
        db.add(p)
    db.add(order)
    db.commit()
    oid = order.id
    return db.query(Order).options(joinedload(Order.items)).filter(Order.id == oid).one()


def get_order(db: Session, customer: Customer, order_id: int) -> Order:
    order = db.query(Order).options(joinedload(Order.items)).filter(Order.id == order_id).first()
    if not order:
        raise NotFoundError("Order not found")
    if order.customer_id != customer.id:
        raise ForbiddenError("Not your order")
    return order


def cancel_order(db: Session, customer: Customer, order_id: int) -> Order:
    order = get_order(db, customer, order_id)
    if order.status in ("delivered", "cancelled"):
        raise BadRequestError("Order cannot be cancelled")
    order.status = "cancelled"
    for item in order.items:
        p = db.get(Product, item.product_id)
        if p:
            p.stock_quantity += item.quantity
            db.add(p)
    db.add(order)
    db.commit()
    oid = order.id
    return db.query(Order).options(joinedload(Order.items)).filter(Order.id == oid).one()
