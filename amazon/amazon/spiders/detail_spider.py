import scrapy
from amazon.items import DetailItem
from amazon.mysqlpipelines.pipelines import Sql
import pydispatch
from scrapy import signals
from datetime import datetime


class DetailSpider(scrapy.Spider):
    name = "detail"
    custom_settings = {
        'LOG_LEVEL': 'ERROR',
        'LOG_ENABLED': True,
        'LOG_STDOUT': True
    }

    def __init__(self):
        scrapy.Spider.__init__(self)
        pydispatch.dispatcher.connect(self.handle_spider_closed, signals.spider_closed)
        # all asin scrapied will store in the array
        self.product_pool = {}
        self.log = []
        self.products = []

    def start_requests(self):
        self.products = Sql.findall_asin_level1()
        print(len(self.products))
        for row in self.products:
            yield scrapy.Request(
                    url='https://www.amazon.com/gp/offer-listing/' + row['asin'] + '/?f_new=true',
                    callback=self.listing_parse,
                    meta={
                        'asin': row['asin'],
                        'cid': row['cid'],
                    }
            )

    def review_parse(self, response):
        item = self.fetch_detail_from_review_page(response)
        self.product_pool[item['asin']] = item
        yield item

    def listing_parse(self, response):
        print(response.status)

        if not response.css('#olpProductImage'):
            yield scrapy.Request(
                    url='https://www.amazon.com/product-reviews/' + response.meta['asin'],
                    callback=self.review_parse,
                    meta={'asin': response.meta['asin'], 'cid': response.meta['cid']}
            )
            return
        try:
            item = self.fetch_detail_from_listing_page(response)
            self.product_pool[item['asin']] = item
        except Exception as err:
            print(err)
            print(response.meta['asin'])
        yield item

    def handle_spider_closed(self, spider):
        work_time = datetime.now() - spider.started_on
        print('total spent:', work_time)
        print(len(self.product_pool), 'item fetched')
        print('done')
        print(self.log)




    def fetch_detail_from_listing_page(self, response):
        item = DetailItem()
        item['asin'] = response.meta['asin']
        item['image'] = response.css('#olpProductImage img::attr(src)')[0].extract().strip().replace('_SS160', '_SS320')
        item['title'] = response.css('title::text')[0].extract().split(':')[2].strip()

        try:
            item['star'] = response.css('.a-icon-star span::text')[0].extract().split(' ')[0].strip()
        except:
            item['star'] = 0
        try:
            item['reviews'] = response.css('.a-size-small > .a-link-normal::text')[0].extract().strip().split(' ')[0]
        except:
            item['reviews'] = 0

        price_info_list = response.css(".olpOffer[role=\"row\"] ")
        item['amazon_price'] = 0
        item['seller_price'] = 0
        for row in price_info_list:
            if (item['amazon_price'] == 0) and row.css(".olpSellerName > img"):
                try:
                    item['amazon_price'] = row.css('.olpOfferPrice::text')[0].extract().strip().lstrip('$')
                except:
                    item['amazon_price'] = 0
                continue
            if (item['seller_price'] == 0) and (not row.css(".olpSellerName > img")):
                try:
                    item['seller_price'] = row.css('.olpOfferPrice::text')[0].extract().strip().lstrip('$')
                except:
                    item['seller_price'] = 0
        return item

    def fetch_detail_from_review_page(self, response):
        item = DetailItem()
        #item['title'] = response.css('.product-title >h1>a')[0].extract()
        item['asin'] = response.meta['asin']
        item['image'] = '2'
        item['title'] = '2'
        item['star'] = '2'
        item['reviews'] = '2'
        item['seller_price'] = '2'
        item['amazon_price'] = '2'
        return item
