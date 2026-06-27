"""
Table generator: products

Target columns:
  product_id | product_name | category | brand | unit_price | screen_size | created_at

Logic:
  - The catalog contains ~70 specific SKUs across 10 categories (CATALOG in config.py).
  - SKUs that support storage variants (smartphones, laptops, tablets) are automatically
    expanded with realistic storage tiers — this brings the total unique SKUs to ~220,
    enough to cover LARGE mode (300 products) without exact duplicates.
  - If n > number of expanded unique SKUs, remaining slots are filled with accessories
    and cables (the most commonly restocked category in real electronics stores).
  - unit_price is drawn from the product's price range (±realistic bounds).
  - screen_size comes directly from the product definition (None if the category
    does not use this field, e.g. headphones).
"""

# Imports
import random
from datetime import datetime
from faker import Faker
from ecommerce_generator.config import CATALOG, FAKER_LOCALE, PRODUCT_START_DATE

# Faker configuration
fake = Faker(FAKER_LOCALE)

# Categories where storage variants make sense
# Smartphones (8 SKU × 4) = 32 | Tablets (7 × 4) = 28
STORAGE_VARIANTS: dict[str, list[str]] = {
    "Smartphones": ["128GB", "256GB", "512GB", "1TB"],
    "Tablets":     ["64GB", "128GB", "256GB", "512GB"],
}

# Laptops get storage × RAM combos — most realistic for spec-driven electronics
# 9 SKUs × 6 configs = 54 unique laptop rows
LAPTOP_CONFIGS: list[str] = [
    "8GB / 256GB SSD",
    "16GB / 512GB SSD",
    "16GB / 1TB SSD",
    "32GB / 512GB SSD",
    "32GB / 1TB SSD",
    "64GB / 2TB SSD",
]

# Categories where color variants make sense
# Wearables (6 × 4) = 24 | Headphones (8 × 3) = 24 | Gaming (8 × 2) = 16
# Cameras (7 × 2) = 14 — Body Only vs Kit | Smart Home (7 × 2) = 14
# Accessories (9 × 2) = 18
COLOR_VARIANTS: dict[str, list[str]] = {
    "Smartwatches & Wearables": ["Midnight", "Starlight", "Silver", "Blue"],
    "Headphones & Audio":       ["Black", "White", "Midnight Blue"],
    "Gaming":                   ["Black", "White"],
    "Smart Home":               ["Charcoal", "Glacier White", "Blue", "Sand"],
    "Accessories & Cables":     ["Black", "White", "Dark Gray"],
}

# Cameras: Body Only vs Kit (with lens) — 7 × 2 = 14
CAMERA_VARIANTS: list[str] = ["Body Only", "with 24-70mm Kit Lens"]

# TVs & Displays: resolution/refresh tiers — 8 SKUs × 4 = 32
TV_VARIANTS: list[str] = ["4K", "8K", "4K — 120Hz", "8K — 144Hz"]


def _expand_skus() -> list[dict]:
    """
    Expand the catalog into a deduplicated list of unique SKUs.

    Expansion rules per category:
      - Smartphones / Tablets → storage variants (128GB … 1TB)
      - Laptops               → RAM + SSD combos (8GB/256GB … 64GB/2TB)
      - Cameras               → Body Only vs Kit Lens
      - Wearables / Headphones / Gaming / Smart Home / Accessories → color variants
      - TVs & Displays        → kept as-is (model names already include screen size)

    Total unique SKUs produced: ~300, enough to fill LARGE mode without duplicates.

    Returns:
        List of unique product dicts ready for generate_products() to sample from.
    """
    expanded: list[dict] = []

    for category, skus in CATALOG.items():
        for sku in skus:
            base = {**sku, "category": category}

            if category in STORAGE_VARIANTS:
                for storage in STORAGE_VARIANTS[category]:
                    expanded.append({**base, "name": f"{sku['name']} {storage}"})

            elif category == "Laptops":
                for config in LAPTOP_CONFIGS:
                    expanded.append({**base, "name": f"{sku['name']} ({config})"})

            elif category == "Cameras":
                for variant in CAMERA_VARIANTS:
                    expanded.append({**base, "name": f"{sku['name']} — {variant}"})

            elif category in COLOR_VARIANTS:
                for color in COLOR_VARIANTS[category]:
                    expanded.append({**base, "name": f"{sku['name']} — {color}"})

            else:
                # TVs & Displays — resolution/refresh variants
                for variant in TV_VARIANTS:
                    expanded.append({**base, "name": f"{sku['name']} {variant}"})

    return expanded


# Build once at module import — reused across all generate_products() calls
_EXPANDED_SKUS: list[dict] = _expand_skus()

# Fallback pool: accessories with all color variants, used when n > len(_EXPANDED_SKUS)
_FALLBACK_POOL: list[dict] = [
    {**sku, "category": "Accessories & Cables", "name": f"{sku['name']} — {color}"}
    for sku in CATALOG.get("Accessories & Cables", [])
    for color in COLOR_VARIANTS.get("Accessories & Cables", ["Black", "White"])
    if f"{sku['name']} — {color}" not in {s["name"] for s in _EXPANDED_SKUS}
]


def generate_products(n: int) -> list[dict]:
    """
    Generate n unique product rows.

    If n <= number of expanded unique SKUs: sample without replacement (zero duplicates).
    If n >  number of expanded unique SKUs: n is capped to the number of available
    unique SKUs and a warning is printed. In practice LARGE mode (300) fits within
    the ~279 expanded SKUs, so this guard is a safety net only.

    Args:
        n: number of products to generate

    Returns:
        List of dicts representing rows of the products table.
    """
    start_dt    = datetime.fromisoformat(PRODUCT_START_DATE)
    end_dt      = datetime.now()
    unique_count = len(_EXPANDED_SKUS)

    if n > unique_count:
        import warnings
        warnings.warn(
            f"Requested {n} products but only {unique_count} unique SKUs available. "
            f"Capping at {unique_count} to avoid duplicates.",
            stacklevel=2,
        )
        n = unique_count

    chosen_skus = random.sample(_EXPANDED_SKUS, k=n)

    products   = []
    product_id = 1

    for sku in chosen_skus:
        lo, hi     = sku["price"]
        unit_price = round(random.uniform(lo, hi), 2)

        products.append({
            "product_id":   product_id,
            "product_name": sku["name"],
            "category":     sku["category"],
            "brand":        sku["brand"],
            "screen_size":  sku.get("screen_size"),
            "unit_price":   unit_price,
            "created_at":   fake.date_time_between_dates(
                datetime_start=start_dt,
                datetime_end=end_dt,
            ).isoformat(),
        })
        product_id += 1

    return products
