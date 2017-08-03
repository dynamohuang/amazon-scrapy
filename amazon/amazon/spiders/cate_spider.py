import scrapy
from amazon.items import CateItem

class CateSpider(scrapy.Spider):
    name = "cate"

    def start_requests(self):
        urls = [
            'https://www.amazon.com/Best-Sellers/zgbs/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, meta={'level': 1})

    def parse(self, response):

        if response.meta['level'] == 1:
            list = response.css('#zg_browseRoot ul')[0].css('li a')
        elif response.meta['level'] == 2:
            list = response.css('#zg_browseRoot ul')[0].css('ul')[0].css('li a')
        else:
            return 0
        item = CateItem()
        leve_cur = response.meta['level']
        response.meta['level'] = response.meta['level'] + 1

        for one in list:
            item['title'] = one.css('::text')[0].extract()
            link = one.css('::attr(href)')[0].extract()
            item['link'] = link.split('ref=')[0]
            item['level'] = leve_cur
            item['pid'] = 1
            print(leve_cur)
            yield item
            yield scrapy.Request(url=item['link'], callback=self.parse, meta=response.meta)




