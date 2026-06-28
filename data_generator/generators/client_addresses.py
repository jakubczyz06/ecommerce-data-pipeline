"""
Table generator: client_addresses

Target columns:
  address_id | client_id | country | state | city | postal_code |
  street | building_number | apartment_number | address_type

Logic:
  - Each client has a minimum of 1 address (billing).
  - VIP: 60% chance for a second address (shipping); other segments have less.
  - State is drawn from US_STATES, city - exclusively from the list of cities
    appropriate for that state (STATE_CITIES), which eliminates geographical
    inconsistencies, e.g. "New York, CA".
"""



# Imports
import random
from faker import Faker
from data_generator.config import FAKER_LOCALE, STATE_CITIES, US_STATES



# Faker configuration
fake = Faker(FAKER_LOCALE)





# Returns a consistent pair (state, city) - the city comes from the list for the given state
def _random_state_and_city() -> tuple[str, str]:
    state = random.choice(US_STATES)
    city  = random.choice(STATE_CITIES[state])
    return state, city





# Generating the fake customer's address
SECOND_ADDRESS_PROBABILITY: dict[str, float] = {
    "VIP":        0.60,
    "Regular":    0.25,
    "Occasional": 0.10,
    "Dormant":    0.05,
}

def generate_addresses(clients: list[dict]) -> list[dict]:
    addresses  = []
    address_id = 1

    for client in clients:
        segment             = client.get("_segment", "Regular")
        second_address_prob = SECOND_ADDRESS_PROBABILITY.get(segment, 0.10)
        num_addresses       = 2 if random.random() < second_address_prob else 1

        for idx in range(num_addresses):
            state, city = _random_state_and_city()

            if num_addresses == 1:
                addr_type = "billing_and_shipping"
            elif idx == 0:
                addr_type = "billing"
            else:
                addr_type = "shipping"

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
                "address_type": addr_type,
            })
            address_id += 1

    return addresses