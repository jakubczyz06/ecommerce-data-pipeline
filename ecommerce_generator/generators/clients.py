"""
Table generator: clients

Target columns:
  client_id | full_name | gender | phone_number | email | registration_date

Note:
  - `_segment` is an internal field - passed to the addresses and orders generators,
    but filtered out before saving to CSV in main.py.
"""



# Imports
import random
import re
from faker import Faker

from ecommerce_generator.config import FAKER_LOCALE, SEGMENTS





# Faker configuration
fake = Faker(FAKER_LOCALE)





# Client assignation
def assign_segment() -> str:
    """Randomly assigns a client segment based on configuration weights"""
    segments = list(SEGMENTS.keys())
    weights  = [SEGMENTS[s]["weight"] for s in segments]
    return random.choices(segments, weights = weights, k = 1)[0]





# Creation of the fake customer's email
EMAIL_DOMAINS = ["gmail.com", "outlook.com", "yahoo.com", "icloud.com"]

def _build_email(first_name: str, last_name: str, client_id: int) -> str:
    local_part = f"{first_name}.{last_name}.{client_id}".lower()
    local_part = re.sub(r"[^a-z0-9]+", ".", local_part).strip(".")
    domain     = random.choice(EMAIL_DOMAINS)
    return f"{local_part}@{domain}"





# Fake customer generation
def generate_clients(n: int) -> list[dict]:
    clients = []

    for client_id in range(1, n + 1):
        segment    = assign_segment()
        gender     = random.choice(["Male", "Female"])
        first_name = fake.first_name_male() if gender == "Male" else fake.first_name_female()
        last_name  = fake.last_name()

        clients.append({
            "client_id":         client_id,
            "full_name":         f"{first_name} {last_name}",
            "gender":            gender,
            "phone_number":      fake.numerify("(###) ###-####"),
            "email":             _build_email(first_name, last_name, client_id),
            "registration_date": fake.date_between(
                start_date = "-3y",
                end_date = "-6m",
            ).isoformat(),
            "_segment": segment,
        })

    return clients