"""
Generator tabeli: products

Kolumny docelowe:
  product_id | product_name | category | brand | unit_price | created_at
"""

import random
import string
from datetime import datetime
from faker import Faker
from ecommerce_generator.config import FAKER_LOCALE, CATALOG, PRODUCT_COLORS, SCREEN_SIZES, PRODUCT_START_DATE

fake = Faker(FAKER_LOCALE)


def _random_model_code() -> str:
    """
    Generuje kod modelu w stylu producenta elektroniki.
    Przykłady: 'X-490', 'Pro-7', 'A55-Ultra'
    """
    patterns = [
        lambda: f"{random.choice(string.ascii_uppercase)}{random.randint(10, 99)}",
        lambda: f"{random.choice(string.ascii_uppercase)}{random.randint(100, 999)}",
        lambda: f"{random.choice(string.ascii_uppercase)}{random.randint(10, 99)}{random.choice(string.ascii_uppercase)}",
        lambda: f"Pro-{random.randint(5, 15)}",
        lambda: f"Max-{random.randint(5, 15)}",
    ]
    return random.choice(patterns)()


def build_product_name(template: str, brand: str) -> str:
    """
    Buduje nazwę produktu na podstawie szablonu i marki.
    """
    return template.format(
        brand=brand,
        model=_random_model_code(),
        size=random.choice(SCREEN_SIZES),
        color=random.choice(PRODUCT_COLORS),
    )


def generate_products(n: int) -> list[dict]:
    """
    Generuje n produktów z katalogu elektroniki.

    Args:
        n: liczba produktów do wygenerowania

    Returns:
        Lista słowników reprezentujących wiersze tabeli products.
    """
    categories = list(CATALOG.keys())
    products = []
    product_id = 1

    start_dt = datetime.fromisoformat(PRODUCT_START_DATE)
    end_dt = datetime.now()

    for i in range(n):
        category = categories[i % len(categories)]
        category_cfg = CATALOG[category]

        brand = random.choice(category_cfg["brands"])
        template = random.choice(category_cfg["templates"])
        product_name = build_product_name(template, brand)

        lo, hi = category_cfg["price_range"]
        unit_price = round(random.uniform(lo, hi), 2)

        products.append({
            "product_id": product_id,
            "product_name": product_name,
            "category": category,
            "brand": brand,
            "unit_price": unit_price,
            "created_at": fake.date_time_between_dates(
                datetime_start=start_dt,
                datetime_end=end_dt
            ).isoformat(),
        })
        product_id += 1

    return products