from .sql import Sql
import pprint
from amazon.items import CateItem

class CatePipeline(object):
    def process_item(self,item,spider):
        #print(item)
        ret = Sql.insert_cate_log(item)
        print(ret)
        pass


