import requests
from datetime import datetime, timedelta
from loguru import logger
import time
from utils.my_mysql_add import MySql
from settings import mysql_info, run_time
from get_ci_data import *
from get_four_data import *
from apscheduler.schedulers.background import BlockingScheduler


coon = MySql()
__coon = MySql(mysql_info,'sys_wx_accounts_info')





def select_data(news_id, spider_yestoday_data, spider_data):
    """
    全部点赞 阅读 在看
    :param news_id:
    :return:
    """

    sql = f"""SELECT count(*), avg(read_count), SUM(read_count), max(read_count), avg(good_count), SUM(good_count), max(good_count), avg(look_count), SUM(look_count), max(look_count),sum(comment_count),avg(comment_count),max(comment_count) FROM sys_wx_contents_temp WHERE news_id={news_id} and news_time >'{spider_yestoday_data} 00:00:00' and news_time <'{spider_data} 00:00:00'"""
    results = coon.getOne(sql)
    return results


def select_toutiao_data(news_id, spider_yestoday_data, spider_data):
    """
    微信头条点赞 阅读 在看
    :param news_id:
    :return:
    """


    sql = f"""SELECT count(*), avg(read_count), SUM(read_count), max(read_count), avg(good_count), SUM(good_count), max(good_count), avg(look_count), SUM(look_count), max(look_count) FROM sys_wx_contents_temp WHERE news_id={news_id} and news_time BETWEEN '{spider_yestoday_data} 00:00:00' and '{spider_data} 00:00:00' and idx=1"""
    results = coon.getOne(sql)
    return results


def select_notoutiao_data(news_id, spider_yestoday_data, spider_data):
    """
    非头条点赞 阅读 在看
    :param news_id:
    :return:
    """


    sql = f"""SELECT count(*), avg(read_count), SUM(read_count), max(read_count), avg(good_count), SUM(good_count), max(good_count), avg(look_count), SUM(look_count), max(look_count) FROM sys_wx_contents_temp WHERE news_id={news_id} and news_time BETWEEN '{spider_yestoday_data} 00:00:00' and '{spider_data} 00:00:00' and idx != 1"""
    results = coon.getOne(sql)
    return results


def select_da10W_data(news_id, spider_yestoday_data, spider_data):
    """
    超10W阅读文章数
    :param news_id:
    :return:
    """

    sql = f"""SELECT count(*) FROM sys_wx_contents_temp WHERE news_id={news_id} and news_time BETWEEN '{spider_yestoday_data} 00:00:00' and '{spider_data} 00:00:00' and read_count > 100000"""
    results = coon.getOne(sql)
    return results


def select_news():
    sql = """select id from sys_wx_news"""
    results = coon.getAll(sql)
    return results


def select_best(news_id, yesterday_start_time, yesterday_end_time):
    sql = f"""select news_id from sys_wx_accounts_info where news_id ={news_id} and create_time BETWEEN {yesterday_start_time} and {yesterday_end_time} """
    results = __coon.getOne(sql)
    return results

def select_old_(spider_yestoday_data, spider_data):
    sql = f"""SELECT COUNT(*) from sys_wx_contents_temp where original_source in ("人民日报","新华社","求是","解放军报","光明日报","经济日报","中国日报","中央人民广播电台","中央电视台","中央国际广播电台","科技日报","中国纪检监察报","工人日报","中国青年报","中国妇女报","农民日报","法制日报","中新社") and create_time BETWEEN '{spider_yestoday_data} 00:00:00' and '{spider_data} 00:00:00'"""
    results = coon.getOne(sql)
    return results

def change_(item):
    keys_ = item.keys()
    for i in keys_:
        if item[i] == None:
            item[i] = 0
    return item

def wx_start():
    spider_data, spider_yestoday_data, yesterday_start_time, yesterday_end_time = run_time()

    results = select_news()
    # print(222,results)
    if results:
        for news_id in results:
            if select_best(news_id[0], yesterday_start_time, yesterday_end_time):
                __coon.delete(news_id[0], yesterday_start_time, yesterday_end_time)
                logger.info('更新完成')
                # continue
            item = dict()
            result_data = select_data(news_id[0], spider_yestoday_data, spider_data)
            result_data_ = select_toutiao_data(news_id[0], spider_yestoday_data, spider_data)
            no_result_data = select_notoutiao_data(news_id[0], spider_yestoday_data, spider_data)
            da10W_result = select_da10W_data(news_id[0], spider_yestoday_data, spider_data)
            if result_data and result_data_ and no_result_data and da10W_result:
                item["news_id"] = news_id[0]
                item["publish_num_change"] = result_data[0]
                item["top_publish_num_change"] = result_data_[0]
                item["likes_num"] = result_data[5]
                item["max_likes_num"] = result_data[6]
                item["read_num"] = result_data[2]
                item["max_read_num"] = result_data[3]
                item["look_num"] = result_data[8]
                item["max_look_num"] = result_data[9]
                item["top_likes_num"] = result_data_[5]
                item["top_max_likes_num"] = result_data_[6]
                item["top_read_num"] = result_data_[2]
                item["top_max_read_num"] = result_data_[3]
                item["top_look_num"] = result_data_[8]
                item["top_max_look_num"] = result_data_[9]
                item["no_top_max_likes_num"] = no_result_data[6]
                item["no_top_max_read_num"] = no_result_data[3]
                item["no_top_max_read_num"] = no_result_data[3]
                item["gt_100000_read_count"] = da10W_result[0]

                get_mii_wx_dict = {}
                get_mii_wx_dict['likes_num'] = result_data[5]
                get_mii_wx_dict['avg_likes_num'] = result_data[4]
                get_mii_wx_dict['max_likes_num'] = result_data[6]

                get_mii_wx_dict['avg_read_num'] = result_data[1]

                get_mii_wx_dict['comments_num'] = result_data[10]
                get_mii_wx_dict['avg_comment_num'] = result_data[11]
                get_mii_wx_dict['max_comments_num'] = result_data[12]
            else:
                logger.add(f"{datetime.now().strftime('%Y-%m-%d')}.log")
                logger.info(f"失败的id:{news_id}")
                continue
            item["adapter_type"] = 'ls'
            item["create_time"] = int(time.time()*1000)

            change_(item)
            change_(get_mii_wx_dict)
            item["psi_value"] = get_PSI(item['publish_num_change'])
            item["gi_value"] = get_GI(1)
            item["ci_value"] = get_CI(select_old_(spider_yestoday_data, spider_data)[0])
            item["mii_value"] = get_MII_wx(item,get_mii_wx_dict)

            item['wci'] = get_wci(item)

            __coon.insert(item)
            # print(item)
            # return item

if __name__ == '__main__':
    print(3333)
    wx_start()

    scheduler = BlockingScheduler(timezone='Asia/Shanghai')
    scheduler.add_job(wx_start, 'cron', hour='9', minute='30')
    scheduler.add_job(wx_start, 'cron', hour='14', minute='30')
    scheduler.start()