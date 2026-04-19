from typing import Any

SUBSCRIPTION_TIERS: dict[str, dict[str, Any]] = {
    "starter": {"max_products": 100, "featured_listings": 0},
    "growth": {"max_products": 500, "featured_listings": 5},
    "pro": {"max_products": 5000, "featured_listings": 20},
}


def get_plan_features(plan_tier: str) -> dict[str, Any]:
    return SUBSCRIPTION_TIERS.get(plan_tier, SUBSCRIPTION_TIERS["starter"])
