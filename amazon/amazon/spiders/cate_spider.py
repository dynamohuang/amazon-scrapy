import scrapy
import json
from amazon.items import CateItem

class CateSpider(scrapy.Spider):
    name = "cate"

    def start_requests(self):
        urls = [
            'https://www.amazon.com/Best-Sellers/zgbs/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        list = response.css('#zg_browseRoot ul')[0].css('li a')
        item = CateItem()
        for one in list:
            item['title'] = one.css('::text')[0].extract()
            link = one.css('::attr(href)')[0].extract()
            item['link'] = link.split('ref=')[0]
            item['level'] = 1
            item['pid'] = 0
            yield item




