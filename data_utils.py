import json
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

# Load exchange rates from the JSON file
def load_exchange_rates(file_name):
    with open(file_name, 'r') as file:
        return json.load(file)

exchange_rates = load_exchange_rates('exchange_rates.json')

def convert_to_eur(price, currency, date, exchange_rates):
    if currency == "EUR" or price is None or date not in exchange_rates:
        return price
    date_exchange_rates = exchange_rates.get(date, {})
    rate = date_exchange_rates.get(currency)
    return price / rate if rate else None
