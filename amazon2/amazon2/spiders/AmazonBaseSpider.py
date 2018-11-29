import scrapy
import pydispatch.dispatcher
from scrapy import signals
from datetime import datetime


class AmazonBaseSpider(scrapy.Spider):
    name = "AmazonBase"
    custom_settings = {
        'LOG_LEVEL': 'ERROR',
        'LOG_ENABLED': True,
        'LOG_STDOUT': True,
    }

    def __init__(self):
        pydispatch.dispatcher.connect(self.handle_spider_closed, signals.spider_closed)
        self.result_pool = {}
        self.log = []

    def start_requests(self):
        return

    def parse(self, response):
        return

    def print_progress(self, spider):
        work_time = datetime.now() - spider.started_on
        print('Spent:', work_time, ':', len(self.result_pool), 'item fetched')

    def handle_spider_closed(self):
        return
