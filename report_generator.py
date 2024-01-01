import numpy as np
from datetime import datetime
from collections import defaultdict

def compute_stats(data, key):
    values = [item[key] for item in data if item[key] is not None]
    if not values:
        return None
    return {
        'min': float(np.min(values)),
        'max': float(np.max(values)),
        'avg': float(np.mean(values)),
        'median': float(np.median(values)),
        'stddev': float(np.std(values)),
        'total': float(np.sum(values))
    }

def parse_date_for_day(date_str):
    try:
        return datetime.strptime(date_str.split('T')[0], '%Y-%m-%d').date()
    except (ValueError, TypeError):
        return None

def analyze_data(data):
    report = {
        'field_counts': {},
        'stats': {},
        'provinces': {},
        'daily_stats': [],
        'agency_stats': []
    }

    if not data:
        return "No data to analyze."

    # Initialize field counts
    for key in data[0].keys():
        report['field_counts'][key] = sum(item[key] is not None for item in data)

    # Calculate overall stats
    for key in ['price', 'area', 'price_per_square_meter']:
        report['stats'][key] = compute_stats(data, key)

    # Group data by day, province, and agency
    daily_data, province_data, agency_data = defaultdict(list), defaultdict(list), defaultdict(list)
    for item in data:
        day, province, agency_id = parse_date_for_day(item['date_created']), item['province'], item['agency_id']
        if day: daily_data[day].append(item)
        if province: province_data[province].append(item)
        if agency_id is not None: agency_data[agency_id].append(item)

    # Calculate stats for each day, province, and agency
    for day, items in daily_data.items():
        report['daily_stats'].append({
            'date': day.isoformat(),
            'count': len(items),
            'stats': {key: compute_stats(items, key) for key in ['price', 'area', 'price_per_square_meter']}
        })

    for province, items in province_data.items():
        report['provinces'][province] = {
            'count': len(items),
            'stats': {key: compute_stats(items, key) for key in ['price', 'area', 'price_per_square_meter']}
        }

    for agency_id, items in agency_data.items():
        report['agency_stats'].append({
            'agency_id': agency_id,
            'count': len(items),
            'stats': {key: compute_stats(items, key) for key in ['price', 'area', 'price_per_square_meter']}
        })
    report['agency_stats'].sort(key=lambda x: x['count'], reverse=True)

    return report
