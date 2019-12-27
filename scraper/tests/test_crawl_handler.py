from unittest.mock import patch

from django.test import SimpleTestCase

from scraper.crawl import CrawlTaskHandler
from scraper.scraper.spiders.bulletin import BulletinSpider


@patch('scraper.crawl.CrawlerProcess.start')
@patch(
    'scraper.scraper.spiders.bulletin.BulletinSpider.__init__',
    return_value=None
)
class CrawlTaskHandlerTest(SimpleTestCase):

    def test_crawl_process_without_args(self, mock_init, mock_start):
        crawl = CrawlTaskHandler(BulletinSpider)
        crawl.run_spider()
        self.assertTrue(mock_init.called)
        with self.assertRaises(AssertionError):
            mock_init.assert_called_with(year=2019)

    def test_crawl_process_with_args(self, mock_init, mock_start):
        crawl = CrawlTaskHandler(
            spider=BulletinSpider,
            input='inputargument',
            year=2019
        )
        crawl.run_spider()
        self.assertTrue(mock_init.called)
        _, kwargs = mock_init.call_args
        self.assertEqual(kwargs.get('input'), 'inputargument')
        self.assertEqual(kwargs.get('year'), 2019)


@patch('scraper.crawl.CrawlerProcess.start')
@patch('scraper.scraper.spiders.bulletin.BulletinSpider.start_requests')
class CrawlTaskHandlerScraperRequestTest(SimpleTestCase):

    def test_crawl_process_runs_requests(self, mock_req, mock_start):
        crawl = CrawlTaskHandler(BulletinSpider)
        crawl.run_spider()
        self.assertTrue(mock_req.called)
