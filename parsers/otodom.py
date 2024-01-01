from data_utils import safe_get, parse_date, format_date, convert_to_eur, exchange_rates

def parse_data(data):
    extracted_data = []
    for plot in data:
        listings = safe_get(plot, ['data', 'data', 'searchAds', 'items'], [])
        
        for listing in listings:
            # Extract and parse dates
            date_created_str = safe_get(listing, ["dateCreated"])
            date_created = parse_date(date_created_str)
            date_created_for_exchange_rate = date_created.strftime('%Y-%m-%d') if date_created else None
            date_scraped_str = plot.get("created", {}).get("$date", "")
            date_scraped = parse_date(date_scraped_str)

            # Extract pricing and currency information
            price = safe_get(listing, ["totalPrice", "value"])
            currency = safe_get(listing, ["totalPrice", "currency"])
            price_per_sqm = safe_get(listing, ["pricePerSquareMeter", "value"])

            # Convert prices to EUR using the formatted date for exchange rate lookup
            converted_price = convert_to_eur(price, currency, date_created_for_exchange_rate, exchange_rates) if date_created_for_exchange_rate else None
            converted_price_per_sqm = convert_to_eur(price_per_sqm, currency, date_created_for_exchange_rate, exchange_rates) if date_created_for_exchange_rate else None

            # Build the extracted item
            extracted_item = {
                "id": safe_get(listing, ["id"]),
                "title": safe_get(listing, ["title"]),
                "street": safe_get(listing, ["location", "address", "street", "name"]),
                "city": safe_get(listing, ["location", "address", "city", "name"]),
                "province": safe_get(listing, ["location", "address", "province", "name"]),
                "agency_id": safe_get(listing, ["agency", "id"]),
                "agency_name": safe_get(listing, ["agency", "name"]),
                "price": converted_price,
                "currency": currency,
                "price_per_square_meter": converted_price_per_sqm,
                "price_local": price,
                "price_per_square_meter_local": price_per_sqm,
                "is_private_owner": safe_get(listing, ["isPrivateOwner"]),
                "area": safe_get(listing, ["areaInSquareMeters"]),
                "unit": "square_meter",
                "date_created": format_date(date_created),
                "total_images": safe_get(listing, ["totalPossibleImages"]),
                "description": safe_get(listing, ["seo", "details", "description"]),
                "date_scraped": format_date(date_scraped)
            }
            extracted_data.append(extracted_item)

    return extracted_data
