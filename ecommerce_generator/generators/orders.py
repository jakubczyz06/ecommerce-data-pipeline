"""
Table generator: orders

Target columns:
  order_id | client_id | order_date | order_status

Logic:
  - The number of orders per client depends on the segment (SEGMENTS.orders_range).
  - The total number of orders is scaled to target_orders via _adjust_counts_to_target.
  - Dormant clients have orders older than DORMANT_CUTOFF_DAYS.
  - order_date is always >= client's registration_date (temporal consistency).

Date logic per segment:
  - VIP       → orders from the last 120 days (active, fresh transactions)
  - Regular   → orders from the last 365 days
  - Occasional → orders from the last 540 days
  - Dormant   → orders FROM BEFORE DORMANT_CUTOFF_DAYS days (inactive)
"""



# Imports
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





# Faker configuration
fake = Faker(FAKER_LOCALE)





# Drawing a raw number of orders per client (before scaling to the target)
def _raw_order_counts(clients: list[dict]) -> list[int]:
    counts = []
    for client in clients:
        segment = client.get("_segment", "Regular")
        lo, hi  = SEGMENTS[segment]["orders_range"]
        counts.append(random.randint(lo, hi))
    return counts





# Scaling the counts list
def _adjust_counts_to_target(counts: list[int], target_orders: int) -> list[int]:
    if target_orders < len(counts):
        raise ValueError(
            f"target_orders ({target_orders}) must be >= number of clients ({len(counts)})"
        )

    arr  = np.maximum(np.array(counts, dtype = np.int64), 1)
    diff = int(target_orders - arr.sum())

    if diff != 0:
        indices = np.random.choice(len(arr), size=abs(diff), replace=True)
        np.add.at(arr, indices, 1 if diff > 0 else -1)
        arr = np.maximum(arr, 1)  # safeguard against dropping to 0

    return arr.tolist()





# Returning an order date consistent with the segment and the client's registration
# in ISO format
def _order_date(segment: str, registered_since: str) -> datetime:
    now             = datetime.now()
    registration_dt = datetime.fromisoformat(registered_since)
    start_dt        = datetime.fromisoformat(ORDER_START_DATE)

    if segment == "Dormant":
        # Order must be older than DORMANT_CUTOFF_DAYS
        end_dt = now - timedelta(days=DORMANT_CUTOFF_DAYS + 1)
        if end_dt <= start_dt:
            end_dt = start_dt + timedelta(days=1)
        effective_start = max(start_dt, registration_dt)
        if effective_start >= end_dt:
            effective_start = end_dt - timedelta(days=1)
        return fake.date_time_between_dates(
            datetime_start=effective_start,
            datetime_end=end_dt,
        )

    # Active segments - lookback window depends on the segment
    lookback = {"VIP": 120, "Regular": 365, "Occasional": 540}
    days_back = lookback.get(segment, 365)
    start_dt  = max(start_dt, now - timedelta(days=days_back))

    # Do not go back before the client's registration date
    start_dt = max(start_dt, registration_dt)

    if start_dt >= now:
        start_dt = now - timedelta(days=7)

    return fake.date_time_between_dates(
        datetime_start=start_dt,
        datetime_end=now,
    )





# Generating the fake orders
def generate_orders(clients: list[dict], target_orders: int) -> list[dict]:
    raw_counts = _raw_order_counts(clients)
    counts     = _adjust_counts_to_target(raw_counts, target_orders)

    orders   = []
    order_id = 1

    for client, num_orders in zip(clients, counts):
        segment          = client.get("_segment", "Regular")
        registered_since = client["registration_date"]

        for _ in range(num_orders):
            orders.append({
                "order_id":     order_id,
                "client_id":    client["client_id"],
                "order_date":   _order_date(segment, registered_since).isoformat(),
                "order_status": random.choices(
                    ORDER_STATUSES,
                    weights=ORDER_STATUS_WEIGHTS,
                    k = 1,
                )[0],
            })
            order_id += 1

    return orders