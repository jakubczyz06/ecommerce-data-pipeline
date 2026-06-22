"""
Entry point generatora danych e-commerce.

Uruchomienie:
    python -m ecommerce_generator.main
"""

import csv
import os
import random

from faker import Faker

from ecommerce_generator.config import (
    CONFIG,
    MODE,
    OUTPUT_DIR,
    RANDOM_SEED,
)
from ecommerce_generator.generators.client_addresses import generate_addresses
from ecommerce_generator.generators.clients import generate_clients
from ecommerce_generator.generators.order_items import generate_order_items
from ecommerce_generator.generators.orders import generate_orders
from ecommerce_generator.generators.products import generate_products

# ── Seed — musi być ustawiony przed jakimkolwiek wywołaniem generatorów ────────
random.seed(RANDOM_SEED)
Faker.seed(RANDOM_SEED)


def _save_csv(rows: list[dict], filename: str) -> None:
    """Zapisuje listę słowników do pliku CSV."""
    if not rows:
        print(f"[WARN] Brak danych do zapisu: {filename}")
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = os.path.join(OUTPUT_DIR, filename)

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"[OK] {filename:35s} → {len(rows):>7,} wierszy")


def main() -> None:
    cfg = CONFIG[MODE]
    num_clients = cfg["num_clients"]
    num_products = cfg["num_products"]
    num_orders = cfg["num_orders"]

    print(f"Tryb: {MODE}  |  klienci={num_clients:,}  produkty={num_products:,}  zamówienia={num_orders:,}\n")

    clients = generate_clients(num_clients)
    addresses = generate_addresses(clients)
    products = generate_products(num_products)
    orders = generate_orders(clients, target_orders=num_orders)
    order_items = generate_order_items(orders, products, clients)

    # Usuń wewnętrzne pole _segment przed zapisem
    clients_export = [{k: v for k, v in c.items() if k != "_segment"} for c in clients]

    _save_csv(clients_export, "clients.csv")
    _save_csv(addresses,      "client_addresses.csv")
    _save_csv(products,        "products.csv")
    _save_csv(orders,          "orders.csv")
    _save_csv(order_items,     "order_items.csv")

    print("\nGotowe.")


if __name__ == "__main__":
    main()
