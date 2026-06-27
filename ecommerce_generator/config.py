"""
Centralna konfiguracja generatora danych e-commerce.

Sklep: elektronika użytkowa (USA)
Język: en_US
"""

# ── Język Fakera ──────────────────────────────────────────────────────────────

FAKER_LOCALE = "en_US"

# ── Tryby generowania ─────────────────────────────────────────────────────────
#
# MODE nie jest tu hardcodowany — wybierany interaktywnie przez CLI w main.py.
# Możesz też podać go jako argument: python -m ecommerce_generator.main --mode LARGE

CONFIG = {
    "SMALL": {
        "label": "Small  —  100 klientów / 20 produktów / 500 zamówień",
        "num_clients":  100,
        "num_products":  20,
        "num_orders":   500,
    },
    "MEDIUM": {
        "label": "Medium — 1 000 klientów / 100 produktów / 8 000 zamówień",
        "num_clients":  1_000,
        "num_products":   100,
        "num_orders":   8_000,
    },
    "LARGE": {
        "label": "Large  — 5 000 klientów / 300 produktów / 50 000 zamówień",
        "num_clients":  5_000,
        "num_products":   300,
        "num_orders":  50_000,
    },
}

# ── Katalog wyjściowy ─────────────────────────────────────────────────────────

OUTPUT_DIR = "data"

# ── Seed dla powtarzalności ───────────────────────────────────────────────────
#
# Seed jest ustawiany PRZED wywołaniem jakiegokolwiek generatora (w main.py).
# Dzięki temu ten sam seed zawsze daje identyczny zestaw danych.

RANDOM_SEED = 42

# ── Zakresy dat ───────────────────────────────────────────────────────────────
#
# PRODUCT_START_DATE  — najwcześniejsza możliwa data dodania produktu do sklepu
# ORDER_START_DATE    — najwcześniejsza możliwa data złożenia zamówienia

PRODUCT_START_DATE = "2020-01-01"
ORDER_START_DATE   = "2022-01-01"

# ── Waluta ────────────────────────────────────────────────────────────────────

CURRENCY = "USD"

# ── Segmenty klientów ─────────────────────────────────────────────────────────
#
# weight        — prawdopodobieństwo przypisania segmentu nowemu klientowi
# orders_range  — (min, max) liczby zamówień przed skalowaniem do target_orders
# dormant       — czy segment jest traktowany jako nieaktywny

SEGMENTS = {
    "VIP": {
        "weight":       0.10,
        "orders_range": (15, 40),
        "dormant":      False,
    },
    "Regular": {
        "weight":       0.25,
        "orders_range": (5, 15),
        "dormant":      False,
    },
    "Occasional": {
        "weight":       0.40,
        "orders_range": (2, 5),
        "dormant":      False,
    },
    "Dormant": {
        "weight":       0.25,
        "orders_range": (1, 2),
        "dormant":      True,
    },
}

# Klient Dormant nie złożył zamówienia od co najmniej N dni
DORMANT_CUTOFF_DAYS = 180

# Preferowane kategorie produktów per segment — wpływają na dobór pozycji w zamówieniu
SEGMENT_CATEGORY_PREFERENCES = {
    "VIP":        ["Smartphones", "Laptops", "Smartwatches & Wearables", "Cameras"],
    "Regular":    ["Smartphones", "Laptops", "Headphones & Audio", "Gaming"],
    "Occasional": ["Accessories & Cables", "Headphones & Audio", "Smart Home"],
    "Dormant":    ["Accessories & Cables", "Headphones & Audio"],
}

# ── Statusy zamówień ──────────────────────────────────────────────────────────

ORDER_STATUSES      = ["completed", "shipped", "processing", "cancelled"]
ORDER_STATUS_WEIGHTS = [60, 20, 15, 5]

# ── Geografia: stany i miasta USA ─────────────────────────────────────────────
#
# Słownik STATE_CITIES mapuje skrót stanu → lista rzeczywistych miast.
# W client_addresses.py miasto jest losowane wyłącznie z listy właściwej dla stanu,
# co eliminuje absurdy typu "New York, CA".
#
# Pokryte stany: wszystkie 20 z listy US_STATES (10–15 miast każdy).

STATE_CITIES: dict[str, list[str]] = {
    "CA": [
        "Los Angeles", "San Diego", "San Jose", "San Francisco", "Fresno",
        "Sacramento", "Long Beach", "Oakland", "Bakersfield", "Anaheim",
        "Santa Ana", "Riverside", "Stockton", "Irvine", "Chula Vista",
    ],
    "TX": [
        "Houston", "San Antonio", "Dallas", "Austin", "Fort Worth",
        "El Paso", "Arlington", "Corpus Christi", "Plano", "Laredo",
        "Lubbock", "Garland", "Irving", "Amarillo", "Grand Prairie",
    ],
    "FL": [
        "Jacksonville", "Miami", "Tampa", "Orlando", "St. Petersburg",
        "Hialeah", "Tallahassee", "Fort Lauderdale", "Port St. Lucie", "Cape Coral",
        "Pembroke Pines", "Hollywood", "Gainesville", "Miramar", "Coral Springs",
    ],
    "NY": [
        "New York City", "Buffalo", "Rochester", "Yonkers", "Syracuse",
        "Albany", "New Rochelle", "Mount Vernon", "Schenectady", "Utica",
        "White Plains", "Hempstead", "Troy", "Niagara Falls", "Binghamton",
    ],
    "IL": [
        "Chicago", "Aurora", "Naperville", "Joliet", "Rockford",
        "Springfield", "Elgin", "Peoria", "Champaign", "Waukegan",
        "Cicero", "Bloomington", "Arlington Heights", "Evanston", "Decatur",
    ],
    "PA": [
        "Philadelphia", "Pittsburgh", "Allentown", "Erie", "Reading",
        "Scranton", "Bethlehem", "Lancaster", "Harrisburg", "Altoona",
        "York", "Wilkes-Barre", "Chester", "Easton", "Lebanon",
    ],
    "OH": [
        "Columbus", "Cleveland", "Cincinnati", "Toledo", "Akron",
        "Dayton", "Parma", "Canton", "Youngstown", "Lorain",
        "Hamilton", "Springfield", "Kettering", "Elyria", "Middletown",
    ],
    "GA": [
        "Atlanta", "Augusta", "Columbus", "Macon", "Savannah",
        "Athens", "Sandy Springs", "South Fulton", "Roswell", "Johns Creek",
        "Albany", "Warner Robins", "Alpharetta", "Marietta", "Smyrna",
    ],
    "NC": [
        "Charlotte", "Raleigh", "Greensboro", "Durham", "Winston-Salem",
        "Fayetteville", "Cary", "Wilmington", "High Point", "Concord",
        "Gastonia", "Greenville", "Asheville", "Chapel Hill", "Rocky Mount",
    ],
    "MI": [
        "Detroit", "Grand Rapids", "Warren", "Sterling Heights", "Ann Arbor",
        "Lansing", "Flint", "Dearborn", "Livonia", "Westland",
        "Troy", "Farmington Hills", "Kalamazoo", "Wyoming", "Southfield",
    ],
    "NJ": [
        "Newark", "Jersey City", "Paterson", "Elizabeth", "Edison",
        "Woodbridge", "Lakewood", "Toms River", "Hamilton", "Trenton",
        "Clifton", "Camden", "Brick", "Cherry Hill", "Passaic",
    ],
    "VA": [
        "Virginia Beach", "Norfolk", "Chesapeake", "Richmond", "Newport News",
        "Alexandria", "Hampton", "Roanoke", "Portsmouth", "Suffolk",
        "Lynchburg", "Harrisonburg", "Charlottesville", "Danville", "Manassas",
    ],
    "WA": [
        "Seattle", "Spokane", "Tacoma", "Vancouver", "Bellevue",
        "Kent", "Everett", "Renton", "Spokane Valley", "Kirkland",
        "Bellingham", "Kennewick", "Yakima", "Federal Way", "Redmond",
    ],
    "AZ": [
        "Phoenix", "Tucson", "Mesa", "Chandler", "Scottsdale",
        "Gilbert", "Tempe", "Peoria", "Surprise", "Glendale",
        "Goodyear", "Avondale", "Flagstaff", "Buckeye", "Lake Havasu City",
    ],
    "MA": [
        "Boston", "Worcester", "Springfield", "Cambridge", "Lowell",
        "Brockton", "New Bedford", "Quincy", "Lynn", "Fall River",
        "Newton", "Lawrence", "Somerville", "Framingham", "Haverhill",
    ],
    "TN": [
        "Nashville", "Memphis", "Knoxville", "Chattanooga", "Clarksville",
        "Murfreesboro", "Franklin", "Jackson", "Johnson City", "Bartlett",
        "Hendersonville", "Kingsport", "Collierville", "Cleveland", "Smyrna",
    ],
    "IN": [
        "Indianapolis", "Fort Wayne", "Evansville", "South Bend", "Carmel",
        "Fishers", "Bloomington", "Hammond", "Gary", "Lafayette",
        "Muncie", "Terre Haute", "Kokomo", "Anderson", "Noblesville",
    ],
    "MO": [
        "Kansas City", "St. Louis", "Springfield", "Columbia", "Independence",
        "Lee's Summit", "O'Fallon", "St. Joseph", "St. Charles", "Blue Springs",
        "Joplin", "Chesterfield", "Jefferson City", "Cape Girardeau", "Florissant",
    ],
    "MD": [
        "Baltimore", "Frederick", "Rockville", "Gaithersburg", "Bowie",
        "Hagerstown", "Annapolis", "College Park", "Salisbury", "Laurel",
        "Greenbelt", "Cumberland", "Westminster", "Hyattsville", "Takoma Park",
    ],
    "WI": [
        "Milwaukee", "Madison", "Green Bay", "Kenosha", "Racine",
        "Appleton", "Waukesha", "Oshkosh", "Eau Claire", "Janesville",
        "West Allis", "La Crosse", "Sheboygan", "Wauwatosa", "Fond du Lac",
    ],
}

# Skróty stanów — zachowane dla ewentualnych filtrów / raportów
US_STATES: list[str] = list(STATE_CITIES.keys())

# ── Katalog produktów elektronicznych ────────────────────────────────────────
#
# Struktura każdej kategorii:
#   "brands"       → marki charakterystyczne dla tej kategorii
#   "templates"    → szablony nazw produktów
#   "price_range"  → (min, max) w USD
#   "screen_sizes" → (opcjonalne) rozmiary ekranów właściwe dla kategorii
#
# Placeholdery w szablonach:
#   {brand} → losowa marka z "brands"
#   {model} → losowy kod modelu, np. "X-490"
#   {size}  → losowy rozmiar z "screen_sizes" (tylko gdy klucz istnieje)

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
            "{brand} {model} {size} Laptop",
            "{brand} {model} Pro {size}",
            "{brand} {model} Gaming Laptop",
            "{brand} {model} Ultrabook {size}",
        ],
        "price_range": (499, 3_499),
        "screen_sizes": ['13"', '14"', '15.6"', '16"'],
    },
    "Tablets": {
        "brands": ["Apple", "Samsung", "Microsoft", "Lenovo", "Amazon"],
        "templates": [
            "{brand} {model} {size} Tablet",
            "{brand} {model} Tab",
            "{brand} {model} Tab Pro",
        ],
        "price_range": (149, 1_299),
        "screen_sizes": ['8"', '10.2"', '10.9"', '11"', '12.9"'],
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
            "{brand} {model} {size} 4K OLED TV",
            "{brand} {model} {size} QLED TV",
            "{brand} {model} {size} 4K Smart TV",
            "{brand} {model} {size} Monitor",
            "{brand} {model} {size} Curved Gaming Monitor",
        ],
        "price_range": (199, 4_999),
        "screen_sizes": ['43"', '55"', '65"', '75"', '85"'],
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
