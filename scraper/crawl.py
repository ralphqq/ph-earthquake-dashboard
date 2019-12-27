import os

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


class CrawlTaskHandler:

    def __init__(self, spider, log_enabled=True, **kwargs):
        os.environ.setdefault(
            'SCRAPY_SETTINGS_MODULE',
            'scraper.scraper.settings'
        )

        # Custom settings
        s = get_project_settings()
        s['SPIDER_MODULES'] = ['scraper.scraper.spiders']
        s['NEWSPIDER_MODULE'] = 'scraper.scraper.spiders'
        s['ITEM_PIPELINES'] = {
            'scraper.scraper.pipelines.ScraperPipeline': 300,
        }
        s['LOG_ENABLED'] = log_enabled

        self.process = CrawlerProcess(s)
        self.spider = spider
        self.kwargs = kwargs

    def run_spider(self):
        self.process.crawl(self.spider, **self.kwargs)
        self.process.start()
