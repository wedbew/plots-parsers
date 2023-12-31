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