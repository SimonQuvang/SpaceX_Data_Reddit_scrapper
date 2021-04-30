# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose
from w3lib.html import remove_tags


def clean_thead(text):
    temp = text.split('—')
    return temp[0].strip()


class SpacexDevItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(input_processor = MapCompose(remove_tags, clean_thead), output_processor = TakeFirst())
    date = scrapy.Field(input_processor = MapCompose(remove_tags), output_processor = TakeFirst())
    comment = scrapy.Field(input_processor = MapCompose(remove_tags), output_processor = TakeFirst())
    link = scrapy.Field()

class SpaceXJobItem(scrapy.Item):
    title = scrapy.Field(input_processor = MapCompose(remove_tags), output_processor = TakeFirst())
    location = scrapy.Field(input_processor=MapCompose(remove_tags), output_processor=TakeFirst())
    type = scrapy.Field(input_processor=MapCompose(remove_tags), output_processor=TakeFirst())
    link = scrapy.Field(input_processor=MapCompose(remove_tags), output_processor=TakeFirst())

