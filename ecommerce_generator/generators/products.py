"""
Generator tabeli: products

Kolumny docelowe:
  product_id | product_name | category | brand | unit_price | screen_size | created_at

Logika:
  - Katalog zawiera ~70 konkretnych SKU w 10 kategoriach (CATALOG w config.py).
  - Generator losuje produkty z katalogu z wagami proporcjonalnymi do liczby
    SKU per kategoria — większe kategorie są proporcjonalnie częstsze.
  - Przy n > liczba unikalnych SKU produkty powtarzają się (nowy product_id,
    nowa data created_at) — realistyczne przy trybie LARGE (300 produktów).
  - unit_price losowany z zakresu price produktu (±realistyczne widełki
    zamiast jednej ceny katalogowej).
  - screen_size pochodzi bezpośrednio z definicji produktu (None jeśli
    kategoria nie używa tego pola, np. słuchawki).
"""

import random
from datetime import datetime
from faker import Faker
from ecommerce_generator.config import CATALOG, FAKER_LOCALE, PRODUCT_START_DATE

fake = Faker(FAKER_LOCALE)

# Spłaszczona lista wszystkich SKU z przypisaną kategorią — budowana raz
# przy imporcie modułu, żeby generate_products() nie robiła tego w pętli.
_ALL_SKUS: list[dict] = [
    {**product, "category": category}
    for category, products in CATALOG.items()
    for product in products
]

# Wagi proporcjonalne do liczby SKU per kategoria
_CATEGORIES    = list(CATALOG.keys())
_CATEGORY_SIZE = [len(CATALOG[cat]) for cat in _CATEGORIES]


def generate_products(n: int) -> list[dict]:
    """
    Generuje n wierszy tabeli products.

    Losowanie odbywa się z powtórzeniami (replace=True), więc n może być
    większe niż liczba unikalnych SKU w katalogu — każde losowanie dostaje
    nowy product_id i datę created_at.

    Args:
        n: liczba produktów do wygenerowania

    Returns:
        Lista słowników reprezentujących wiersze tabeli products.
    """
    start_dt = datetime.fromisoformat(PRODUCT_START_DATE)
    end_dt   = datetime.now()

    # Losujemy najpierw kategorie (z wagami), potem konkretny SKU z kategorii
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
            "screen_size": sku.get("screen_size"),  # None jeśli brak pola
            "unit_price":   unit_price,
            "created_at":   fake.date_time_between_dates(
                datetime_start=start_dt,
                datetime_end=end_dt,
            ).isoformat(),
        })
        product_id += 1

    return products
