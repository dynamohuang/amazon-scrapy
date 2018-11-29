
BOT_NAME = 'amazon2'

SPIDER_MODULES = ['amazon2.spiders']
NEWSPIDER_MODULE = 'amazon2.spiders'

ROBOTSTXT_OBEY = False

CONCURRENT_REQUESTS = 32

COOKIES_ENABLED = False

SPIDER_MIDDLEWARES = {
    'amazon2.middlewares.AmazonSpiderMiddleware.AmazonSpiderMiddleware': 543,
}

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'amazon2.middlewares.RotateUserAgentMiddleware.RotateUserAgentMiddleware': 543,
}
