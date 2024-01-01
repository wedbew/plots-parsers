import requests
import json
from datetime import datetime, timedelta

def fetch_exchange_rates(api_key, start_date, end_date, currencies):
    base_url = "http://api.exchangeratesapi.io/v1/"
    current_date = start_date
    exchange_rates = {}

    while current_date <= end_date:
        date_str = current_date.strftime('%Y-%m-%d')
        response = requests.get(f"{base_url}{date_str}?access_key={api_key}&symbols={','.join(currencies)}")
        data = response.json()

        if data.get("success", False):
            rates = data['rates']
            exchange_rates[date_str] = rates
        else:
            print(f"Failed to fetch data for {date_str}: {data.get('error')}")

        current_date += timedelta(days=1)

    return exchange_rates

def save_to_json(file_name, data):
    with open(file_name, 'w') as file:
        json.dump(data, file, indent=4)

# Your API Key
api_key = ''

# Define your date range and currencies
start_date = datetime(2023, 9, 21)
end_date = datetime(2023, 12, 31)
currencies = ["PLN", "EUR", "DKK", "SEK"]

# Fetch the exchange rates
rates = fetch_exchange_rates(api_key, start_date, end_date, currencies)

# Save to JSON file
json_file_name = 'exchange_rates.json'
save_to_json(json_file_name, rates)
