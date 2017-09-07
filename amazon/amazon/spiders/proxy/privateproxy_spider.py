import scrapy
import json
import pymysql
from  amazon import settings

class privateproxySpider(scrapy.Spider):
    name = "privateproxy"
    custom_settings = {
        'LOG_LEVEL': 'ERROR',
        'LOG_ENABLED': True,
        'LOG_STDOUT': True
    }

    def start_requests(self):
        url = "http://www.qq.com"
        db = pymysql.connect(settings.MYSQL_HOST, settings.MYSQL_USER, settings.MYSQL_PASSWORD, settings.MYSQL_DB, charset=settings.MYSQL_CHARSET, cursorclass=pymysql.cursors.DictCursor)
        cursor = db.cursor()

        sql = "SELECT CONCAT_WS(':', ip, port) AS proxy FROM proxy where work = 1"
        cursor.execute(sql)

        proxy_array = []
        proxy_list = cursor.fetchall()
        for item in proxy_list:
            proxy_array.append(item['proxy'])

        with open('proxy.json', 'w') as f:
            json.dump(proxy_array, f)
        yield scrapy.Request(url=url, callback=self.parse, meta={})

    def parse(self, response):
        print('proxy update done')





