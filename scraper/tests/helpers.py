from datetime import datetime, timedelta
import random

from scraper.scraper.utils import convert_to_datetime


def create_processed_items(n_items=10):
    """Generates fake processed items."""
    now = datetime.now()
    td = timedelta(minutes=3)
    return [{
        'time_of_quake': convert_to_datetime((now - td * i).isoformat()),
        'url': f'https://www.eqx.com/{i + 1:03d}.html',
        'latitude': random.randint(0, 90),
        'longitude': random.randint(-180, 180),
        'depth': random.randint(1, 200),
        'magnitude': random.randint(1, 10),
        'location': f'Location {i + 1}'
    } for i in range(n_items)]
