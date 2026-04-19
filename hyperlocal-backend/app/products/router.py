from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.pagination import PaginatedResponse, PaginationParams
from app.database import get_db
from app.dependencies import get_current_shop_owner
from app.products.schemas import ProductCreate, ProductOut, ProductUpdate
from app.products import service
from app.users.shop_owner.models import ShopOwner

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("", response_model=PaginatedResponse[ProductOut])
def search_products(
    q: str | None = None,
    subcategory_id: int | None = None,
    shop_owner_id: int | None = None,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
):
    items, total = service.list_products(
        db,
        q=q,
        subcategory_id=subcategory_id,
        shop_owner_id=shop_owner_id,
        limit=pagination.limit,
        offset=pagination.offset,
    )
    return PaginatedResponse[ProductOut].build(
        [ProductOut.model_validate(i) for i in items],
        total,
        pagination.limit,
        pagination.offset,
    )


@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    return service.get_product(db, product_id)


@router.post("", response_model=ProductOut)
def create_product(
    body: ProductCreate,
    owner: ShopOwner = Depends(get_current_shop_owner),
    db: Session = Depends(get_db),
):
    return service.create_product(db, owner, body)


@router.patch("/{product_id}", response_model=ProductOut)
def update_product(
    product_id: int,
    body: ProductUpdate,
    owner: ShopOwner = Depends(get_current_shop_owner),
    db: Session = Depends(get_db),
):
    return service.update_product(db, owner, product_id, body)


@router.delete("/{product_id}", status_code=204)
def remove_product(
    product_id: int,
    owner: ShopOwner = Depends(get_current_shop_owner),
    db: Session = Depends(get_db),
):
    service.delete_product(db, owner, product_id)
