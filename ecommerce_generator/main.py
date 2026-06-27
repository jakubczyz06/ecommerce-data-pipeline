"""
Operational file of generating synthetic data
"""



# Imports
import argparse
import csv
import logging
import os
import random
import time
import sys
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





# Logger configuration
LOG_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "ecommerce_generator.log",
)

logger = logging.getLogger("ecommerce_generator")
logger.setLevel(logging.INFO)

# Prevent duplicate handlers
if not logger.handlers:
    file_handler = logging.FileHandler(
        LOG_PATH,
        mode="a",
        encoding="utf-8",
    )

    # Stream handler Docker/Console
    stream_handler = logging.StreamHandler(sys.stdout)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M",
    )

    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)





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

    while True:
        raw = input("Your choice (1 / 2 / 3): ").strip()

        if raw in ("1", "2", "3"):
            print()
            return VALID_MODES[int(raw) - 1]

        print("Invalid option. Please enter 1, 2 or 3.")





# CSV export
def _save_csv(rows: list[dict], filename: str) -> None:
    """Save a list of dictionaries as a CSV file."""

    if not rows:
        logger.warning("No data to save: %s", filename)
        return

    os.makedirs(OUTPUT_DIR, exist_ok = True)
    path = os.path.join(OUTPUT_DIR, filename)

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

    # Select mode from CLI or interactive prompt
    mode = args.mode or _ask_mode()
    seed = args.seed if args.seed is not None else RANDOM_SEED

    cfg = CONFIG[mode]

    num_clients = cfg["num_clients"]
    num_products = cfg["num_products"]
    num_orders = cfg["num_orders"]

    # Set random seed BEFORE generating any data
    random.seed(seed)
    Faker.seed(seed)

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

    # Internal field used only during generation
    clients_export = [
        {k: v for k, v in client.items() if k != "_segment"}
        for client in clients
    ]

    _save_csv(clients_export, "clients.csv")
    _save_csv(addresses, "client_addresses.csv")
    _save_csv(products, "products.csv")
    _save_csv(orders, "orders.csv")
    _save_csv(order_items, "order_items.csv")

    elapsed = time.perf_counter() - start_time

    logger.info(
        "Generation completed in %.2f seconds.",
        elapsed,
    )
    logger.info("Output directory: %s/", OUTPUT_DIR)





if __name__ == "__main__":
    main()