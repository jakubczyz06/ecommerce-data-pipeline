"""
Generator tabeli: orders

Kolumny docelowe:
  order_id | client_id | order_date | order_status

Logika:
  - Liczba zamówień per klient wynika z segmentu (config.SEGMENTS).
  - Całkowita liczba zamówień jest skalowana do target_orders.
  - Klienci Dormant mają zamówienia starsze niż DORMANT_CUTOFF_DAYS.
  - order_date jest zawsze >= registration_date klienta.
"""

import random
from datetime import datetime, timedelta

import numpy as np
from faker import Faker

from ecommerce_generator.config import (
    DORMANT_CUTOFF_DAYS,
    FAKER_LOCALE,
    ORDER_START_DATE,
    ORDER_STATUSES,
    ORDER_STATUS_WEIGHTS,
    SEGMENTS,
)

fake = Faker(FAKER_LOCALE)


def _raw_order_counts(clients: list[dict]) -> list[int]:
    """Oblicza surową liczbę zamówień per klient (przed skalowaniem)."""
    counts = []
    for client in clients:
        segment = client.get("_segment", "Regular")
        lo, hi = SEGMENTS[segment]["orders_range"]
        counts.append(random.randint(lo, hi))
    return counts


def _adjust_counts_to_target(counts: list[int], target_orders: int) -> list[int]:
    """
    Dopasowuje listę counts tak, aby ich suma była równa target_orders.
    Używa numpy dla wydajności przy dużych zbiorach (tryb LARGE).
    """
    if target_orders < len(counts):
        raise ValueError("target_orders must be >= number of clients")

    arr = np.maximum(np.array(counts, dtype=np.int64), 1)
    diff = int(target_orders - arr.sum())

    if diff != 0:
        indices = np.random.choice(len(arr), size=abs(diff), replace=True)
        np.add.at(arr, indices, 1 if diff > 0 else -1)
        arr = np.maximum(arr, 1)

    return arr.tolist()


def _order_date(segment: str, registered_since: str) -> datetime:
    """
    Zwraca datę zamówienia dopasowaną do segmentu klienta.
    Gwarantuje, że data zamówienia nie jest wcześniejsza niż rejestracja klienta.

    Args:
        segment:          segment klienta
        registered_since: data rejestracji w formacie ISO (YYYY-MM-DD)
    """
    now = datetime.now()
    registration_dt = datetime.fromisoformat(registered_since)
    start_dt = datetime.fromisoformat(ORDER_START_DATE)

    if segment == "Dormant":
        end_dt = now - timedelta(days=DORMANT_CUTOFF_DAYS + 1)
        if end_dt <= start_dt:
            end_dt = start_dt + timedelta(days=1)
        # Nie generuj zamówienia przed rejestracją klienta
        effective_start = max(start_dt, registration_dt)
        if effective_start >= end_dt:
            effective_start = end_dt - timedelta(days=1)
        return fake.date_time_between_dates(
            datetime_start=effective_start,
            datetime_end=end_dt,
        )

    if segment == "VIP":
        start_dt = max(start_dt, now - timedelta(days=120))
    elif segment == "Regular":
        start_dt = max(start_dt, now - timedelta(days=365))
    else:  # Occasional
        start_dt = max(start_dt, now - timedelta(days=540))

    # Nie generuj zamówienia przed rejestracją klienta
    start_dt = max(start_dt, registration_dt)

    if start_dt >= now:
        start_dt = now - timedelta(days=7)

    return fake.date_time_between_dates(
        datetime_start=start_dt,
        datetime_end=now,
    )


def generate_orders(clients: list[dict], target_orders: int) -> list[dict]:
    """
    Generuje zamówienia dla wszystkich klientów.

    Args:
        clients:       lista z generators/clients.py
        target_orders: docelowa liczba zamówień

    Returns:
        Lista słowników reprezentujących wiersze tabeli orders.
    """
    raw_counts = _raw_order_counts(clients)
    counts = _adjust_counts_to_target(raw_counts, target_orders)

    orders = []
    order_id = 1

    for client, num_orders in zip(clients, counts):
        segment = client.get("_segment", "Regular")
        registered_since = client["registration_date"]

        for _ in range(num_orders):
            orders.append({
                "order_id": order_id,
                "client_id": client["client_id"],
                "order_date": _order_date(segment, registered_since).isoformat(),
                "order_status": random.choices(
                    ORDER_STATUSES,
                    weights=ORDER_STATUS_WEIGHTS,
                    k=1,
                )[0],
            })
            order_id += 1

    return orders
