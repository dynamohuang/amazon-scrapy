from datetime import datetime

import re
import scrapy

from pydispatch import dispatcher
from scrapy import signals

from amazon.helper import Helper
from amazon.items import SalesRankingItem
from amazon.sql import RankingSql


class SalesRankingSpider(scrapy.Spider):
    name = 'sales_ranking'
    custom_settings = {
        'LOG_LEVEL': 'DEBUG',
        'LOG_FILE': 'sales_ranking.json',
        'LOG_ENABLED': True,
        'LOG_STDOUT': True
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.items = []
        dispatcher.connect(self.load_asin, signals.engine_started)

    def start_requests(self):
        for item in self.items:
            yield scrapy.Request('https://www.amazon.com/dp/%s' % item['asin'], self.parse, meta={'item': item})

    def parse(self, response):
        product_detail = response.xpath('//div/table').re(r'#[0-9,]+(?:.*)in .* \(.*[Ss]ee [Tt]op.*\)')
        result = re.match(r'#([0-9,]+)(?:.*)in (.*) \(.*[Ss]ee [Tt]op.*\)', response.xpath('//body').extract()[0])
        print('1', response.xpath('//body').extract()[0])
        if len(product_detail) == 0:
            rankid_detail = response.css('table #SalesRank').re(r'.*#[0-9,]+(?:.*)in.*\(.*[Ss]ee [Tt]op.*\)')
            print('2', rankid_detail)
        else:
            pass
        if len(product_detail) != 0:
            item = SalesRankingItem()
            key_rank_str = product_detail[0]
            key_rank_tuple = Helper.get_rank_classify(key_rank_str)
            item['rank'] = Helper.get_num_split_comma(key_rank_tuple[0])
            item['classify'] = key_rank_tuple[1]
            item['sk_id'] = response.meta['item']['id']
            print(item)
        else:
            print('catch asin[%s] sales ranking error' % response.meta['item']['asin'])
            raise Exception('catch asin[%s] sales ranking error' % response.meta['item']['asin'])

    def load_asin(self):
        self.items = RankingSql.fetch_sales_ranking()


