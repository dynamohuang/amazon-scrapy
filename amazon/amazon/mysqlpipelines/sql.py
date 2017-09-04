import pymysql
from  amazon import settings


db = pymysql.connect(settings.MYSQL_HOST, settings.MYSQL_USER,settings.MYSQL_PASSWORD,settings.MYSQL_DB,charset='utf8',cursorclass=pymysql.cursors.DictCursor)
cursor = db.cursor()


class Sql:

    asin_pool = []

    @classmethod
    def insert_cate_log(cls, item):
        sql = "INSERT INTO py_cates (title,link,level,pid) VALUES ('%s', '%s','%d','%d')" % (item['title'],item['link'],item['level'],item['pid'])
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
        pass


    @classmethod
    def cache_best_asin(cls, item):
        cls.asin_pool.append((item['asin'], item['cid'], item['rank']))
        pass

    @classmethod
    def store_cate_level1(cls):
        sql = "INSERT INTO py_asin_best (asin,cid,rank) VALUES (%s, %s, %s)"
        try:
            cursor.executemany(sql,cls.asin_pool)
            db.commit()
        except Exception as err:
            print(err)
            db.rollback()
        pass


    @classmethod
    def findall_cate_level1(cls):
        sql = "SELECT id,link FROM py_cates WHERE level < 2"
        cursor.execute(sql)
        return cursor.fetchall()

    @classmethod
    def findall_asin_level1(cls):
        sql = "SELECT distinct(asin), cid FROM py_asin_best limit 0,300"
        cursor.execute(sql)
        return cursor.fetchall()




