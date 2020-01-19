# -*- coding: utf-8 -*-
import logging

from django.db import IntegrityError

from bulletin.models import Bulletin


class ScraperPipeline(object):

    def __init__(self, stats):
        self.stats = stats

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.stats)

    def process_item(self, item, spider):
        """Saves item from spider to database."""
        try:
            bulletin_update = Bulletin.objects.create(**item)
        except IntegrityError as e:
            logging.warning(f'Unable to save to database: {e}')
            self.stats.inc_value('items_duplicate')
        except Exception as e:
            logging.error(f'An unexpected error occurred: {e}')
        else:
            logging.info(f'Saved {bulletin_update} to db')
            self.stats.inc_value('items_saved_to_db')

        return item
