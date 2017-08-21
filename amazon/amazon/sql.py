from datetime import datetime

import pymysql

from amazon import settings


def conn_db():
    db_conf = settings.MYSQL
    db_conf['cursorclass'] = pymysql.cursors.DictCursor
    conn = pymysql.connect(**db_conf)
    conn.autocommit(1)
    return conn


def cursor_db(conn):
    return conn.cursor()


class ReviewSql(object):
    conn = conn_db()
    cursor = cursor_db(conn)

    @classmethod
    def insert_profile_item(cls, item):
        sql = "INSERT INTO `py_review_profile`" \
              "(`asin`, `product`, `brand`, `seller`, `image`," \
              "`review_total`, `review_rate`, `pct_five`, `pct_four`, `pct_three`, " \
              "`pct_two`, `pct_one`, `latest_total`) " \
              "VALUES ('%s', %s, %s, %s, '%s', '%s', " \
              "'%s', '%s', '%s', '%s', '%s', '%s', 0)" %\
              (item['asin'], cls.conn.escape(item['product']), cls.conn.escape(item['brand']), cls.conn.escape(item['seller']), item['image'],
               item['review_total'], item['review_rate'], item['pct_five'], item['pct_four'],
               item['pct_three'], item['pct_two'], item['pct_one'])
        try:
            if cls.check_exist_profile(item['asin']):
                cls.update_profile_item(item)
                print('update review profile--[asin]:', item['asin'])
            else:
                cls.cursor.execute(sql)
                cls.conn.commit()
                print('save review profile--[asin]:', item['asin'])
        except pymysql.MySQLError as e:
            with open('sql.log', 'r+') as i:
                i.write('profile sql error![error]:'+e)
            print(e)
            cls.conn.rollback()
        pass

    @classmethod
    def update_profile_item(cls, item):
        sql = "UPDATE `py_review_profile` SET `latest_total`=`review_total`,`product`=%s, `brand`=%s, `seller`=%s, `image`=%s, `review_total`='%s', `review_rate`='%s'," \
              "`pct_five`='%s', `pct_four`='%s', `pct_three`='%s', `pct_two`='%s', `pct_one`='%s' " \
              "WHERE `asin`='%s'" % \
              (cls.conn.escape(item['product']), cls.conn.escape(item['brand']), cls.conn.escape(item['seller']), cls.conn.escape(item['image']),
               item['review_total'], item['review_rate'],item['pct_five'], item['pct_four'], item['pct_three'], item['pct_two'],
               item['pct_one'], item['asin'])
        try:
            cls.cursor.execute(sql)
            cls.conn.commit()
        except pymysql.MySQLError as e:
            print(e)
            cls.conn.rollback()

    @classmethod
    def check_exist_profile(cls, asin):
        sql = "SELECT * FROM `py_review_profile` WHERE (`asin` = '%s')" % (asin)
        result = cls.cursor.execute(sql)
        if result:
            return True
        else:
            return False

    @classmethod
    def insert_detail_item(cls, item):
        sql = "INSERT INTO `py_review_detail`(`asin`, `review_id`, `reviewer`, `review_url`, `star`, `date`, `title`, `content`) " \
              "VALUES ('%s', '%s', %s, '%s', '%s', '%s', %s, %s)" % \
              (item['asin'], item['review_id'], cls.conn.escape(item['reviewer']), item['review_url'], item['star'],
               item['date'], cls.conn.escape(item['title']), cls.conn.escape(item['content']))
        try:
            if cls.check_exist_detail(item['asin'], item['review_id']) is not True:
                print('save review detail--[asin]:', item['asin'], '[reviewID]:', item['review_id'])
                cls.cursor.execute(sql)
                cls.conn.commit()
        except pymysql.MySQLError as e:
            print(e)
            cls.conn.rollback()
        pass

    @classmethod
    def check_exist_detail(cls, asin, review_id):
        sql = "SELECT * FROM `py_review_detail` WHERE `asin` = '%s' AND `review_id`='%s'" % (asin, review_id)
        result = cls.cursor.execute(sql)
        if result:
            return True
        else:
            return False

    @classmethod
    def get_last_review_total(cls, asin):
        sql = "SELECT `review_total`, `latest_total` FROM `py_review_profile` WHERE `asin`='%s'" % asin
        cls.cursor.execute(sql)
        item = cls.cursor.fetchone()
        if item:
            return item['latest_total']
        else:
            return False

    @classmethod
    def update_profile_self(cls, asin):
        sql = "UPDATE `py_review_profile` SET `latest_total` = `review_total` WHERE `asin`='%s'" % asin
        cls.cursor.execute(sql)
        cls.conn.commit()


class RankingSql(object):
    conn = conn_db()
    cursor = cursor_db(conn)
    py_keyword_table = 'py_salesranking_keywords'  # 爬虫抓
    py_sales_table = 'py_salesrankings'
    keyword_table = 'salesranking_keywords'
    sales_table = 'salesrankings'

    @classmethod
    def insert_sales_ranking(cls, item):
        sql = "INSERT INTO `%s`(`sk_id`, `rank`, `classify`, `date`) VALUES ('%s', '%s', %s, '%s')" % \
              (cls.py_sales_table, item['sk_id'], item['rank'], cls.conn.escape(item['classify']), datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        update_sql = "UPDATE `%s` SET `last_rank`=`rank`, `classify`=%s, `rank`='%s', `updated_at`=NOW() WHERE `id`='%s'" % \
                     (cls.sales_table, cls.conn.escape(item['classify']), item['rank'], item['sk_id'])
        try:
            cls.cursor.execute(sql)
            cls.cursor.execute(update_sql)
            cls.conn.commit()
        except pymysql.DatabaseError as error:
            print(error)
            cls.conn.rollback()

    @classmethod
    def insert_keyword_ranking(cls, item):
        sql = "INSERT INTO `%s`(`skwd_id`, `rank`, `date`) VALUES ('%s', '%s', '%s')" % \
              (cls.py_keyword_table, item['skwd_id'], item['rank'], datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        update_sql = "UPDATE `%s` SET `last_rank`=`rank`, `rank`='%s', `updated_at`=NOW() WHERE `id`='%s'" % \
                     (cls.keyword_table, item['rank'], item['skwd_id'])
        try:
            cls.cursor.execute(sql)
            cls.cursor.execute(update_sql)
            cls.conn.commit()
        except pymysql.DatabaseError as error:
            print(error)
            cls.conn.rollback()

    @classmethod
    def fetch_sales_ranking(cls):
        sql = "SELECT `id`, `asin` FROM `%s`WHERE `status` =1" % cls.sales_table
        cls.cursor.execute(sql)
        item = cls.cursor.fetchall()
        return item

    @classmethod
    def fetch_keywords_ranking(cls):
        sql = "SELECT `a`.`id`, `a`.`keyword`, `a`.`rank` as `rank`, `b`.`asin` as `asin` FROM `%s` as `a` " \
              "LEFT JOIN `%s` as `b` ON `b`.`id`=`a`.`sk_id`" % \
              (cls.keyword_table, cls.sales_table)
        cls.cursor.execute(sql)
        item = cls.cursor.fetchall()
        return item

    @classmethod
    def update_keywords_expire_rank(cls, skwd_id):
        sql = "UPDATE `%s` SET `last_rank`=`rank`, `rank`=321, `updated_at`=NOW() WHERE `id`='%s'" % (cls.keyword_table, skwd_id)
        py_sql = "INSERT INTO `%s`(`skwd_id`, `rank`, `date`) VALUES ('%s', 321, NOW())" % (cls.py_keyword_table, skwd_id)
        try:
            cls.cursor.execute(sql)
            cls.cursor.execute(py_sql)
            cls.conn.commit()
        except pymysql.DataError as error:
            print(error)
            cls.conn.rollback()





