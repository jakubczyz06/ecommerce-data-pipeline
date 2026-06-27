"""
Entry point generatora danych e-commerce.

Uruchomienie (interaktywny wybór trybu):
    python -m ecommerce_generator.main

Uruchomienie z argumentem:
    python -m ecommerce_generator.main --mode LARGE
    python -m ecommerce_generator.main --mode SMALL --seed 123
"""

import argparse
import csv
import logging
import os
import random
import sys
import time

from faker import Faker

from ecommerce_generator.config import (
    CONFIG,
    OUTPUT_DIR,
    RANDOM_SEED,
)
from ecommerce_generator.generators.client_addresses import generate_addresses
from ecommerce_generator.generators.clients import generate_clients
from ecommerce_generator.generators.order_items import generate_order_items
from ecommerce_generator.generators.orders import generate_orders
from ecommerce_generator.generators.products import generate_products

# ── Logger ────────────────────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("ecommerce_generator")


# ── CLI ───────────────────────────────────────────────────────────────────────

VALID_MODES = list(CONFIG.keys())  # ["SMALL", "MEDIUM", "LARGE"]


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generator syntetycznych danych e-commerce.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "--mode",
        choices=VALID_MODES,
        metavar="MODE",
        help="Tryb generowania: " + " | ".join(VALID_MODES),
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        metavar="N",
        help=f"Seed losowości (domyślnie: {RANDOM_SEED})",
    )
    return parser.parse_args()


def _ask_mode() -> str:
    """Interaktywny wybór trybu gdy nie podano --mode."""
    print("\n╔══════════════════════════════════════════════════════╗")
    print("║        Generator danych e-commerce  🛒               ║")
    print("╚══════════════════════════════════════════════════════╝\n")
    print("Wybierz tryb generowania:\n")

    for i, mode in enumerate(VALID_MODES, start=1):
        label = CONFIG[mode]["label"]
        print(f"  [{i}] {label}")

    print()

    while True:
        raw = input("Twój wybór (1 / 2 / 3): ").strip()
        if raw in ("1", "2", "3"):
            chosen = VALID_MODES[int(raw) - 1]
            print()
            return chosen
        print("  Nieprawidłowy wybór — wpisz 1, 2 lub 3.")


# ── Zapis CSV ─────────────────────────────────────────────────────────────────

def _save_csv(rows: list[dict], filename: str) -> None:
    """Zapisuje listę słowników do pliku CSV w katalogu OUTPUT_DIR."""
    if not rows:
        log.warning("Brak danych do zapisu: %s", filename)
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = os.path.join(OUTPUT_DIR, filename)

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    log.info("%-30s →  %7s wierszy  (%s)", filename, f"{len(rows):,}", path)


# ── Główna logika ─────────────────────────────────────────────────────────────

def main() -> None:
    args = _parse_args()

    # Wybór trybu — argument lub interaktywny prompt
    mode = args.mode or _ask_mode()
    seed = args.seed if args.seed is not None else RANDOM_SEED

    cfg = CONFIG[mode]
    num_clients  = cfg["num_clients"]
    num_products = cfg["num_products"]
    num_orders   = cfg["num_orders"]

    # ── Seed musi być ustawiony PRZED pierwszym wywołaniem generatorów ────────
    random.seed(seed)
    Faker.seed(seed)

    log.info("Tryb: %s  |  seed: %d", mode, seed)
    log.info("Docelowo: %s klientów, %s produktów, %s zamówień",
             f"{num_clients:,}", f"{num_products:,}", f"{num_orders:,}")
    print()

    t_start = time.perf_counter()

    log.info("Generowanie klientów...")
    clients = generate_clients(num_clients)

    log.info("Generowanie adresów...")
    addresses = generate_addresses(clients)

    log.info("Generowanie produktów...")
    products = generate_products(num_products)

    log.info("Generowanie zamówień...")
    orders = generate_orders(clients, target_orders=num_orders)

    log.info("Generowanie pozycji zamówień...")
    order_items = generate_order_items(orders, products, clients)

    print()
    log.info("Zapis do CSV...")

    # _segment to pole wewnętrzne — nie trafia do pliku
    clients_export = [{k: v for k, v in c.items() if k != "_segment"} for c in clients]

    _save_csv(clients_export, "clients.csv")
    _save_csv(addresses,      "client_addresses.csv")
    _save_csv(products,       "products.csv")
    _save_csv(orders,         "orders.csv")
    _save_csv(order_items,    "order_items.csv")

    elapsed = time.perf_counter() - t_start
    print()
    log.info("Gotowe w %.1f s  →  katalog: %s/", elapsed, OUTPUT_DIR)


if __name__ == "__main__":
    main()
