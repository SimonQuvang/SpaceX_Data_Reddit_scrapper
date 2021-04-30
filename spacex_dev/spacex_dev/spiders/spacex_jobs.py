import scrapy
from spacex_dev.items import SpaceXJobItem
from scrapy.loader import ItemLoader

class SpacexSpider(scrapy.Spider):
    name = 'spacex'
    allowed_domains = ['https://www.spacex.com/careers/']
    start_urls = ["https://www.spacex.com/careers/?department="]

    def parse(self, response):
        for table in response.css('table.jobs'):
            if table.css('thead strong::text'):
                pass
            l = ItemLoader(item=SpacexDevItem(), selector=table)
            l.add_css('name', 'thead strong')
            trs = table.css('tbody tr')
            for tr in trs:
                l.selector = tr
                l.add_css('date', 'td')
                l.add_css('comment', 'td a')
                l.add_css('link', 'td a::attr(href)')
                yield l.load_item()
