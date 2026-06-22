"""
Generator tabeli: order_items

Kolumny docelowe:
  order_item_id | order_id | product_id | quantity | unit_price

Logika:
  - Segment klienta wpływa na to, z jakich kategorii częściej kupuje.
  - VIP-y częściej kupują więcej pozycji w zamówieniu.
  - unit_price bazuje na cenie produktu i ma małe odchylenie promocyjne.
"""

import random
from ecommerce_generator.config import SEGMENTS, SEGMENT_CATEGORY_PREFERENCES


SEGMENT_ITEM_RANGE = {
    "VIP": (3, 5),
    "Regular": (2, 4),
    "Occasional": (1, 3),
    "Dormant": (1, 2),
}

SEGMENT_QUANTITY_MAX = {
    "VIP": 3,
    "Regular": 2,
    "Occasional": 2,
    "Dormant": 1,
}


def _build_category_map(products: list[dict]) -> dict[str, list[dict]]:
    """Grupuje produkty po kategoriach."""
    category_map: dict[str, list[dict]] = {}
    for product in products:
        category_map.setdefault(product["category"], []).append(product)
    return category_map


def _pick_product(
    products: list[dict],
    category_map: dict[str, list[dict]],
    preferred_categories: list[str],
    used_product_ids: set[int],
) -> dict | None:
    """
    Wybiera produkt preferując kategorie z listy preferred_categories.
    Zwraca None, jeśli nie ma już wolnych produktów.
    """
    preferred_pool = [
        p for cat in preferred_categories
        for p in category_map.get(cat, [])
        if p["product_id"] not in used_product_ids
    ]

    fallback_pool = [
        p for p in products
        if p["product_id"] not in used_product_ids
    ]

    if preferred_pool and random.random() < 0.85:
        return random.choice(preferred_pool)

    if fallback_pool:
        return random.choice(fallback_pool)

    return None


def generate_order_items(
    orders: list[dict],
    products: list[dict],
    clients: list[dict],
) -> list[dict]:
    """
    Generuje pozycje zamówień.

    Args:
        orders:   lista z generators/orders.py
        products: lista z generators/products.py
        clients:  lista z generators/clients.py

    Returns:
        Lista słowników reprezentujących wiersze tabeli order_items.
    """
    client_segment = {c["client_id"]: c.get("_segment", "Regular") for c in clients}
    category_map = _build_category_map(products)

    order_items = []
    order_item_id = 1

    for order in orders:
        segment = client_segment.get(order["client_id"], "Regular")
        preferred_categories = SEGMENT_CATEGORY_PREFERENCES.get(segment, list(category_map.keys()))

        lo, hi = SEGMENT_ITEM_RANGE.get(segment, (1, 3))
        num_items = random.randint(lo, hi)

        used_product_ids = set()

        for _ in range(num_items):
            product = _pick_product(
                products=products,
                category_map=category_map,
                preferred_categories=preferred_categories,
                used_product_ids=used_product_ids,
            )

            if product is None:
                break

            used_product_ids.add(product["product_id"])

            quantity_max = SEGMENT_QUANTITY_MAX.get(segment, 2)
            quantity = random.randint(1, quantity_max)

            unit_price = round(
                product["unit_price"] * random.uniform(0.95, 1.05),
                2
            )

            order_items.append({
                "order_item_id": order_item_id,
                "order_id": order["order_id"],
                "product_id": product["product_id"],
                "quantity": quantity,
                "unit_price": unit_price,
            })
            order_item_id += 1

    return order_items
