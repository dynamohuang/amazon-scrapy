import scrapy
import re
import json

class KuaidailiSpider(scrapy.Spider):
    name = "kuaidaili"
    # custom_settings = {
    #     'LOG_LEVEL': 'ERROR',
    #     'LOG_ENABLED': True,
    #     'LOG_STDOUT': True
    # }


    def start_requests(self):

        self.headers = {
            'Host': 'www.kuaidaili.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:52.0) Gecko/20100101 Firefox/52.0',
        }

        url = "http://www.kuaidaili.com/free/inha/"
        yield scrapy.Request(url=url, callback=self.parse, meta={})

    def parse(self, response):
        print(response.status)
        print('3333')
        print(response.css('.center tr').re('td'))




