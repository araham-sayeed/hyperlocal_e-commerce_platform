from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import get_db
from app.categories.schemas import CategoryOut, StoreNearbyOut, StoreSearchOut, SubCategoryOut
from app.categories import service

router = APIRouter(prefix="/catalog", tags=["Categories & Discovery"])


@router.get("/categories", response_model=list[CategoryOut])
def get_categories(db: Session = Depends(get_db)):
    return service.list_categories(db)


@router.get("/categories/{category_id}/subcategories", response_model=list[SubCategoryOut])
def get_subcategories(category_id: int, db: Session = Depends(get_db)):
    return service.list_subcategories(db, category_id)


@router.get("/stores/search", response_model=list[StoreSearchOut])
def search_stores(
    q: str = Query(..., min_length=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    rows = service.search_shops_by_name(db, q, limit)
    return [
        StoreSearchOut(
            shop_owner_id=o.id,
            shop_name=o.shop_name,
            latitude=o.latitude,
            longitude=o.longitude,
        )
        for o in rows
    ]


@router.get("/stores/nearby", response_model=list[StoreNearbyOut])
def stores_nearby(
    lat: float = Query(..., description="User latitude"),
    lon: float = Query(..., description="User longitude"),
    radius_km: float | None = None,
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    settings = get_settings()
    r = radius_km if radius_km is not None else settings.default_search_radius_km
    rows = service.stores_nearby(db, lat, lon, r, limit)
    return [
        StoreNearbyOut(
            shop_owner_id=o.id,
            shop_name=o.shop_name,
            distance_km=round(d, 3),
            latitude=o.latitude,
            longitude=o.longitude,
        )
        for o, d in rows
    ]
