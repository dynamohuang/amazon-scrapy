import json
import random
import redis
import time
from amazon import settings


class ProxyMiddleware(object):
    def __init__(self):
        with open('proxy.json', 'r') as f:
            self.proxies = json.load(f)
            self.r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB,
                                 password=settings.REDIS_PASSWORD)

    def process_request(self, request, spider):
        while True:
            proxy = random.choice(self.proxies)
            if self.proxyReady(proxy):
                request.meta['proxy'] = 'http://{}'.format(proxy)
                break

    def proxyReady(self, proxy):
        key = proxy + settings.BOT_NAME
        retult = self.r.exists(key)
        if retult:
            return False
        else:
            self.r.setex(key, 1, 15)
            return True
