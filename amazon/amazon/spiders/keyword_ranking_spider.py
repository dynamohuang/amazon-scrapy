import scrapy
from pydispatch import dispatcher
from scrapy import signals
from amazon.helper import Helper
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
        self.keyword_pool = {}
        self.store_poll = {}
        self.store_date = {}
        dispatcher.connect(self.init_scrapy, signals.engine_started)
        dispatcher.connect(self.close_scrapy, signals.engine_stopped)

    def start_requests(self):
        for keyword, poll in self.keyword_pool.items():
            yield scrapy.Request(('https://www.amazon.com/s/?field-keywords=%s&t=' + Helper.random_str(10)) % keyword,
                                 self.load_first_page, meta={'items': poll})

    def parse(self, response):
        result_li = response.xpath('//li[@data-asin]')
        for item in response.meta['items']:
            if len(result_li) == 0:
                self.found[item['id']] = 'none'
            else:
                for result in result_li:
                    data_asin = result.xpath('./@data-asin').extract()[0]
                    if data_asin == item['asin']:
                        # print(item)
                        self.found[item['id']] = True
                        # keywordItem = KeywordRankingItem()
                        data_id = result.xpath('./@id').extract()[0]
                        item_id = data_id.split('_')[1]
                        rank = int(item_id) +1
                        if item['id'] in self.store_poll.keys():
                            self.store_poll[item['id']].append(rank)
                        else:
                            self.store_poll[item['id']] = [rank]
                        self.store_date[item['id']] = Helper.get_now_date()
                        print(self.store_date, self.store_poll)
                        # keywordItem['skwd_id'] = item['id']
                        # keywordItem['rank'] = int(item_id) +1
                        # yield keywordItem
                        # print(keywordItem)
                        break

    def load_first_page(self, response):
        page = response.css('#bottomBar span.pagnDisabled::text').extract()
        page = 1 if len(page) == 0 else int(page[0])
        page_num = 1
        while page_num <= page:
            # yield scrapy.Request(response.url + '&page=%s' % page_num, self.parse, meta={'asin': response.meta['item']['asin'],
            #                                                                              'skwd_id': response.meta['item']['id']})
            yield scrapy.Request(response.url + '&page=%s' % page_num, self.parse, meta={'items': response.meta['items']})
            page_num += 1

    def init_scrapy(self):
        self.items = RankingSql.fetch_keywords_ranking()
        for item in self.items:
            if item['keyword'] in self.keyword_pool.keys():
                self.keyword_pool[item['keyword']].append({'id': item['id'], 'asin': item['asin']})
            else:
                self.keyword_pool[item['keyword']] = [{'id': item['id'], 'asin': item['asin']}]

        self.found = {item['id']: False for item in self.items}

    def close_scrapy(self):
        for skwd_id, is_found in self.found.items():
            if is_found is not True:
                if is_found == 'none':
                    RankingSql.update_keywords_none_rank(skwd_id)
                else:
                    RankingSql.update_keywords_expire_rank(skwd_id)
            else:
                keywordrank = KeywordRankingItem()
                keywordrank['skwd_id'] = skwd_id
                keywordrank['rank'] = min(self.store_poll[skwd_id])
                keywordrank['date'] = self.store_date[skwd_id]
                RankingSql.insert_keyword_ranking(keywordrank)

