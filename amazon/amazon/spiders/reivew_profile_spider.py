import scrapy

from amazon.amazon.helper import Helper
from amazon.amazon.items import ReviewProfileItem


class ProfileSpider(scrapy.Spider):
    name = 'review_profile'
    custom_settings = {
        'LOG_LEVEL': 'ERROR',
        'LOG_FILE': 'profile.json',
        'LOG_ENABLED': True,
        'LOG_STDOUT': True
    }

    def __init__(self, asin, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.asin = asin

    def start_requests(self):
        yield scrapy.Request('https://www.amazon.com/product-reviews/%s' % self.asin, callback=self.parse)

    def parse(self, response):
        item = ReviewProfileItem()

        item['asin'] = response.meta['asin'] if 'asin' in response.meta else self.asin
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
