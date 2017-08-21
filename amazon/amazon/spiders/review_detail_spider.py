import math
import subprocess

import scrapy
from pydispatch import dispatcher
from scrapy import signals

from amazon_spider.items import ReviewProfileItem
from amazon_spider.items import ReviewDetailItem
from amazon_spider.helper import Helper
from amazon_spider.sql import ReviewSql


class ReviewSpider(scrapy.Spider):
    name = 'detail'
    custom_settings = {
        'LOG_LEVEL': 'ERROR',
        'LOG_FILE': 'profile.json',
        'LOG_ENABLED': True,
        'LOG_STDOUT': True
    }

    def __init__(self, asin, daily=0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.asin = asin
        self.last_review = 0
        self.profile_update_self = False    # profile自动计数更新
        self.updated = False   # profile是否更新过
        self.daily = True if int(daily) == 1 else False  # 判断是否是每日更新
        self.start_urls = [
            'https://www.amazon.com/product-reviews/%s?sortBy=recent&filterByStar=three_star' % self.asin,
            'https://www.amazon.com/product-reviews/%s?sortBy=recent&filterByStar=two_star' % self.asin,
            'https://www.amazon.com/product-reviews/%s?sortBy=recent&filterByStar=one_star' % self.asin
        ]
        dispatcher.connect(self.update_profile_self, signals.engine_stopped)
        dispatcher.connect(self.init_profile, signals.engine_started)

    def start_requests(self):
        self.load_profile()
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.get_detail)

    def parse(self, response):
        reviews = response.css('.review-views .review')
        for row in reviews:
            item = ReviewDetailItem()
            item['asin'] = self.asin
            item['review_id'] = row.css('div::attr(id)')[0].extract()
            item['reviewer'] = row.css('.author::text')[0].extract()
            item['title'] = row.css('.review-title::text')[0].extract()
            item['review_url'] = row.css('.review-title::attr(href)')[0].extract()
            item['date'] = Helper.get_date_split_str(row.css('.review-date::text')[0].extract())
            item['star'] = Helper.get_star_split_str(row.css('.review-rating span::text')[0].extract())
            content = row.css('.review-data .review-text::text').extract()
            item['content'] = content[0] if len(content) > 0 else ''
            yield item

    def get_detail(self, response):
        # 获取页面数
        page = response.css('ul.a-pagination li a::text')

        i = 1
        # 获取评价总数
        total = response.css('.AverageCustomerReviews .totalReviewCount::text').extract()  # 获取评价总数
        now_total = Helper.get_num_split_comma(total[0])
        last_review = self.last_review
        sub_total = int(now_total) - int(last_review)
        if sub_total != 0:
            # if sub_total != 0:  # 若计算出的页数 不为0 则说明有新的评论，更新profile
            self.updated = True
            yield scrapy.Request('https://www.amazon.com/product-reviews/%s' % self.asin,
                                 callback=self.profile_parse)
            if len(page) < 3:  # 若找到的a标签总数小于3 说明没有page组件 只有1页数据
                yield scrapy.Request(url=response.url + '&pageNumber=1', callback=self.parse)
            else:
                if self.daily:
                    page_num = math.ceil(sub_total / 10)
                    print('update item page_num is %s' % page_num)
                else:
                    self.profile_update_self = True
                    page_num = Helper.get_num_split_comma(page[len(page) - 3].extract())  # 获得总页数
                while i <= int(page_num):
                    yield scrapy.Request(url=response.url + '&pageNumber=%s' % i,
                                         callback=self.parse)
                    i = i + 1
        else:
            print('there is no item to update')

    def profile_parse(self, response):
        item = ReviewProfileItem()

        item['asin'] = self.asin
        # 获取平均评价数值
        average = response.css('.averageStarRatingNumerical a span::text').extract()  # 获取平均评价值
        item['review_rate'] = Helper.get_star_split_str(average[0])  # 获取平均值
        # 获取评价总数
        total = response.css('.AverageCustomerReviews .totalReviewCount::text').extract()  # 获取评价总数
        item['review_total'] = Helper.get_num_split_comma(total[0])
        # 获取产品名称
        product = response.css('.product-title h1 a::text').extract()
        item['product'] = product[0]
        # 获取产品 brand
        item['brand'] = response.css('.product-by-line a::text').extract()[0]
        item['image'] = response.css('.product-image img::attr(src)').extract()[0]

        # 获取产品商家
        item['seller'] = item['brand']
        # 获取各星评价百分比数
        review_summary = response.css('.reviewNumericalSummary .histogram '
                                      '#histogramTable tr td:last-child').re(r'\d{1,3}\%')

        pct = list(map(lambda x: x[0:-1], review_summary))

        item['pct_five'] = pct[0]
        item['pct_four'] = pct[1]
        item['pct_three'] = pct[2]
        item['pct_two'] = pct[3]
        item['pct_one'] = pct[4]

        yield item

    def load_profile(self):
        # 若没有profile记录 则抓取新的profile 录入数据库
        if self.last_review is False:
            self.profile_update_self = True
            print('this asin profile is not exist, now to get the profile of asin:', self.asin)
            yield scrapy.Request('https://www.amazon.com/product-reviews/%s' % self.asin,
                                 callback=self.profile_parse)
            self.last_review = ReviewSql.get_last_review_total(self.asin)

    # scrapy 完成后 加载，如果是没有记录的profile 初次insert lastest_review为0 将所有多余的数据跑完后 防止第二次重复跑取，将latest_total更新
    def update_profile_self(self):
        if self.profile_update_self is True and self.updated is False:
            # 若需要自主更新 并且 未更新状态
            ReviewSql.update_profile_self(self.asin)

    # scrapy 开始前加载，获取目前asin的latest_review
    def init_profile(self):
        self.last_review = ReviewSql.get_last_review_total(self.asin)
