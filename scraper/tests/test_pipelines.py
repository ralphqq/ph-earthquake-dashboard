from django.db import transaction
from django.test import TestCase

from bulletin.models import Bulletin
from scraper.scraper.pipelines import ScraperPipeline
from scraper.scraper.spiders.bulletin import BulletinSpider
from scraper.tests.helpers import create_processed_items


class ScraperPipelineTest(TestCase):

    def setUp(self):
        self.spider = BulletinSpider(limit=1)
        self.item_pipeline = ScraperPipeline()
        self.total_items = 5
        self.items = create_processed_items(self.total_items)

    def test_pipeline_successfully_saves_items(self):
        for item in self.items:
            self.item_pipeline.process_item(item, self.spider)

        self.assertEqual(Bulletin.objects.count(), self.total_items)

    def test_pipeline_discards_duplicate_items(self):
        # Duplicate an item
        self.items[1] = self.items[0]
        for item in self.items:
            with transaction.atomic():
                self.item_pipeline.process_item(item, self.spider)

        self.assertEqual(Bulletin.objects.count(), self.total_items - 1)
