from datetime import datetime
from unittest.mock import patch

from django.test import SimpleTestCase
from scrapy.utils.project import get_project_settings

from scraper.scraper.utils import (
    convert_to_datetime, clean_decimal, fix_url
)


@patch.dict(
    'os.environ',
    {'SCRAPY_SETTINGS_MODULE': 'scraper.scraper.settings'}
)
class UtilsTest(SimpleTestCase):

    def test_valid_datetime_conversion(self):
        date_str = [
            '30 November 2019 - 11:59 PM',
            '20 May 2018 - 01:04 PM'
        ]
        for dt in date_str:
            result = convert_to_datetime(dt)
            self.assertIsInstance(result, datetime)

    def test_invalid_datetime_conversion(self):
        date_str = [
            'Invalid date format here',
            'Another invalid date format here'
        ]
        for dt in date_str:
            result = convert_to_datetime(dt)
            self.assertIsNone(result)

    def test_decimal_cleanup(self):
        res1 = clean_decimal('003.14')
        res2 = clean_decimal('x003.14*')
        res3 = clean_decimal('x-x')
        self.assertEqual(res1, 3.14)
        self.assertEqual(res2, 3.14)
        self.assertIsNone(res3)

    def test_url_fix_function(self):
        settings = get_project_settings()
        base_url = settings['BULLETIN_BASE_URL']
        raw_url = '2019\\2019_December_22_25.html'
        result = fix_url(raw_url)
        self.assertIn(base_url, result)
        self.assertNotIn('\\', result)
