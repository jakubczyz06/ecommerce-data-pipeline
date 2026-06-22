"""
Generator tabeli: orders

Kolumny docelowe:
  order_id | client_id | order_date | order_status

Logika:
  - Liczba zamówień per klient wynika z segmentu (config.SEGMENTS).
  - Całkowita liczba zamówień jest skalowana do target_orders.
  - Klienci Dormant mają zamówienia starsze niż DORMANT_CUTOFF_DAYS.
"""

import random
from datetime import datetime, timedelta
from faker import Faker
from ecommerce_generator.config import (
    FAKER_LOCALE,
    SEGMENTS,
    DORMANT_CUTOFF_DAYS,
    ORDER_STATUSES,
    ORDER_STATUS_WEIGHTS,
    ORDER_START_DATE,
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
    """
    if target_orders < len(counts):
        raise ValueError("target_orders must be >= number of clients")

    adjusted = [max(1, c) for c in counts]
    diff = target_orders - sum(adjusted)

    while diff != 0:
        if diff > 0:
            idx = random.randrange(len(adjusted))
            adjusted[idx] += 1
            diff -= 1
        else:
            reducible = [i for i, c in enumerate(adjusted) if c > 1]
            if not reducible:
                break
            idx = random.choice(reducible)
            adjusted[idx] -= 1
            diff += 1

    return adjusted


def _order_date(segment: str) -> datetime:
    """Zwraca datę zamówienia dopasowaną do segmentu klienta."""
    now = datetime.now()
    start_dt = datetime.fromisoformat(ORDER_START_DATE)

    if segment == "Dormant":
        end_dt = now - timedelta(days=DORMANT_CUTOFF_DAYS + 1)
        if end_dt <= start_dt:
            end_dt = start_dt + timedelta(days=1)
        return fake.date_time_between_dates(
            datetime_start=start_dt,
            datetime_end=end_dt
        )

    if segment == "VIP":
        start_dt = max(start_dt, now - timedelta(days=120))
    elif segment == "Regular":
        start_dt = max(start_dt, now - timedelta(days=365))
    else:  # Occasional
        start_dt = max(start_dt, now - timedelta(days=540))

    if start_dt >= now:
        start_dt = now - timedelta(days=7)

    return fake.date_time_between_dates(
        datetime_start=start_dt,
        datetime_end=now
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

        for _ in range(num_orders):
            orders.append({
                "order_id": order_id,
                "client_id": client["client_id"],
                "order_date": _order_date(segment).isoformat(),
                "order_status": random.choices(
                    ORDER_STATUSES,
                    weights=ORDER_STATUS_WEIGHTS,
                    k=1
                )[0],
            })
            order_id += 1

    return orders