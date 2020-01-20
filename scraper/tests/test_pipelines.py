from unittest.mock import patch

from django.db import transaction
from django.test import TestCase
from scrapy.crawler import Crawler
from scrapy.statscollectors import StatsCollector
from scrapy.utils.project import get_project_settings

from bulletin.models import Bulletin
from scraper.scraper.pipelines import ScraperPipeline
from scraper.scraper.spiders.bulletin import BulletinSpider
from scraper.tests.helpers import create_processed_items


class ScraperPipelineTest(TestCase):

    def setUp(self):
        self.spider = BulletinSpider(limit=1)
        crawler = Crawler(BulletinSpider, settings=get_project_settings())
        stats = StatsCollector(crawler)
        self.item_pipeline = ScraperPipeline(stats=stats)
        self.total_items = 5
        self.items = create_processed_items(self.total_items)

    def test_pipeline_successfully_saves_items(self):
        for item in self.items:
            self.item_pipeline.process_item(item, self.spider)

        self.assertEqual(Bulletin.objects.count(), self.total_items)
        self.assertEqual(
            self.item_pipeline.stats.get_value('items_saved_to_db'),
            self.total_items
        )

    @patch('scraper.scraper.pipelines.logging.warning')
    def test_pipeline_discards_duplicate_items(self, mock_warning):
        # Duplicate an item
        self.items[1] = self.items[0]
        for item in self.items:
            with transaction.atomic():
                self.item_pipeline.process_item(item, self.spider)

        self.assertEqual(Bulletin.objects.count(), self.total_items - 1)
        self.assertEqual(
            self.item_pipeline.stats.get_value('items_saved_to_db'),
            self.total_items - 1
        )
        self.assertEqual(
            self.item_pipeline.stats.get_value('items_duplicate'),
            1
        )

        duplicate_url = self.items[0]['url']
        warning_message = f'Unable to save bulletin with URL: {duplicate_url}'
        mock_warning.assert_called_with(warning_message)

    @patch('scraper.scraper.pipelines.logging.error')
    @patch('scraper.scraper.pipelines.Bulletin.save')
    def test_unexpected_errors_when_processing(self, mock_save, mock_error):
        # Set ok side effects except for one instance
        side_effect = [None for i in range(self.total_items)]
        side_effect[2] = ValueError
        mock_save.side_effect = side_effect

        for item in self.items:
            self.item_pipeline.process_item(item, self.spider)

        self.assertEqual(mock_save.call_count, self.total_items)
        self.assertTrue(mock_error.called)
