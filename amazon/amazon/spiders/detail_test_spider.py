import scrapy
import pydispatch
import re
from scrapy import signals
from datetime import datetime



class DetailSpider(scrapy.Spider):
    name = "detail_test"
    custom_settings = {
        'LOG_LEVEL': 'ERROR',
        'LOG_ENABLED': True,
        'LOG_STDOUT': True
    }

    def __init__(self):
        scrapy.Spider.__init__(self)
        pydispatch.dispatcher.connect(self.handle_spider_closed, signals.spider_closed)

    def start_requests(self):

        asin_list = ['']

        for asin in asin_list:
            yield scrapy.Request(
                    url='https://www.amazon.com/gp/offer-listing/' + asin + '/?f_new=true',
                    callback=self.parse,
                    meta={
                        'asin': asin,
                    }
            )

    def parse(self, response):
        print(22)


    def handle_spider_closed(self, spider):
        work_time = datetime.now() - spider.started_on
        print('total spent:', work_time)
        print(len(self.product_pool), 'item fetched')
        print(self.product_pool)
        print('done')
        print(self.log)


