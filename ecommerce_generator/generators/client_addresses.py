"""
Generator tabeli: client_addresses

Kolumny docelowe:
  address_id | client_id | country | state | city | postal_code |
  street | building_number | apartment_number | address_type

Logika:
  - Każdy klient ma minimum 1 adres (billing).
  - VIP: 60% szans na drugi adres (shipping); pozostałe segmenty mniej.
  - Stan jest losowany z US_STATES, miasto — wyłącznie z listy miast
    właściwej dla tego stanu (STATE_CITIES), co eliminuje niespójności
    geograficzne, np. "New York, CA".
"""

import random
from faker import Faker
from ecommerce_generator.config import FAKER_LOCALE, STATE_CITIES, US_STATES

fake = Faker(FAKER_LOCALE)

SECOND_ADDRESS_PROBABILITY: dict[str, float] = {
    "VIP":        0.60,
    "Regular":    0.25,
    "Occasional": 0.10,
    "Dormant":    0.05,
}


def _random_state_and_city() -> tuple[str, str]:
    """Zwraca spójną parę (stan, miasto) — miasto pochodzi z listy dla danego stanu."""
    state = random.choice(US_STATES)
    city  = random.choice(STATE_CITIES[state])
    return state, city


def generate_addresses(clients: list[dict]) -> list[dict]:
    """
    Generuje adresy dla listy klientów.

    Args:
        clients: lista wygenerowana przez generators/clients.py

    Returns:
        Lista słowników reprezentujących wiersze tabeli client_addresses.
    """
    addresses  = []
    address_id = 1

    for client in clients:
        segment             = client.get("_segment", "Regular")
        second_address_prob = SECOND_ADDRESS_PROBABILITY.get(segment, 0.10)
        num_addresses       = 2 if random.random() < second_address_prob else 1

        for idx in range(num_addresses):
            state, city = _random_state_and_city()

            addresses.append({
                "address_id":       address_id,
                "client_id":        client["client_id"],
                "country":          "United States",
                "state":            state,
                "city":             city,
                "postal_code":      fake.postcode(),
                "street":           fake.street_name(),
                "building_number":  str(random.randint(1, 9999)),
                "apartment_number": (
                    str(random.randint(1, 999)) if random.random() < 0.45 else None
                ),
                "address_type": "billing" if idx == 0 else "shipping",
            })
            address_id += 1

    return addresses
