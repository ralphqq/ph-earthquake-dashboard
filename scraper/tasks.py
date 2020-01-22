import logging

from celery import shared_task

from scraper.crawl import CrawlTaskHandler
from scraper.scraper.spiders.bulletin import BulletinSpider


@shared_task(name='run-scraper')
def run_scraper():
    """Starts a scraping task."""
    try:
        crawler = CrawlTaskHandler(BulletinSpider)
        crawler.run_spider()
        logging.info('Successfully completed scraping task')
    except Exception as e:
        logging.warning(f'Problems encountered during scraping task: {e}')
