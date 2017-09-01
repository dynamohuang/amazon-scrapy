# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy



class CateItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    level = scrapy.Field()
    pid = scrapy.Field()
    pass

class AsinBestItem(scrapy.Item):
    asin = scrapy.Field()
    cid = scrapy.Field()
    rank = scrapy.Field()
    pass

class DetailItem(scrapy.Item):
    asin = scrapy.Field()
    image = scrapy.Field()
    title = scrapy.Field()
    star = scrapy.Field()
    reviews = scrapy.Field()
    seller_price = scrapy.Field()
    amazon_price = scrapy.Field()
    pass

class ReviewProfileItem(scrapy.Item):
    asin = scrapy.Field()
    product = scrapy.Field()
    brand = scrapy.Field()
    seller = scrapy.Field()
    image = scrapy.Field()
    review_total = scrapy.Field()
    review_rate = scrapy.Field()
    pct_five = scrapy.Field()
    pct_four = scrapy.Field()
    pct_three = scrapy.Field()
    pct_two = scrapy.Field()
    pct_one = scrapy.Field()
    pass


class ReviewDetailItem(scrapy.Item):
    asin = scrapy.Field()
    review_id = scrapy.Field()
    reviewer = scrapy.Field()
    review_url = scrapy.Field()
    star = scrapy.Field()
    date = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    pass


class KeywordRankingItem(scrapy.Item):
    skwd_id = scrapy.Field()
    rank = scrapy.Field()


class SalesRankingItem(scrapy.Item):
    sk_id = scrapy.Field()
    rank = scrapy.Field()
    classify = scrapy.Field()
    asin = scrapy.Field()
