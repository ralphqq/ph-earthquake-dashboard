from unittest.mock import patch

from django.test import SimpleTestCase

from scraper.crawl import CrawlTaskHandler
from scraper.scraper.spiders.bulletin import BulletinSpider
from scraper.tasks import run_scraper


@patch('scraper.crawl.CrawlerProcess.crawl')
class CeleryScrapeTasksTest(SimpleTestCase):

    def test_task_calls_spider(self, mock_crawl):
        run_scraper()
        self.assertEqual(mock_crawl.called, True)

    def test_errors_show_warning(self, mock_crawl):
        error_message = 'Oops'
        with patch('scraper.tasks.logging.warning') as mock_warning:
            mock_crawl.side_effect = Exception(error_message)
            run_scraper()

            self.assertTrue(mock_warning.called)
            log_message = (
                f'Problems encountered during scraping task: '
                f'{error_message}'
            )
            mock_warning.assert_called_with(log_message)
