# -*- coding: UTF-8 -*-
# @author: ylw
# @file: text_utils
# @time: 2021-9-3
# @desc:
import re
import hashlib
import base64
import datetime
import time
from until.my_mysql_add import MySql
from loguru import logger
from settings import content_table
__conn = MySql()


def insert(item):
    """
    插入数据库
    :param item:
    :return:
    """
    keys = ', '.join(item.keys())
    values = ', '.join(['%s'] * len(item))
    sql = f'''insert into {content_table} ({keys}) values ({values})'''
    try:
        __conn.insertOne(sql, tuple(item.values()))
        __conn.end()
        # logger.info(f"入库成功----> {item['title_url']}")
    except Exception as e:
        print(e)
        logger.info(f"入库失败----> {item['title_url']}")


def select_mysql(url):
    sql = f"""SELECT id FROM sys_title_search WHERE title_url = '{url}'"""
    result = __conn.getOne(sql)
    if result:
        return True
    else:
        return False


def match_chinese(text):
    return re.findall('[\u4e00-\u9fa5]', text)


def MD5_(text: str):
    return hashlib.md5(text.encode(encoding='UTF-8')).hexdigest()


def decode_base64(x):
    str_x = x.encode('utf-8')
    str_new = base64.b64decode(str_x)
    return str(str_new)[2:-1]


def get_daytime():
    return datetime.datetime.now().strftime('%Y-%m-%d')


def get_timestamp(time_):
    """
    获取时间戳
    :param time_:
    :return:
    """
    timearry = time.strptime(time_, '%Y-%m-%d %H:%M:%S')
    timestamp = int(time.mktime(timearry))
    return timestamp*1000


if __name__ == '__main__':
    print(decode_base64('aHR0cHM6Ly92OS14Zy13ZWItcGMuaXhpZ3VhLmNvbS9iNjJhZjk5NDQyZTMzYmU1Y2IwYmFlMjQyMTU5MzFkYS82M2VmNWRhNC92aWRlby90b3MvY24vdG9zLWNuLXZlLTRjMDAxLWFsaW5jMi81ZGQwZjgwNzM0OTQ0YTUwOGJiZmVkZjI1ZDNlOGFiZC8\u002FYT0xNzY4JmNoPTAmY3I9MCZkcj0wJmVyPTAmY2Q9MCU3QzAlN0MwJTdDMCZjdj0xJmJyPTI0MyZidD0yNDMmY3M9MCZkcz0xJmZ0PWtUaF9IVlZ5d2hpUkZfODBtb35oRko0WUEwcGlhYlVvfmpLSnpxYWJqRzBQMy1BJm1pbWVfdHlwZT12aWRlb19tcDQmcXM9MCZyYz1PMmRsTjJZNE9EWTVPRHM4T21RNE0wQnBNM1kxYlRNNlpteHFaVE16TkRjek0wQmhMVjh1WXk0ME5tSXhZV0V4TkdNd1lTTnlNRE0yY2pSbmEyeGdMUzFrTFRCemN3JTNEJTNEJmw9MjAyMzAyMTcxNzUyMTFBM0NDQkMwQTczNDhDQTAzNjkwOCZidGFnPTMwMDAw').replace('.\\xd3M\\x85', '?'))