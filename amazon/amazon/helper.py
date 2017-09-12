import datetime

import re
import pytz

from math import ceil
from random import Random

from amazon import settings


class Helper(object):
    tz = pytz.timezone(settings.TIMEZONE)

    @classmethod
    def get_num_split_comma(cls, value):
        num = value.split(',')
        ranknum = ''
        if len(num) > 1:
            for n in num:
                ranknum += n
            return ranknum
        else:
            return value

    @classmethod
    def get_star_split_str(cls, value):
        rate = value.split('out of 5 stars')   # 分割字符串
        return rate[0].strip()

    @classmethod
    def get_date_split_str(cls, value):
        return value.split('on')[1].strip()

    @classmethod
    def convert_date_str(cls, date_str):
        return datetime.datetime.strptime(date_str, '%B %d, %Y')

    @classmethod
    def delay_forty_days(cls):
        now = datetime.datetime.now()
        delay14 = now + datetime.timedelta(days=-40)  # 计算往前40天之后的时间
        return delay14

    @classmethod
    def get_rank_classify(cls, spider_str):
        result = re.match(r'#([0-9,]+)(?:.*)in (.*) \(.*[Ss]ee [Tt]op.*\)', spider_str)
        return result.groups()

    @classmethod
    def get_keyword_page_num(cls, rank):
        page_num = ceil(int(rank) / 16)
        return page_num

    @classmethod
    def get_keyword_page_range(cls, page_num):
        return range(page_num - 4 if page_num - 4 > 0 else 1, page_num + 4 if page_num + 4 <= 20 else 20)

    @classmethod
    def random_str(cls, randomlength):
        str = ''
        chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
        length = len(chars) - 1
        random = Random()
        for i in range(randomlength):
            str += chars[random.randint(0, length)]
        return str

    @classmethod
    def get_now_date(cls):
        now = datetime.datetime.now(cls.tz).strftime('%Y-%m-%d %H:%M:%S')
        return now
