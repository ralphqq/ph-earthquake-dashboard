# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join

from scraper.utils import (
    clean_decimal, convert_to_datetime, fix_url
)


class PhivolcsItem(scrapy.Item):
    time_of_quake = scrapy.Field()
    url = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()
    depth = scrapy.Field()
    magnitude = scrapy.Field()
    location = scrapy.Field()


class PhivolcsItemLoader(ItemLoader):
    default_input_processor = MapCompose(str.strip)
    default_output_processor = TakeFirst()

    time_of_quake_in = MapCompose(str.strip, convert_to_datetime)

    url_in = MapCompose(str.strip, fix_url)

    latitude_in = MapCompose(str.strip, clean_decimal)

    longitude_in = MapCompose(str.strip, clean_decimal)

    depth_in = MapCompose(str.strip, clean_decimal)

    magnitude_in = MapCompose(str.strip, clean_decimal)

    location_out = Join()
