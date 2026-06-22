"""
Generator tabeli: client_addresses

Kolumny docelowe:
  client_id | address_id | country | city | postal_code |
  street | building_number | apartment_number | address_type

Logika:
  - Każdy klient ma minimum 1 adres.
  - VIP ma 60% szans na 2. adres.
  - Pozostałe segmenty mają mniejszą szansę na drugi adres.
  - address_type: billing / shipping
"""

import random
from faker import Faker
from ecommerce_generator.config import FAKER_LOCALE

fake = Faker(FAKER_LOCALE)

SECOND_ADDRESS_PROBABILITY = {
    "VIP": 0.60,
    "Regular": 0.25,
    "Occasional": 0.10,
    "Dormant": 0.05,
}


def generate_addresses(clients: list[dict]) -> list[dict]:
    """
    Generuje adresy dla listy klientów.

    Args:
        clients: lista wygenerowana przez generators/clients.py

    Returns:
        Lista słowników reprezentujących wiersze tabeli client_addresses.
    """
    addresses = []
    address_id = 1

    for client in clients:
        segment = client.get("_segment", "Regular")
        second_address_prob = SECOND_ADDRESS_PROBABILITY.get(segment, 0.10)
        num_addresses = 2 if random.random() < second_address_prob else 1

        for idx in range(num_addresses):
            addresses.append({
                "address_id": address_id,
                "client_id": client["client_id"],
                "country": "United States",
                "city": fake.city(),
                "postal_code": fake.postcode(),
                "street": fake.street_name(),
                "building_number": str(random.randint(1, 9999)),
                "apartment_number": (
                    str(random.randint(1, 999))
                    if random.random() < 0.45
                    else None
                ),
                "address_type": "billing" if idx == 0 else "shipping",
            })
            address_id += 1

    return addresses