"""
Central configuration for the e-commerce data generator.

Store: Consumer Electronics (USA)
Locale: en_US
"""



# Faker language configuration
FAKER_LOCALE = "en_US"





# Generation modes
CONFIG = {
    "SMALL": {
        "label":        "Small (100 clients / 20 products / 500 orders)",
        "num_clients":  100,
        "num_products":  20,
        "num_orders":   500,
    },
    "MEDIUM": {
        "label":        "Medium (1,000 clients / 100 products / 8,000 orders)",
        "num_clients":  1_000,
        "num_products":   100,
        "num_orders":   8_000,
    },
    "LARGE": {
        "label":        "Large (5,000 clients / 260 products / 50,000 orders)",
        "num_clients":  5_000,
        "num_products":   260,
        "num_orders":  50_000,
    },
}





# Output directory
OUTPUT_DIR = "data"





# Random seed for reproducibility
RANDOM_SEED = 42





# Date ranges
PRODUCT_START_DATE = "2020-01-01"
ORDER_START_DATE   = "2022-01-01"





# Currency
CURRENCY = "USD"





# Client segments
SEGMENTS = {
    "VIP": {
        "weight":       0.10,
        "orders_range": (15, 40),
    },
    "Regular": {
        "weight":       0.25,
        "orders_range": (5, 15),
    },
    "Occasional": {
        "weight":       0.40,
        "orders_range": (2, 5),
    },
    "Dormant": {
        "weight":       0.25,
        "orders_range": (1, 2),
    },
}

DORMANT_CUTOFF_DAYS = 180

SEGMENT_CATEGORY_PREFERENCES = {
    "VIP":        ["Smartphones", "Laptops", "Smartwatches & Wearables", "Cameras"],
    "Regular":    ["Smartphones", "Laptops", "Headphones & Audio", "Gaming"],
    "Occasional": ["Accessories & Cables", "Headphones & Audio", "Smart Home"],
    "Dormant":    ["Accessories & Cables", "Headphones & Audio"],
}





# Order statuses
ORDER_STATUSES       = ["completed", "shipped", "processing", "cancelled"]
ORDER_STATUS_WEIGHTS = [60, 20, 15, 5]





# Geography: US states and cities
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

US_STATES: list[str] = list(STATE_CITIES.keys())





# Electronics product catalog
CATALOG: dict[str, list[dict]] = {

    # Smartphones (8 SKUs)
    "Smartphones": [
        {"brand": "Apple",   "name": "iPhone 16",           "price": (799,  899)},
        {"brand": "Apple",   "name": "iPhone 16 Plus",      "price": (899,  999)},
        {"brand": "Apple",   "name": "iPhone 16 Pro",       "price": (999, 1099)},
        {"brand": "Apple",   "name": "iPhone 16 Pro Max",   "price": (1099, 1199)},
        {"brand": "Samsung", "name": "Galaxy S25",          "price": (699,  799)},
        {"brand": "Samsung", "name": "Galaxy S25+",         "price": (899,  999)},
        {"brand": "Samsung", "name": "Galaxy S25 Ultra",    "price": (1099, 1399)},
        {"brand": "Google",  "name": "Pixel 9 Pro",         "price": (799,  999)},
    ],

    # Laptops (9 SKUs)
    "Laptops": [
        {"brand": "Apple",     "name": "MacBook Air 13",      "price": (999,  1299), "screen_size": '13"'},
        {"brand": "Apple",     "name": "MacBook Air 15",      "price": (1199, 1499), "screen_size": '15"'},
        {"brand": "Apple",     "name": "MacBook Pro 14",      "price": (1799, 2499), "screen_size": '14"'},
        {"brand": "Apple",     "name": "MacBook Pro 16",      "price": (2499, 3499), "screen_size": '16"'},
        {"brand": "Dell",      "name": "XPS 13",              "price": (999,  1699), "screen_size": '13"'},
        {"brand": "Dell",      "name": "XPS 15",              "price": (1299, 2199), "screen_size": '15"'},
        {"brand": "Lenovo",    "name": "ThinkPad X1 Carbon",  "price": (1199, 1999), "screen_size": '14"'},
        {"brand": "HP",        "name": "Spectre x360 14",     "price": (1099, 1699), "screen_size": '14"'},
        {"brand": "Microsoft", "name": "Surface Laptop 5",    "price": (999,  1799), "screen_size": '13.5"'},
    ],

    # Tablets (7 SKUs)
    "Tablets": [
        {"brand": "Apple",     "name": "iPad mini 7",         "price": (499,  599),  "screen_size": '8.3"'},
        {"brand": "Apple",     "name": "iPad 10th Gen",       "price": (349,  449),  "screen_size": '10.9"'},
        {"brand": "Apple",     "name": "iPad Air 11",         "price": (599,  749),  "screen_size": '11"'},
        {"brand": "Apple",     "name": "iPad Pro 13",         "price": (999, 1299),  "screen_size": '13"'},
        {"brand": "Samsung",   "name": "Galaxy Tab S9",       "price": (599,  799),  "screen_size": '11"'},
        {"brand": "Samsung",   "name": "Galaxy Tab S9 Ultra", "price": (999, 1199),  "screen_size": '14.6"'},
        {"brand": "Microsoft", "name": "Surface Pro 10",      "price": (799, 1299),  "screen_size": '13"'},
    ],

    # Headphones & Audio (8 SKUs)
    "Headphones & Audio": [
        {"brand": "Apple",      "name": "AirPods 4",                  "price": (129, 179)},
        {"brand": "Apple",      "name": "AirPods Pro 2",              "price": (199, 249)},
        {"brand": "Apple",      "name": "AirPods Max",                "price": (449, 549)},
        {"brand": "Sony",       "name": "WH-1000XM5",                 "price": (279, 349)},
        {"brand": "Sony",       "name": "WF-1000XM5",                 "price": (199, 279)},
        {"brand": "Bose",       "name": "QuietComfort 45",            "price": (249, 329)},
        {"brand": "Bose",       "name": "QuietComfort Ultra Earbuds", "price": (249, 299)},
        {"brand": "Sennheiser", "name": "Momentum 4 Wireless",        "price": (279, 349)},
    ],

    # Smartwatches & Wearables (6 SKUs)
    "Smartwatches & Wearables": [
        {"brand": "Apple",   "name": "Apple Watch Series 10", "price": (399, 499)},
        {"brand": "Apple",   "name": "Apple Watch Ultra 2",   "price": (749, 849)},
        {"brand": "Samsung", "name": "Galaxy Watch 7",        "price": (269, 329)},
        {"brand": "Samsung", "name": "Galaxy Watch Ultra",    "price": (599, 699)},
        {"brand": "Garmin",  "name": "Forerunner 965",        "price": (499, 599)},
        {"brand": "Garmin",  "name": "Fenix 7 Pro",           "price": (699, 899)},
    ],

    # Cameras (7 SKUs)
    "Cameras": [
        {"brand": "Sony",     "name": "Alpha A7 IV",    "price": (2299, 2799)},
        {"brand": "Sony",     "name": "ZV-E10 II",      "price": (699,   899)},
        {"brand": "Canon",    "name": "EOS R50",        "price": (599,   799)},
        {"brand": "Canon",    "name": "EOS R6 Mark II", "price": (2299, 2699)},
        {"brand": "Nikon",    "name": "Z30",            "price": (699,   899)},
        {"brand": "Fujifilm", "name": "X-T5",           "price": (1499, 1799)},
        {"brand": "GoPro",    "name": "HERO12 Black",   "price": (299,   399)},
    ],

    # TVs & Displays (8 SKUs)
    "TVs & Displays": [
        {"brand": "Samsung", "name": 'Neo QLED QN90D 55"',       "price": (1199, 1599), "screen_size": '55"',
         "variants": ["4K — 60Hz", "4K — 120Hz"]},
        {"brand": "Samsung", "name": 'Neo QLED QN90D 65"',       "price": (1799, 2299), "screen_size": '65"',
         "variants": ["4K — 60Hz", "4K — 120Hz", "8K — 60Hz"]},
        {"brand": "LG",      "name": 'OLED C4 55"',              "price": (1199, 1499), "screen_size": '55"',
         "variants": ["4K — 120Hz"]},
        {"brand": "LG",      "name": 'OLED C4 65"',              "price": (1699, 1999), "screen_size": '65"',
         "variants": ["4K — 120Hz"]},
        {"brand": "Sony",    "name": 'Bravia XR A95L 65"',       "price": (2499, 2999), "screen_size": '65"',
         "variants": ["4K — 120Hz", "8K — 120Hz"]},
        {"brand": "LG",      "name": 'UltraGear 27" 4K Monitor', "price": (449,   599), "screen_size": '27"',
         "variants": ["4K — 60Hz", "4K — 144Hz"]},
        {"brand": "Samsung", "name": 'Odyssey G7 32" Monitor',   "price": (499,   699), "screen_size": '32"',
         "variants": ["4K — 144Hz", "4K — 240Hz"]},
        {"brand": "Dell",    "name": 'UltraSharp U2723D 27"',    "price": (499,   699), "screen_size": '27"',
         "variants": ["4K — 60Hz"]},
    ],

    # Gaming (8 SKUs)
    "Gaming": [
        {"brand": "Sony",        "name": "PlayStation 5 Slim",        "price": (399, 499)},
        {"brand": "Microsoft",   "name": "Xbox Series X",             "price": (449, 499)},
        {"brand": "Nintendo",    "name": "Nintendo Switch OLED",      "price": (299, 349)},
        {"brand": "Razer",       "name": "BlackShark V2 Pro Headset", "price": (149, 199)},
        {"brand": "Razer",       "name": "DeathAdder V3 Mouse",       "price": (69,   99)},
        {"brand": "Logitech",    "name": "G Pro X Superlight 2",      "price": (149, 169)},
        {"brand": "SteelSeries", "name": "Apex Pro TKL Keyboard",     "price": (149, 199)},
        {"brand": "Logitech",    "name": "G915 TKL Keyboard",         "price": (159, 229)},
    ],

    # Smart Home (7 SKUs)
    "Smart Home": [
        {"brand": "Amazon",  "name": "Echo Dot 5th Gen",          "price": (39,  59)},
        {"brand": "Amazon",  "name": "Echo Show 10",              "price": (199, 249)},
        {"brand": "Google",  "name": "Nest Hub 2nd Gen",          "price": (79,   99)},
        {"brand": "Google",  "name": "Nest Learning Thermostat",  "price": (199, 249)},
        {"brand": "Ring",    "name": "Video Doorbell Pro 2",      "price": (199, 249)},
        {"brand": "Philips", "name": "Hue Starter Kit",           "price": (149, 199)},
        {"brand": "Apple",   "name": "HomePod mini",              "price": (89,   99)},
    ],

    # Accessories & Cables (9 SKUs)
    "Accessories & Cables": [
        {"brand": "Anker",    "name": "MagSafe Wireless Charger 15W",    "price": (25,  45)},
        {"brand": "Anker",    "name": "Prime 27 000mAh Power Bank",      "price": (89, 129)},
        {"brand": "Anker",    "name": "USB-C to USB-C Cable 6ft",        "price": (9,   19)},
        {"brand": "Anker",    "name": "737 GaNPrime Charger 120W",       "price": (59,  89)},
        {"brand": "Belkin",   "name": "BoostCharge Pro 3-in-1",          "price": (79, 119)},
        {"brand": "Spigen",   "name": "Tough Armor Case for iPhone 16",  "price": (29,  49)},
        {"brand": "Apple",    "name": "MagSafe Charger 1m",              "price": (35,  45)},
        {"brand": "Logitech", "name": "MX Master 3S Mouse",              "price": (89, 109)},
        {"brand": "Logitech", "name": "MX Keys S Keyboard",              "price": (99, 119)},
    ],
}