from data_utils import safe_get, parse_date, format_date
from datetime import datetime

def parse_data(data):
    extracted_data = []
    count = 0
    for plot in data:
        listings = safe_get(plot, ['data', 'listings'], [])
        date_scraped_str = plot.get("created", {}).get("$date", "")
        date_scraped = parse_date(date_scraped_str)

        for item in listings:
            listing = safe_get(item, ['listing'], {})
            media = safe_get(listing, ['media'], {})
            point = safe_get(listing, ['point'], {})
            seller = safe_get(listing, ['seller'], {})

            # Parse price to a number
            price_str = safe_get(listing, ["price"], "").replace("€", "").replace(",", "")
            price = None
            try:
                price = float(price_str)
            except ValueError:
                pass  # Keep price as None if parsing fails

            # Calculate area in square meters
            floor_area_unit = safe_get(listing, ["floorArea", "unit"])
            floor_area_value = safe_get(listing, ["floorArea", "value"])
            area = None
            if floor_area_unit == "ACRES":
                try:
                    area = float(floor_area_value) * 4046.86  # 1 acre = 4046.86 square meters
                except ValueError:
                    pass  # Keep area as None if parsing fails

            # Format date_created
            date_created_str = safe_get(listing, ["publishDate", "$numberLong"])
            date_created = None
            if date_created_str:
                date_created = datetime.utcfromtimestamp(float(date_created_str) / 1000).strftime('%Y-%m-%dT%H:%M:%S+0000')

            # Calculate price per square meter, if both price and area are not None
            price_per_square_meter = None
            if price is not None and area is not None and area != 0:
                price_per_square_meter = price / area

            extracted_item = {
                "id": safe_get(listing, ["id"]),
                "title": safe_get(listing, ["title"]),
                "street": safe_get(seller, ["address"]),
                "city": None,
                "province": None,
                "agency_id": safe_get(seller, ["sellerId"]),
                "agency_name": safe_get(seller, ["name"]),
                "price": price,
                "currency": "EUR",
                "price_per_square_meter": price_per_square_meter,
                "price_local": price,
                "price_per_square_meter_local": None,
                "is_private_owner": safe_get(seller, ["sellerType"]) != "UNBRANDED_AGENT",
                "area": area,
                "unit": "square_meter",
                "date_created": date_created if date_created else format_date(date_scraped),
                "total_images": safe_get(media, ["totalImages"], 0),
                "description": None,
                "date_scraped": format_date(date_scraped),
                "latitude": safe_get(point, ["coordinates", 1]),
                "longitude": safe_get(point, ["coordinates", 0])
            }

            # Append only if both price and area are present
            if price is not None and area is not None:
                extracted_data.append(extracted_item)

            count += 1

            if count % 50 == 0:
                print(f"Processed {count} listings")

    return extracted_data
