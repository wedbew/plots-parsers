from data_utils import (safe_get, parse_date, format_date, convert_to_eur, 
                        exchange_rates)

def parse_data(data):
    extracted_data = []
    count = 0
    for plot in data:
        listings = safe_get(plot, ['data','searchResults', 'on_market'], [])
        date_scraped_str = plot.get("created", {}).get("$date", "")
        date_scraped = parse_date(date_scraped_str)
        
        for listing in listings:
            date_created_str = date_scraped_str
            date_created = parse_date(date_created_str)
            date_created_for_exchange_rate = date_created.strftime('%Y-%m-%d') if date_created else None
            price = safe_get(listing, ["priceCash"])
            currency = "DKK"  # Assuming the currency is always DKK
            price_per_sqm = safe_get(listing, ["perAreaPrice"])

            converted_price = convert_to_eur(price, currency, date_created_for_exchange_rate, exchange_rates) if date_created_for_exchange_rate else None
            converted_price_per_sqm = convert_to_eur(price_per_sqm, currency, date_created_for_exchange_rate, exchange_rates) if date_created_for_exchange_rate else None
            images = len(safe_get(listing, ["images"])) if safe_get(listing, ["images"]) is not None else 0
            extracted_item = {
                "id": safe_get(listing, ["caseID"]),
                "title": safe_get(listing, ["slug"]),
                "street": safe_get(listing, ["address", "road", "name"]),
                "city": safe_get(listing, ["address", "city", "name"]),
                "province": safe_get(listing, ["address", "province", "name"]),
                "agency_id": safe_get(listing, ["realtor", "name"]),
                "agency_name": safe_get(listing, ["realtor", "descriptionTitle"]),
                "price": converted_price,
                "currency": currency,
                "price_per_square_meter": converted_price_per_sqm,
                "price_local": price,
                "price_per_square_meter_local": price_per_sqm,
                "is_private_owner": False,
                "area": safe_get(listing, ["lotArea"]),
                "unit": "square_meter",
                "date_created": format_date(date_scraped),
                "total_images": images,
                "description": safe_get(listing, ["descriptionBody"]),
                "date_scraped": format_date(date_scraped),
                "latitude": safe_get(listing, ["coordinates", "lat"]),
                "longitude": safe_get(listing, ["coordinates", "lon"])
            }

            extracted_data.append(extracted_item)
            count += 1

            if count % 50 == 0:
                print(f"Processed {count} listings")

    return extracted_data
