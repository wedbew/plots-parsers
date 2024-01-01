# Function to format numbers with commas for better readability
def format_number(number):
    return f"{number:,.2f}"

# Function to generate the report
def generate_report(data):
    price_stats = data["stats"]["price"]
    area_stats = data["stats"]["area"]
    price_per_sqm_stats = data["stats"]["price_per_square_meter"]
    min_date = data["stats"]["min_date"]
    max_date = data["stats"]["max_date"]

    total_listings = 25226
    date_range = f"{min_date} - {max_date}"
    price_range = f"From {format_number(price_stats['min'])} EUR to {format_number(price_stats['max'])} EUR"
    avg_price = format_number(price_stats["avg"]) + " EUR"
    median_price = format_number(price_stats["median"]) + " EUR"
    stddev_price = format_number(price_stats["stddev"]) + " EUR"
    total_price_volume = format_number(price_stats["total"]) + " EUR"
    area_range = f"From {format_number(area_stats['min'])} sqm to {format_number(area_stats['max'])} sqm"
    avg_area = format_number(area_stats["avg"]) + " sqm"
    median_area = format_number(area_stats["median"]) + " sqm"
    stddev_area = format_number(area_stats["stddev"]) + " sqm"
    total_area = format_number(area_stats["total"]) + " sqm"
    pp_sqm_range = f"From {format_number(price_per_sqm_stats['min'])} EUR/sqm to {format_number(price_per_sqm_stats['max'])} EUR/sqm"
    avg_pp_sqm = format_number(price_per_sqm_stats["avg"]) + " EUR/sqm"
    median_pp_sqm = format_number(price_per_sqm_stats["median"]) + " EUR/sqm"
    stddev_pp_sqm = format_number(price_per_sqm_stats["stddev"]) + " EUR/sqm"
    total_pp_sqm_volume = format_number(price_per_sqm_stats["total"]) + " EUR"

    report = f"General Market Overview\n" \
             f"Total Listings: {total_listings}\n" \
             f"Date Range: {date_range}\n" \
             f"Price Range: {price_range}\n" \
             f"Average Price: {avg_price}\n" \
             f"Median Price: {median_price}\n" \
             f"Standard Deviation of Prices: {stddev_price}\n" \
             f"Total Price Volume: {total_price_volume}\n" \
             f"Area Range: {area_range}\n" \
             f"Average Area: {avg_area}\n" \
             f"Median Area: {median_area}\n" \
             f"Standard Deviation of Area: {stddev_area}\n" \
             f"Total Area: {total_area}\n" \
             f"Price Per Square Meter Range: {pp_sqm_range}\n" \
             f"Average Price Per Square Meter: {avg_pp_sqm}\n" \
             f"Median Price Per Square Meter: {median_pp_sqm}\n" \
             f"Standard Deviation of Price Per Square Meter: {stddev_pp_sqm}\n" \
             f"Total Price Per Square Meter Volume: {total_pp_sqm_volume}\n"

    return report