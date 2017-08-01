from .sql import Sql
from amazon.items import CateItem
from amazon.items import AsinBestItem

class AmazonPipeline(object):
    def process_item(self,item,spider):
        if isinstance(item,CateItem):
            Sql.insert_cate_log(item)
            print('save category: '+ item['title'])
            pass

        if isinstance(item,AsinBestItem):
            Sql.insert_best_asin(item)
            print('save best seller: '+item['asin'])
            pass
        pass





