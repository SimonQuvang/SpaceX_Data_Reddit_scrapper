import scrapy
from spacex_dev.items import SpacexDevItem
from scrapy.loader import ItemLoader

class SpacexSpider(scrapy.Spider):
    name = 'spacex'
    allowed_domains = ['reddit.com/r/spacex']
    start_urls = []
    submission_id = ['c61lqs', 'ci70t4', 'cxyt8x', 'dfd8ik', 'e11zs0', 'ellkmn', 'f9mmb0', 'fr73sy', 'ghgmyg', 'hf368o',
                     'i4j0bk', 'inkzwp', 'j545qo', 'jtvex0', 'kbjngb', 'lc7eij', 'm06c13', 'mk99yw']
    base_url = 'http://reddit.com/r/spacex/comments/'
    for id in submission_id:
        url = base_url + id
        start_urls.append(url)

    def parse(self, response):
        for table in response.css('table'):
            print(table.css('thead strong::text'))
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
