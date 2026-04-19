from pydantic import BaseModel


class CategoryOut(BaseModel):
    id: int
    name: str
    slug: str
    description: str | None

    model_config = {"from_attributes": True}


class SubCategoryOut(BaseModel):
    id: int
    category_id: int
    name: str
    slug: str

    model_config = {"from_attributes": True}


class StoreSearchOut(BaseModel):
    shop_owner_id: int
    shop_name: str
    latitude: float | None
    longitude: float | None


class StoreNearbyOut(BaseModel):
    shop_owner_id: int
    shop_name: str
    distance_km: float
    latitude: float | None
    longitude: float | None
