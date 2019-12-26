from datetime import date
from unittest.mock import patch

from django.test import SimpleTestCase

from scraper.scraper.spiders.bulletin import BulletinSpider
from scraper.tests.helpers import make_response_object


class BulletinSpiderTest(SimpleTestCase):

    def setUp(self):
        settings = 'scraper.scraper.settings'
        with patch.dict('os.environ', {'SCRAPY_SETTINGS_MODULE': settings}):
            self.spider = BulletinSpider(limit=1)
        self.response = make_response_object(
            fname='page.html',
            callback=self.spider.parse
        )

    @patch('scraper.scraper.spiders.bulletin.BulletinSpider.set_start_urls')
    def test_no_year_passed_as_arg(self, mock_set_urls):
        self.assertFalse(mock_set_urls.called)

    @patch('scraper.scraper.spiders.bulletin.BulletinSpider.set_start_urls')
    def test_year_passed_as_arg(self, mock_set_urls):
        spider = BulletinSpider(year=2019, limit=1)
        self.assertTrue(mock_set_urls.called)

    def test_start_urls_for_current_year(self):
        # Get start URLS for current year
        today = date.today()
        self.spider.set_start_urls(today.year)

        # Only up to current month will be scraped
        self.assertEqual(len(self.spider.start_urls), today.month)
        self.assertIn(self.spider.base_url, self.spider.start_urls)

    def test_start_urls_for_previous_year(self):
        # Get start URLS for previous year
        today = date.today()
        self.spider.set_start_urls(today.year - 1)

        # All 12 months will be scraped
        self.assertEqual(len(self.spider.start_urls), 12)
        self.assertNotIn(self.spider.base_url, self.spider.start_urls)

    def test_parse_method(self):
        items = self.spider.parse(self.response)
        for item in items:
            # Check if all fields in items are valid fields
            for k, v in item.items():
                self.assertIn(k, self.spider.bulletin_fields)

    def test_valid_record_finder(self):
        rows = self.response.xpath('//tr')
        self.assertFalse(self.spider._is_valid_record(rows[0]))
        self.assertTrue(self.spider._is_valid_record(rows[50]))
        self.assertFalse(self.spider._is_valid_record(rows[-1]))
