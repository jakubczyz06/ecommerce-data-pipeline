"""
Operational file of generating synthetic data
"""



# Imports
import argparse
import csv
import random
import time
import numpy as np
from faker import Faker

from config import (
    CONFIG,
    RANDOM_SEED,
)
from utils.logger import get_logger
from utils.paths import DATA_DIR
from generators.client_addresses import generate_addresses
from generators.clients import generate_clients
from generators.order_items import generate_order_items
from generators.orders import generate_orders
from generators.products import generate_products





# Logger for "data_generator" module
logger = get_logger("generator")





# Subdirectory for file generator
GENERATOR_OUT = DATA_DIR / "generated_data"
GENERATOR_OUT.mkdir(exist_ok = True)





# Command-line interface
VALID_MODES = list(CONFIG.keys())

def _parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description = "Synthetic e-commerce data generator.",
        formatter_class = argparse.RawTextHelpFormatter,
    )

    parser.add_argument(
        "--mode",
        choices = VALID_MODES,
        metavar = "MODE",
        help = "Generation mode: " + " | ".join(VALID_MODES),
    )

    parser.add_argument(
        "--seed",
        type = int,
        default = None,
        metavar = "N",
        help = f"Random seed (default: {RANDOM_SEED})",
    )

    return parser.parse_args()


def _ask_mode() -> str:
    """Ask the user to choose a generation mode interactively."""
    print("E-commerce Data Generator")
    print("Choose generation mode:\n")

    for i, mode in enumerate(VALID_MODES, start=1):
        label = CONFIG[mode]["label"]
        print(f"[{i}] {label}")

    print()

    valid = [str(i) for i in range(1, len(VALID_MODES) + 1)]

    while True:
        raw = input(f"Your choice ({' / '.join(valid)}): ").strip()

        if raw in valid:
            print()
            return VALID_MODES[int(raw) - 1]

        print(f"Invalid option. Please enter {' or '.join(valid)}.")





# CSV export
def _save_csv(rows: list[dict], filename: str) -> None:
    """Save a list of dictionaries as a CSV file."""

    if not rows:
        logger.warning("No data to save: %s", filename)
        return

    path = GENERATOR_OUT / filename

    with open(path, "w", newline = "", encoding = "utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    logger.info(
        "%-30s -> %7s rows (%s)",
        filename,
        f"{len(rows):,}",
        path,
    )




# Main application
def main() -> None:
    """Run the complete data generation pipeline."""

    args = _parse_args()

    mode = args.mode or _ask_mode()
    seed = args.seed if args.seed is not None else RANDOM_SEED

    cfg = CONFIG[mode]

    num_clients  = cfg["num_clients"]
    num_products = cfg["num_products"]
    num_orders   = cfg["num_orders"]

    random.seed(seed)
    Faker.seed(seed)
    np.random.seed(seed)

    logger.info("Generation mode: %s | Seed: %d", mode, seed)
    logger.info(
        "Target dataset: %s clients | %s products | %s orders",
        f"{num_clients:,}",
        f"{num_products:,}",
        f"{num_orders:,}",
    )

    start_time = time.perf_counter()

    logger.info("Generating clients...")
    clients = generate_clients(num_clients)

    logger.info("Generating client addresses...")
    addresses = generate_addresses(clients)

    logger.info("Generating products...")
    products = generate_products(num_products)

    logger.info("Generating orders...")
    orders = generate_orders(
        clients,
        target_orders = num_orders,
    )

    logger.info("Generating order items...")
    order_items = generate_order_items(
        orders,
        products,
        clients,
    )

    logger.info("Exporting CSV files...")

    clients_export = [
        {k: v for k, v in client.items() if k != "_segment"}
        for client in clients
    ]

    _save_csv(clients_export,  "clients.csv")
    _save_csv(addresses,       "client_addresses.csv")
    _save_csv(products,        "products.csv")
    _save_csv(orders,          "orders.csv")
    _save_csv(order_items,     "order_items.csv")

    elapsed = time.perf_counter() - start_time

    logger.info("Generation completed in %.2f seconds.", elapsed)
    logger.info("Output directory: %s/", GENERATOR_OUT)


if __name__ == "__main__":
    main()
