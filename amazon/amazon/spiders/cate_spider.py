import scrapy
from pprint import pprint

class CateSpider(scrapy.Spider):
    name = "cate"

    def start_requests(self):
        urls = [
            'https://www.amazon.com/Best-Sellers/zgbs/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

       #id zg_browseRoot ul
        list = response.css('#zg_browseRoot ul')[0].css('li a')

        for item in list:
            yield {
                'title': item.css('::text').extract(),
                'link': item.css('::attr(href)').extract(),
                'level': '1',
            }


