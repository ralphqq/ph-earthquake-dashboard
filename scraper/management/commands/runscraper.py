from django.core.management.base import BaseCommand

from scraper.crawl import CrawlTaskHandler
from scraper.scraper.spiders.bulletin import BulletinSpider


class Command(BaseCommand):
    help = 'Runs earthquake bulletin scraper'

    def add_arguments(self, parser):
                # Optional argument
        parser.add_argument(
            '-Y',
            '--year',
            type=int,
            help='Set the year to scrape',
        )

    def handle(self, *args, **kwargs):
        year = kwargs['year']

        msg = year if year else 'current year'
        self.stdout.write(f'Fetching bulletins from {msg}')

        try:
            crawler = None
            if year:
                crawler = CrawlTaskHandler(
                    spider=BulletinSpider,
                    input='inputargument',
                    year=year
                )
            else:
                crawler = CrawlTaskHandler(BulletinSpider)
            crawler.run_spider()
        except KeyboardInterrupt:
                        self.stdout.write('Exited')
        else:
            self.stdout.write('Done')
