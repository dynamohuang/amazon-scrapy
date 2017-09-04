import scrapy
import re
import json

class ProxySpider(scrapy.Spider):
    name = "proxy"
    custom_settings = {
        'LOG_LEVEL': 'ERROR',
        'LOG_ENABLED': True,
        'LOG_STDOUT': True
    }


    def start_requests(self):
        url = "http://fineproxy.org/eng/fresh-proxies/"
        yield scrapy.Request(url=url, callback=self.parse, meta={})

    def parse(self, response):
        pattern = "<strong>Fast proxies: </strong>(.*)<strong>Other fresh and working proxies:</strong>"
        tmp = re.findall(pattern, response.text)[0]
        proxy = re.findall("([0-9]{1,4}.[0-9]{1,4}.[0-9]{1,4}.[0-9]{1,4}:[0-9]{1,4})", tmp)
        with open('proxy.json', 'w') as f:
            json.dump(proxy, f)





