from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import Base, SessionLocal, engine
from app.core.rate_limiter import limiter

from app.categories import models as _categories_models  # noqa: F401
from app.chat import models as _chat_models  # noqa: F401
from app.orders import models as _orders_models  # noqa: F401
from app.products import models as _products_models  # noqa: F401
from app.reviews import models as _reviews_models  # noqa: F401
from app.returns import models as _returns_models  # noqa: F401
from app.support import models as _support_models  # noqa: F401
from app.users.customer import models as _customer_models  # noqa: F401
from app.users.rider import models as _rider_models  # noqa: F401
from app.users.shop_owner import models as _shop_owner_models  # noqa: F401

from app.categories.router import router as categories_router
from app.chat.router import router as chat_router
from app.orders.router import router as orders_router
from app.products.router import router as products_router
from app.reviews.router import router as reviews_router
from app.returns.router import router as returns_router
from app.support.router import router as support_router
from app.users.customer.router import router as customer_router
from app.users.rider.router import router as rider_router
from app.users.shop_owner.router import router as shop_owner_router


def _seed_if_empty() -> None:
    from app.categories.models import Category, SubCategory
    from app.support.models import FAQ, RegionalContact

    db: Session = SessionLocal()
    try:
        if db.query(Category).first() is not None:
            return
        catalog = [
            (
                "Essential Goods",
                "essential-goods",
                [("Household", "household"), ("Cleaning", "cleaning")],
            ),
            (
                "Electronics",
                "electronics",
                [("Mobile Accessories", "mobile-accessories"), ("Small Appliances", "small-appliances")],
            ),
            ("Apparel", "apparel", [("Men", "men"), ("Women", "women")]),
            (
                "Furniture & Home",
                "furniture-home",
                [("Decor", "decor"), ("Storage", "storage")],
            ),
        ]
        for name, slug, subs in catalog:
            c = Category(name=name, slug=slug, description=f"{name} (Pune pilot)")
            db.add(c)
            db.flush()
            for sub_name, sub_slug in subs:
                db.add(SubCategory(category_id=c.id, name=sub_name, slug=sub_slug))

        faqs = [
            ("What is the delivery fee?", "Fees depend on distance; Pune pilot uses flat demo rates."),
            ("How do I register as a shop?", "Use POST /api/v1/shop-owners/register then list products."),
            ("How does OTP login work?", "POST /api/v1/customers/otp/send then verify with the dev code."),
        ]
        for q, a in faqs:
            db.add(FAQ(question=q, answer=a, region="Pune"))

        for area, phone in (
            ("Kothrud", "+91-20-1111-1111"),
            ("Baner", "+91-20-2222-2222"),
            ("Wakad", "+91-20-3333-3333"),
        ):
            db.add(RegionalContact(area_name=area, support_phone=phone))

        db.commit()
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    _seed_if_empty()
    yield


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.app_name, lifespan=lifespan)
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    api = settings.api_v1_prefix
    app.include_router(shop_owner_router, prefix=api)
    app.include_router(rider_router, prefix=api)
    app.include_router(customer_router, prefix=api)
    app.include_router(categories_router, prefix=api)
    app.include_router(products_router, prefix=api)
    app.include_router(orders_router, prefix=api)
    app.include_router(chat_router, prefix=api)
    app.include_router(reviews_router, prefix=api)
    app.include_router(returns_router, prefix=api)
    app.include_router(support_router, prefix=api)

    @app.get("/health", tags=["Health"])
    def health():
        return {"status": "ok"}

    return app


app = create_app()
