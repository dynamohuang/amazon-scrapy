import pymysql
from  amazon import settings


db = pymysql.connect(settings.MYSQL_HOST, settings.MYSQL_USER,settings.MYSQL_PASSWORD,settings.MYSQL_DB,cursorclass=pymysql.cursors.DictCursor)
cursor = db.cursor()


class Sql:

    @classmethod
    def insert_cate_log(cls, item):
        sql = "INSERT INTO py_cates (title,link,level,pid) VALUES ('%s', '%s','%d','%d')" % (item['title'],item['link'],item['level'],item['pid'])
        try:
            #print(sql)
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
        pass


    @classmethod
    def findall_cate_level1(cls):
        sql = "SELECT id,link FROM py_cates WHERE level = 1"
        cursor.execute(sql)
        return cursor.fetchall()




