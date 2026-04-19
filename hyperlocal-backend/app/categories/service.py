from sqlalchemy.orm import Session

from app.categories.models import Category, SubCategory
from app.core.location import haversine_km
from app.users.shop_owner.models import ShopOwner


def list_categories(db: Session):
    return db.query(Category).order_by(Category.name).all()


def list_subcategories(db: Session, category_id: int):
    return db.query(SubCategory).filter(SubCategory.category_id == category_id).order_by(SubCategory.name).all()


def search_shops_by_name(db: Session, q: str, limit: int):
    like = f"%{q}%"
    return db.query(ShopOwner).filter(ShopOwner.shop_name.ilike(like)).order_by(ShopOwner.shop_name).limit(limit).all()


def stores_nearby(db: Session, lat: float, lon: float, radius_km: float, limit: int):
    owners = db.query(ShopOwner).filter(ShopOwner.latitude.isnot(None), ShopOwner.longitude.isnot(None)).all()
    ranked: list[tuple[ShopOwner, float]] = []
    for o in owners:
        assert o.latitude is not None and o.longitude is not None
        d = haversine_km(lat, lon, o.latitude, o.longitude)
        if d <= radius_km:
            ranked.append((o, d))
    ranked.sort(key=lambda x: x[1])
    return ranked[:limit]
