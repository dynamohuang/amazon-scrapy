import scrapy
import json
from amazon.mysqlpipelines.pipelines import Sql
class AsinSpider(scrapy.Spider):
    name = "asin"

    def start_requests(self):
        cates = Sql.findall_cate_level1()
        for row in cates:
            row['link'] += '?ajax=1'
            yield scrapy.Request(url=row['link']+'&pg=1', callback=self.parse,meta={'cid':row['id'],'page':1,'link':row['link']})

    def parse(self, response):
        list = response.css('.zg_itemImmersion')
        for row in list:
            try:
                info = row.css('.zg_itemWrapper')[0].css('div::attr(data-p13n-asin-metadata)')[0].extract()
            except:
                continue
                pass
            info = json.loads(info)
            print(info['asin'])

        page = response.meta['page'] + 1

        if page < 5:
            yield scrapy.Request(url=response.meta['link']+'&pg='+str(page), callback=self.parse, meta=response.meta)


