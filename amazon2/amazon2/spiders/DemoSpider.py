import scrapy
from amazon2.spiders.AmazonBaseSpider import AmazonBaseSpider


# scrapy crawl demo -a asin=B07K97BQDF
class DemoSpider(AmazonBaseSpider):
    name = "demo"

    def __init__(self, asin='B07K97BQDF'):
        AmazonBaseSpider.__init__(self)
        self.asin = asin

    def start_requests(self):
        yield scrapy.Request(
            url='https://www.amazon.com/dp/' + self.asin,
            callback=self.parse,
            meta={
                'asin': self.asin,
                'cid': -10
            }
        )

    def parse(self, response):
        print(response.meta['asin'])
        self.result_pool[response.meta['asin']] = {}
        self.result_pool[response.meta['asin']]['title'] = 'title for ' + response.meta['asin']

    # Bingo! Here we get the result and You can restore or output it
    def handle_spider_closed(self, spider):
        print(self.result_pool.get(self.asin))
        AmazonBaseSpider.print_progress(self, spider)
