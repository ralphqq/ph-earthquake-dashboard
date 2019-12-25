# -*- coding: utf-8 -*-
import logging

from django.db import IntegrityError

from bulletin.models import Bulletin


class ScraperPipeline(object):

    def process_item(self, item, spider):
        """Saves item from spider to database."""
        try:
            bulletin_update = Bulletin.objects.create(**item)
        except IntegrityError as e:
            logging.warning(f'Unable to save to database: {e}')
        except Exception as e:
            logging.error(f'An unexpected error occurred: {e}')
        else:
            logging.info(f'Saved {bulletin_update} to db')

        return item
