"""
Generator tabeli: clients

Kolumny docelowe:
  client_id | full_name | gender | phone_number | email | registration_date

Uwaga:
  - `_segment` jest polem wewnętrznym — przekazywane do generatorów adresów
    i zamówień, ale odfiltrowywane przed zapisem do CSV w main.py.
"""

import random
import re
from faker import Faker

from ecommerce_generator.config import FAKER_LOCALE, SEGMENTS


fake = Faker(FAKER_LOCALE)

EMAIL_DOMAINS = ["gmail.com", "outlook.com", "yahoo.com", "icloud.com"]


def assign_segment() -> str:
    """Losuje segment klienta na podstawie wag z konfiguracji."""
    segments = list(SEGMENTS.keys())
    weights  = [SEGMENTS[s]["weight"] for s in segments]
    return random.choices(segments, weights=weights, k=1)[0]


def _build_email(first_name: str, last_name: str, client_id: int) -> str:
    """
    Buduje realistyczny, unikalny adres e-mail.
    client_id w local part gwarantuje unikalność nawet przy identycznym imieniu i nazwisku.
    """
    local_part = f"{first_name}.{last_name}.{client_id}".lower()
    local_part = re.sub(r"[^a-z0-9]+", ".", local_part).strip(".")
    domain     = random.choice(EMAIL_DOMAINS)
    return f"{local_part}@{domain}"


def generate_clients(n: int) -> list[dict]:
    """
    Generuje n klientów.

    Args:
        n: liczba klientów do wygenerowania

    Returns:
        Lista słowników reprezentujących wiersze tabeli clients.
        Pole `_segment` jest wewnętrzne i nie trafia do finalnego CSV.
    """
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
            "phone_number":      fake.phone_number(),
            "email":             _build_email(first_name, last_name, client_id),
            "registration_date": fake.date_between(
                start_date="-3y",
                end_date="-6m",
            ).isoformat(),
            "_segment": segment,
        })

    return clients
