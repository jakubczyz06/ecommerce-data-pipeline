"""
Centralna konfiguracja generatora danych e-commerce.

Sklep: elektronika użytkowa (USA)
Język: en_US

Zmień MODE na "LARGE" gdy testy przejdą pomyślnie.
"""

# ── Język Fakera — jedna zmiana dotyczy wszystkich generatorów ────────────────

FAKER_LOCALE = "en_US"

# ── Tryb generowania ──────────────────────────────────────────────────────────

MODE = "SMALL"   # "SMALL" | "LARGE"

CONFIG = {
    "SMALL": {
        "num_clients": 100,
        "num_products": 20,
        "num_orders": 500,
    },
    "LARGE": {
        "num_clients": 5_000,
        "num_products": 300,
        "num_orders": 50_000,
    },
}

# ── Katalog wyjściowy ─────────────────────────────────────────────────────────

OUTPUT_DIR = "ecommerce_data"

# ── Seed dla powtarzalności ───────────────────────────────────────────────────

RANDOM_SEED = 42

# ── Zakresy dat ───────────────────────────────────────────────────────────────

PRODUCT_START_DATE = "2020-01-01"
ORDER_START_DATE = "2022-01-01"

# ── Waluta ────────────────────────────────────────────────────────────────────

CURRENCY = "USD"

# ── Segmenty klientów ─────────────────────────────────────────────────────────

SEGMENTS = {
    "VIP": {
        "weight": 0.10,
        "orders_range": (15, 40),
        "avg_spend_multiplier": 2.5,
        "basket_range": (500, 4000),
        "dormant": False,
    },
    "Regular": {
        "weight": 0.25,
        "orders_range": (5, 15),
        "avg_spend_multiplier": 1.2,
        "basket_range": (150, 1200),
        "dormant": False,
    },
    "Occasional": {
        "weight": 0.40,
        "orders_range": (2, 5),
        "avg_spend_multiplier": 0.8,
        "basket_range": (30, 500),
        "dormant": False,
    },
    "Dormant": {
        "weight": 0.25,
        "orders_range": (1, 2),
        "avg_spend_multiplier": 0.6,
        "basket_range": (20, 200),
        "dormant": True,
    },
}

DORMANT_CUTOFF_DAYS = 180

SEGMENT_CATEGORY_PREFERENCES = {
    "VIP": [
        "Smartphones",
        "Laptops",
        "Smartwatches & Wearables",
        "Cameras",
    ],
    "Regular": [
        "Smartphones",
        "Laptops",
        "Headphones & Audio",
        "Gaming",
    ],
    "Occasional": [
        "Accessories & Cables",
        "Headphones & Audio",
        "Smart Home",
    ],
    "Dormant": [
        "Accessories & Cables",
        "Headphones & Audio",
    ],
}

# ── Statusy zamówień (z wagami) ───────────────────────────────────────────────

ORDER_STATUSES = ["completed", "shipped", "processing", "cancelled"]
ORDER_STATUS_WEIGHTS = [60, 20, 15, 5]

# ── Dodatkowe zakresy dla zamówień ────────────────────────────────────────────

ORDER_ITEMS_PER_ORDER = (1, 5)
QUANTITY_RANGE = (1, 3)

# ── Lista stanów USA ──────────────────────────────────────────────────────────

US_STATES = [
    "CA", "TX", "FL", "NY", "IL",
    "PA", "OH", "GA", "NC", "MI",
    "NJ", "VA", "WA", "AZ", "MA",
    "TN", "IN", "MO", "MD", "WI",
]

# ── Katalog produktów elektronicznych ────────────────────────────────────────
#
# Struktura każdej kategorii:
#
# "brands"    → marki charakterystyczne dla tej kategorii
# "templates" → szablony nazw produktów
# {brand}     → zastępowane losową marką z listy "brands"
# {model}     → zastępowane losowym kodem modelu (np. "X-490")
# {size}      → zastępowane losowym rozmiarem ekranu (np. '15.6"')
# {color}     → zastępowane losowym kolorem
# "price_range" → (min, max) w USD
#
# Szablony bez {brand} to produkty, gdzie marka nie wchodzi w nazwę
# (np. akcesoria typu "USB-C Cable 6ft").

CATALOG: dict[str, dict] = {
    "Smartphones": {
        "brands": ["Apple", "Samsung", "Google", "OnePlus", "Motorola"],
        "templates": [
            "{brand} {model} 5G",
            "{brand} {model} Pro",
            "{brand} {model} Ultra",
            "{brand} {model} Plus",
        ],
        "price_range": (299, 1_399),
    },
    "Laptops": {
        "brands": ["Apple", "Dell", "HP", "Lenovo", "ASUS", "Microsoft"],
        "templates": [
            '{brand} {model} {size} Laptop',
            '{brand} {model} Pro {size}',
            "{brand} {model} Gaming Laptop",
            '{brand} {model} Ultrabook {size}',
        ],
        "price_range": (499, 3_499),
    },
    "Tablets": {
        "brands": ["Apple", "Samsung", "Microsoft", "Lenovo", "Amazon"],
        "templates": [
            '{brand} {model} {size} Tablet',
            "{brand} {model} Tab",
            "{brand} {model} Tab Pro",
        ],
        "price_range": (149, 1_299),
    },
    "Headphones & Audio": {
        "brands": ["Sony", "Bose", "Apple", "Sennheiser", "JBL", "Jabra"],
        "templates": [
            "{brand} {model} Wireless Headphones",
            "{brand} {model} Noise-Cancelling Headphones",
            "{brand} {model} True Wireless Earbuds",
            "{brand} {model} Over-Ear Headphones",
            "{brand} {model} In-Ear Monitors",
        ],
        "price_range": (29, 599),
    },
    "Smartwatches & Wearables": {
        "brands": ["Apple", "Samsung", "Garmin", "Fitbit", "Fossil"],
        "templates": [
            "{brand} {model} Smartwatch",
            "{brand} {model} Sport Watch",
            "{brand} {model} Fitness Tracker",
            "{brand} {model} GPS Watch",
        ],
        "price_range": (79, 899),
    },
    "Cameras": {
        "brands": ["Sony", "Canon", "Nikon", "Fujifilm", "Panasonic"],
        "templates": [
            "{brand} {model} Mirrorless Camera",
            "{brand} {model} DSLR Camera",
            "{brand} {model} Point & Shoot Camera",
            "{brand} {model} Action Camera",
        ],
        "price_range": (199, 3_999),
    },
    "TVs & Displays": {
        "brands": ["Samsung", "LG", "Sony", "TCL", "Hisense"],
        "templates": [
            '{brand} {model} {size} 4K OLED TV',
            '{brand} {model} {size} QLED TV',
            '{brand} {model} {size} 4K Smart TV',
            '{brand} {model} {size} Monitor',
            '{brand} {model} {size} Curved Gaming Monitor',
        ],
        "price_range": (199, 4_999),
    },
    "Gaming": {
        "brands": ["Sony", "Microsoft", "Nintendo", "Razer", "SteelSeries", "Logitech"],
        "templates": [
            "{brand} {model} Gaming Controller",
            "{brand} {model} Gaming Headset",
            "{brand} {model} Mechanical Keyboard",
            "{brand} {model} Gaming Mouse",
            "{brand} {model} Gaming Chair",
        ],
        "price_range": (29, 799),
    },
    "Smart Home": {
        "brands": ["Amazon", "Google", "Apple", "Philips", "Ring", "Nest"],
        "templates": [
            "{brand} {model} Smart Speaker",
            "{brand} {model} Smart Display",
            "{brand} {model} Smart Thermostat",
            "{brand} {model} Security Camera",
            "{brand} {model} Video Doorbell",
            "{brand} Smart Bulb {model}",
        ],
        "price_range": (19, 499),
    },
    "Accessories & Cables": {
        "brands": ["Anker", "Belkin", "Apple", "Samsung", "Logitech", "Spigen"],
        "templates": [
            "{brand} USB-C Cable 6ft",
            "{brand} {model} Wireless Charger",
            "{brand} {model} Power Bank",
            "{brand} {model} Phone Case",
            "{brand} {model} Screen Protector",
            "{brand} {model} Laptop Stand",
            "{brand} USB-C Hub {model}",
        ],
        "price_range": (5, 99),
    },
}

# Kolory używane w szablonach produktów ({color})

PRODUCT_COLORS = [
    "Midnight Black",
    "Arctic White",
    "Silver",
    "Space Gray",
    "Navy Blue",
    "Rose Gold",
    "Graphite",
    "Starlight",
]

# Rozmiary ekranów używane w szablonach ({size})

SCREEN_SIZES = [
    '13"',
    '14"',
    '15.6"',
    '16"',
    '24"',
    '27"',
    '32"',
    '43"',
    '55"',
    '65"',
    '75"',
]
