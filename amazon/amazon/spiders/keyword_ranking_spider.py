import scrapy
from pydispatch import dispatcher
from scrapy import signals
from scrapy.exceptions import CloseSpider

from amazon.items import KeywordRankingItem
from amazon.sql import RankingSql


class KeywordRankingSpider(scrapy.Spider):
    name = 'keyword_ranking'
    custom_settings = {
        'LOG_LEVEL': 'ERROR',
        'LOG_FILE': 'keyword_ranking.json',
        'LOG_ENABLED': True,
        'LOG_STDOUT': True
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.items = {}
        self.found = {}
        dispatcher.connect(self.init_scrapy, signals.engine_started)
        dispatcher.connect(self.close_scrapy, signals.engine_stopped)

    def start_requests(self):
        for item in self.items:
            yield scrapy.Request('https://www.amazon.com/s/?field-keywords=%s' % item['keyword'], self.load_first_page, meta={'item': item})

    def parse(self, response):
        result_li = response.xpath('//li[@data-asin]')
        for result in result_li:
            data_asin = result.xpath('./@data-asin').extract()[0]
            if data_asin == response.meta['asin']:
                self.found[response.meta['skwd_id']] = True
                item = KeywordRankingItem()
                data_id = result.xpath('./@id').extract()[0]
                item_id = data_id.split('_')[1]
                item['skwd_id'] = response.meta['skwd_id']
                item['rank'] = int(item_id) +1
                yield item

                break

    def load_first_page(self, response):
        page = response.css('#bottomBar span.pagnDisabled::text').extract()
        page = 1 if len(page) == 0 else int(page[0])
        page_num = 1
        while page_num <= page:
            yield scrapy.Request(response.url + '&page=%s' % page_num, self.parse, meta={'asin': response.meta['item']['asin'],
                                                                                         'skwd_id': response.meta['item']['id']})
            page_num += 1

    def init_scrapy(self):
        self.items = RankingSql.fetch_keywords_ranking()
        self.found = {item['id']: False for item in self.items}

    def close_scrapy(self):
        for skwd_id, is_found in self.found.items():
            if is_found is not True:
                RankingSql.update_keywords_expire_rank(skwd_id)
