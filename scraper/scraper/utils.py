import re
from urllib.parse import urljoin

from dateutil.parser import parse
import pytz
from scrapy.utils.project import get_project_settings


def convert_to_datetime(date_str):
    """Creates a tz-aware datetime object from datetime string."""
    tz = pytz.timezone('Asia/Manila')
    try:
        date_obj = parse(date_str)
        return tz.localize(date_obj)
    except Exception as e:
        return None


def clean_decimal(num_str):
    """Removes all non-decimal characters from string."""
    try:
        non_decimal = re.compile(r'[^\d.\-]+')
        cleaned_num = non_decimal.sub('', num_str)
        final_num= cleaned_num.rstrip('.-')
        return float(final_num)
    except Exception as e:
        return None


def fix_url(url_string):
    """Makes raw URL a valid absolute link."""
    settings = get_project_settings()
    base_url = settings['BULLETIN_BASE_URL']
    try:
        rel_path = url_string.replace('\\', '/')
        return urljoin(base_url, rel_path)
    except Exception as e:
        return None
