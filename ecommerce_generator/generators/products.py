"""
Table generator: products

Target columns:
  product_id | product_name | category | brand | unit_price | screen_size | created_at

Logic:
  - The catalog contains about 70 specific SKUs across 10 categories (CATALOG in config.py).
  - The generator draws products from the catalog with weights proportional to the number
    of SKUs per category - larger categories appear proportionally more often.
  - If n > number of unique SKUs, products will repeat (with a new product_id and
    a new created_at date) - this is realistic in LARGE mode (300 products).
  - unit_price is drawn from the product's price range (±realistic bounds
    instead of a single catalog price).
  - screen_size comes directly from the product definition (None if
    the category does not use this field, e.g. headphones).
"""



# Imports
import random
from datetime import datetime
from faker import Faker
from ecommerce_generator.config import CATALOG, FAKER_LOCALE, PRODUCT_START_DATE





# Faker configuration
fake = Faker(FAKER_LOCALE)





# Flattened list of all SKUs with their assigned category — built once
# upon module import so that generate_products() doesn't do it inside the loop
_ALL_SKUS: list[dict] = [
    {**product, "category": category}
    for category, products in CATALOG.items()
    for product in products
]





# Weights proportional to the number of SKUs per category
_CATEGORIES    = list(CATALOG.keys())
_CATEGORY_SIZE = [len(CATALOG[cat]) for cat in _CATEGORIES]





# Generation of fake products
def generate_products(n: int) -> list[dict]:
    start_dt = datetime.fromisoformat(PRODUCT_START_DATE)
    end_dt   = datetime.now()

    # First draw categories (with weights), then a specific SKU from that category
    chosen_categories = random.choices(_CATEGORIES, weights=_CATEGORY_SIZE, k=n)

    products   = []
    product_id = 1

    for category in chosen_categories:
        sku = random.choice(CATALOG[category])

        lo, hi     = sku["price"]
        unit_price = round(random.uniform(lo, hi), 2)

        products.append({
            "product_id":   product_id,
            "product_name": sku["name"],
            "category":     category,
            "brand":        sku["brand"],
            "screen_size":  sku.get("screen_size"),  # None if the field is missing
            "unit_price":   unit_price,
            "created_at":   fake.date_time_between_dates(
                datetime_start = start_dt,
                datetime_end = end_dt,
            ).isoformat(),
        })
        product_id += 1

    return products