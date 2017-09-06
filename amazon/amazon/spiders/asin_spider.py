import scrapy
import json
from amazon.items import AsinBestItem
import pydispatch
from scrapy import signals
from datetime import datetime
from amazon.mysqlpipelines.pipelines import Sql
class AsinSpider(scrapy.Spider):
    name = "asin"
    custom_settings = {
        'LOG_LEVEL': 'ERROR',
        'LOG_ENABLED': True,
        'LOG_STDOUT': True
    }

    def __init__(self):
        scrapy.Spider.__init__(self)
        pydispatch.dispatcher.connect(self.handle_spider_closed, signals.spider_closed)
        # all asin scrapied will store in the array
        self.asin_pool = []

    def start_requests(self):
        cates = Sql.findall_cate_level1()
        for row in cates:
            row['link'] += '?ajax=1'
            yield scrapy.Request(url=row['link']+'&pg=1', callback=self.parse, meta={'cid': row['id'], 'page': 1, 'link': row['link']})

    def parse(self, response):
        list = response.css('.zg_itemImmersion')

        # scrapy next page  go go go !
        response.meta['page'] = response.meta['page'] +1
        if response.meta['page'] < 6:
            yield scrapy.Request(url=response.meta['link']+'&pg='+str(response.meta['page']), callback=self.parse, meta=response.meta)

        # yield the asin
        for row in list:
            try:
                info = row.css('.zg_itemWrapper')[0].css('div::attr(data-p13n-asin-metadata)')[0].extract()
                rank = int(float(row.css('.zg_rankNumber::text')[0].extract()))

            except:
                continue
                pass
            info = json.loads(info)
            item = AsinBestItem()
            item['asin'] = info['asin']
            item['cid'] = response.meta['cid']
            item['rank'] = rank
            yield item

    def handle_spider_closed(self, spider):
        Sql.store_best_asin()
        work_time = datetime.now() - spider.started_on
        print('total spent:', work_time)
        print('done')



