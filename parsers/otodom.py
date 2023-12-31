# parsers/otodom.py
from data_utils import safe_get, parse_date, format_date

def parse_data(data):
    extracted_data = []
    for plot in data:
        listings = safe_get(plot, ['data', 'data', 'searchAds', 'items'], [])
        
        for listing in listings:
            date_created = parse_date(safe_get(listing, ["dateCreated"]))
            date_scraped = parse_date(plot.get("created", {}).get("$date", ""))

            extracted_item = {
                "id": safe_get(listing, ["id"]),
                "title": safe_get(listing, ["title"]),
                "street": safe_get(listing, ["location", "address", "street", "name"]),
                "city": safe_get(listing, ["location", "address", "city", "name"]),
                "province": safe_get(listing, ["location", "address", "province", "name"]),
                "agency_id": safe_get(listing, ["agency", "id"]),
                "agency_name": safe_get(listing, ["agency", "name"]),
                "price": safe_get(listing, ["totalPrice", "value"]),
                "currency": safe_get(listing, ["totalPrice", "currency"]),
                "is_private_owner": safe_get(listing, ["isPrivateOwner"]),
                "price_per_square_meter": safe_get(listing, ["pricePerSquareMeter", "value"]),
                "area": safe_get(listing, ["areaInSquareMeters"]),
                "unit": "square_meter",
                "date_created": format_date(date_created),
                "total_images": safe_get(listing, ["totalPossibleImages"]),
                "description": safe_get(listing, ["seo", "details", "description"]),
                "date_scraped": format_date(date_scraped)
            }
            extracted_data.append(extracted_item)

    return extracted_data
