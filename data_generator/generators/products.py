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
from data_generator.config import CATALOG, FAKER_LOCALE, PRODUCT_START_DATE





# Faker configuration
fake = Faker(FAKER_LOCALE)





# Creation of various configurations
STORAGE_VARIANTS: dict[str, list[str]] = {
    "Smartphones": ["128GB", "256GB", "512GB", "1TB"],
    "Tablets":     ["64GB", "128GB", "256GB", "512GB"],
}

LAPTOP_CONFIGS: list[str] = [
    "8GB / 256GB SSD",
    "16GB / 512GB SSD",
    "16GB / 1TB SSD",
    "32GB / 512GB SSD",
    "32GB / 1TB SSD",
    "64GB / 2TB SSD",
]

COLOR_VARIANTS: dict[str, list[str]] = {
    "Smartwatches & Wearables": ["Midnight", "Starlight", "Silver", "Blue"],
    "Headphones & Audio":       ["Black", "White", "Midnight Blue"],
    "Gaming":                   ["Black", "White"],
    "Smart Home":               ["Charcoal", "Glacier White", "Blue", "Sand"],
    "Accessories & Cables":     ["Black", "White", "Dark Gray"],
}

CAMERA_VARIANTS: list[str] = ["Body Only", "with 24-70mm Kit Lens"]





# Expanding the catalog into a deduplicated list of unique SKUs
def _expand_skus() -> list[dict]:
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
                for variant in sku.get("variants", [sku["name"]]):
                    name = f"{sku['name']} — {variant}" if sku.get("variants") else sku["name"]
                    expanded.append({**base, "name": name})

    return expanded





# Build once at module import - reused across all generate_products() calls
_EXPANDED_SKUS: list[dict] = _expand_skus()





# Generation of the fake products
def generate_products(n: int) -> list[dict]:
    import warnings

    start_dt    = datetime.fromisoformat(PRODUCT_START_DATE)
    end_dt      = datetime.now()
    unique_count = len(_EXPANDED_SKUS)

    if n > unique_count:
        warnings.warn(
            f"Requested {n} products but only {unique_count} unique SKUs available. "
            f"Capping at {unique_count} to avoid duplicates.",
            stacklevel = 2,
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
