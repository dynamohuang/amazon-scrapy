import scrapy
from amazon.items import DetailItem
from amazon.mysqlpipelines.pipelines import Sql
import pydispatch
from scrapy import signals
from datetime import datetime

class DetailSpider(scrapy.Spider):
    name = "detail"

    def __init__(self):
        scrapy.Spider.__init__(self)
        pydispatch.dispatcher.connect(self.handle_spider_closed, signals.spider_closed)
        # all asin scrapied will store in the array
        self.product_pool = []
        self.log = []


    def start_requests(self):
        products = Sql.findall_asin_level1()
        for row in products:
            yield scrapy.Request(url='https://www.amazon.com/gp/offer-listing/'+ row['asin'] +'/?f_new=true', callback=self.parse, meta={'asin': row['asin'], 'cid': row['cid']})

    def parse(self, response):
        print('hell')
        try:
            response.meta['from']
        except:
            response.meta['from'] = None
        print(response.meta['from'])
        print('22')
        #fetch from review
        if response.meta['from'] == 'review':
            item = DetailItem()
            item = response.css('.product-title >h1>a')[0].extract()
            print(item)
            return item

        #404 or unsupport asin
        if not response.css('#olpProductImage'):
             #fetch from review
            print('22')
            scrapy.Request(url='https://www.amazon.com/product-reviews/'+ response.meta['asin'] , callback=self.parse, meta={'from': 'review', 'asin': response.meta['asin'], 'cid': response.meta['cid']})
        try:
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
            self.product_pool.append(item)
            pass
        except Exception as err:
            print(err)
            print(response.meta['asin'])

        yield item

    def handle_spider_closed(self, spider):

        Sql.store_cate_level1()
        work_time = datetime.now() - spider.started_on
        print('total spent:', work_time)
        print(len(self.product_pool), 'item fetched')
        print('done')
        print(self.log)





