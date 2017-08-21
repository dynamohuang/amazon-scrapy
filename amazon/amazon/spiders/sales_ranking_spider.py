from datetime import datetime

import scrapy

from pydispatch import dispatcher
from scrapy import signals

from amazon.amazon.helper import Helper
from amazon.amazon.items import SalesRankingItem
from amazon.amazon.sql import RankingSql


class SalesRankingSpider(scrapy.Spider):
    name = 'sales_ranking'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.items = []
        dispatcher.connect(self.load_asin, signals.engine_started)

    def start_requests(self):
        for item in self.items:
            yield scrapy.Request('https://www.amazon.com/dp/%s' % item['asin'], self.parse, meta={'item': item})

    def parse(self, response):
        product_detail = response.xpath('//div/table').re(r'#\d*(?:.*)in .* \(.*[Ss]ee [Tt]op.*\)')
        if len(product_detail) != 0:
            item = SalesRankingItem()
            key_rank_str = product_detail[0]
            key_rank_tuple = Helper.get_rank_classify(key_rank_str)
            item['rank'] = key_rank_tuple[0]
            item['classify'] = key_rank_tuple[1]
            item['sk_id'] = response.meta['item']['id']
            yield item
        else:
            raise Exception('catch asin[%s] sales ranking error' % response.meta['item']['asin'])

    def load_asin(self):
        self.items = RankingSql.fetch_sales_ranking()


