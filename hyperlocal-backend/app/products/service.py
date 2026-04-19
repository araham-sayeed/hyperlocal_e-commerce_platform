from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.core.exceptions import ForbiddenError, NotFoundError
from app.products.models import Product
from app.products.schemas import ProductCreate, ProductUpdate
from app.users.shop_owner.models import ShopOwner


def create_product(db: Session, owner: ShopOwner, data: ProductCreate) -> Product:
    p = Product(
        shop_owner_id=owner.id,
        subcategory_id=data.subcategory_id,
        name=data.name,
        description=data.description,
        price=float(data.price),
        stock_quantity=data.stock_quantity,
    )
    db.add(p)
    db.commit()
    db.refresh(p)
    return p


def get_product(db: Session, product_id: int) -> Product:
    p = db.get(Product, product_id)
    if not p:
        raise NotFoundError("Product not found")
    return p


def list_products(
    db: Session,
    *,
    q: str | None,
    subcategory_id: int | None,
    shop_owner_id: int | None,
    limit: int,
    offset: int,
):
    query = db.query(Product).filter(Product.is_active.is_(True))
    if q:
        like = f"%{q}%"
        query = query.filter(or_(Product.name.ilike(like), Product.description.ilike(like)))
    if subcategory_id is not None:
        query = query.filter(Product.subcategory_id == subcategory_id)
    if shop_owner_id is not None:
        query = query.filter(Product.shop_owner_id == shop_owner_id)
    total = query.count()
    items = query.order_by(Product.id.desc()).offset(offset).limit(limit).all()
    return items, total


def update_product(db: Session, owner: ShopOwner, product_id: int, data: ProductUpdate) -> Product:
    p = get_product(db, product_id)
    if p.shop_owner_id != owner.id:
        raise ForbiddenError("Not your product")
    if data.name is not None:
        p.name = data.name
    if data.description is not None:
        p.description = data.description
    if data.price is not None:
        p.price = float(data.price)
    if data.stock_quantity is not None:
        p.stock_quantity = data.stock_quantity
    if data.is_active is not None:
        p.is_active = data.is_active
    db.add(p)
    db.commit()
    db.refresh(p)
    return p


def delete_product(db: Session, owner: ShopOwner, product_id: int) -> None:
    p = get_product(db, product_id)
    if p.shop_owner_id != owner.id:
        raise ForbiddenError("Not your product")
    db.delete(p)
    db.commit()
