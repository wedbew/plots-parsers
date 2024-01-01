import json
import requests
from dateutil import parser

def safe_get(dictionary, keys, default=None):
    """Safely get a value from a nested dictionary using a list of keys."""
    for key in keys:
        try:
            dictionary = dictionary[key]
        except (KeyError, TypeError):
            return default
    return dictionary

def parse_date(date_str):
    """Parse a date string into a datetime object using dateutil for flexibility."""
    try:
        return parser.parse(date_str)
    except (ValueError, TypeError):
        return None

def format_date(date):
    """Format a datetime object to a consistent string format."""
    if date:
        return date.strftime('%Y-%m-%dT%H:%M:%S%z')
    return None

def load_exchange_rates(file_name):
    """Load exchange rates from the JSON file."""
    with open(file_name, 'r') as file:
        return json.load(file)

exchange_rates = load_exchange_rates('exchange_rates.json')

def convert_to_eur(price, currency, date, exchange_rates):
    """Convert a given price to EUR based on exchange rates."""
    if currency == "EUR" or price is None or date not in exchange_rates:
        return price
    date_exchange_rates = exchange_rates.get(date, {})
    rate = date_exchange_rates.get(currency)
    return price / rate if rate else None

def clean_street_name(street_name):
    """Clean up the street name by removing common Polish address prefixes."""
    prefixes_to_remove = ["ul.", "ulica", "al.", "aleja", "pl.", "plac", "os.", "osiedle", "skwer", "droga", "rondo"]
    for prefix in prefixes_to_remove:
        street_name = street_name.replace(prefix, "").strip()
    return street_name

def get_coordinates(street, city, state, country):
    """Get latitude and longitude for a given address using Nominatim's structured API."""
    params = {
        'street': street,
        'city': city,
        'county': country,
        'state': state,
        'format': 'json'
    }
    response = requests.get("https://nominatim.openstreetmap.org/search", params=params)
    if response.status_code == 200:
        results = response.json()
        if results:
            return results[0].get('lat'), results[0].get('lon')
    return None, None
