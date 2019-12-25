# -*- coding: utf-8 -*-
from datetime import date

import scrapy
from scrapy.utils.project import get_project_settings

from scraper.scraper.items import PhivolcsItem, PhivolcsItemLoader


class BulletinSpider(scrapy.Spider):
    name = 'bulletin'
    allowed_domains = ['earthquake.phivolcs.dost.gov.ph']

    def __init__(self, year=None, *args, **kwargs):
        settings = get_project_settings()
        self.bulletin_fields = settings['FEED_EXPORT_FIELDS']
        self.base_url = settings['BULLETIN_BASE_URL']
        self.start_urls = [self.base_url]

        if year is not None:
            year = int(year)
            self.set_start_urls(year)

        self.logger.info(f'{len(self.start_urls)} pages to scrape')
        super().__init__(*args, **kwargs)

    def set_start_urls(self, year):
        """Sets `start_urls` based on available months in given year."""
        today = date.today()
        limit = today.month - 1     # exclude current month

        if year != today.year:
            limit = 12  # include all 12 months
            self.start_urls = []    # remove default URL

        for i in range(limit):
            month = date(year, i + 1, 1)
            url = f'{self.base_url}EQLatest-Monthly/{year}/{month:%Y_%B}.html'
            self.start_urls.append(url)

    def parse(self, response):
        rows = response.xpath('//tr')
        for row in rows:
            if not self._is_valid_record(row):
                continue

            cols = row.xpath('./td')
            l = PhivolcsItemLoader(PhivolcsItem())

            for i, field in enumerate(self.bulletin_fields):
                data_point = None

                if i == 0:
                    data_point = cols[i].xpath('.//a//text()')
                elif i == 1:
                    data_point = cols[i - 1].xpath('.//a/@href')
                elif i > 1:
                    data_point = cols[i - 1].xpath('.//text()')

                l.add_value(field, data_point.extract())

            yield l.load_item()

    def _is_valid_record(self, tr):
        """Checks if row selector points to a valid bulletin record."""
        return bool(tr.xpath('./td/span//a'))
