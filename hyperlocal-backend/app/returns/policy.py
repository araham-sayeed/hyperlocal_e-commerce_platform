"""Return windows by category slug (demo rules)."""

RETURN_DAYS_BY_CATEGORY_SLUG: dict[str, int] = {
    "essential-goods": 7,
    "electronics": 14,
    "apparel": 10,
    "furniture-home": 5,
}


def return_window_days_for_subcategory_slug(slug: str) -> int:
    for key, days in RETURN_DAYS_BY_CATEGORY_SLUG.items():
        if slug.startswith(key) or key in slug:
            return days
    return 7
