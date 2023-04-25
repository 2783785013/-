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
__coon = MySql(mysql_info,'sys_wb_accounts_info')


def select_original_data(news_id, spider_yestoday_data, spider_data):

    sql = f"""SELECT count(*), avg(good_count), SUM(good_count), max(good_count), avg(comment_count), SUM(comment_count), max(comment_count), avg(forward_count), SUM(forward_count), max(forward_count), avg(read_count), SUM(read_count), max(read_count) FROM sys_wb_contents_temp WHERE news_id={news_id} and news_time BETWEEN '{spider_yestoday_data} 00:00:00' and '{spider_data} 00:00:00' and is_original=0"""
    results = coon.getOne(sql)
    return results


def select_wb_type_data(news_id, spider_yestoday_data, spider_data):

    sql = f"""SELECT count(*), avg(read_count), SUM(read_count), max(read_count), avg(comment_count), SUM(comment_count), max(comment_count), avg(forward_count), SUM(forward_count), max(forward_count) FROM sys_wb_contents_temp WHERE news_id={news_id} and news_time BETWEEN '{spider_yestoday_data} 00:00:00' and '{spider_data} 00:00:00' and wb_type=0"""
    sql_ = f"""SELECT count(*), avg(read_count), SUM(read_count), max(read_count), avg(comment_count), SUM(comment_count), max(comment_count), avg(forward_count), SUM(forward_count), max(forward_count) FROM sys_wb_contents_temp WHERE news_id={news_id} and news_time BETWEEN '{spider_yestoday_data} 00:00:00' and '{spider_data} 00:00:00' and wb_type=1"""
    sql_1 = f"""SELECT count(*), avg(read_count), SUM(read_count), max(read_count), avg(comment_count), SUM(comment_count), max(comment_count), avg(forward_count), SUM(forward_count), max(forward_count) FROM sys_wb_contents_temp WHERE news_id={news_id} and news_time BETWEEN '{spider_yestoday_data} 00:00:00' and '{spider_data} 00:00:00' and wb_type=2"""
    results = coon.getOne(sql)
    results_ = coon.getOne(sql_)
    results_1 = coon.getOne(sql_1)
    return results, results_,results_1

def weibo_accountspider(uid, max_num=0):
    try:
        headers = {
            "referer": f"https://m.weibo.cn/u/2803301701?uid={uid}",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
            "cookie": "SINAGLOBAL=967535490146.727.1606204374469; SUB=_2AkMUmzg7f8NxqwJRmf8cyGrka4V-yg3EieKix8ngJRMxHRl-yT9jqmg-tRB6PxsW1H_i4b5CX-MnCz-CHDoFr9mntiJs; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WhNPPRQgWsLN4QdJ_yqpDBp; UOR=,,m.weibo.cn; XSRF-TOKEN=IVhPfoCqBG-9br3w1rGiniKz; _s_tentry=weibo.com; Apache=7050447082165.822.1679630413837; ULV=1679630413975:10:1:1:7050447082165.822.1679630413837:1676879441689; WBPSESS=xvhb-0KtQV-0lVspmRtyc_bQe2D-CwWM30kvWUOzIzMb2_AA_8Ncy020a9dNflAdlZOokT3Ve7SplH7KyakDiEQwu9vMcwKroh15f3TO0QaRjsRVcCU5IymjfEEfUSJqSorFfPyDGFqnK4w36CYb2QLG-h6gsbLq_8Rp6IIO1K0="
        }
        url = f'https://weibo.com/ajax/profile/info?uid={uid}'
        response = requests.get(url=url, headers=headers).json()
        user_data = response['data']["user"]
        fans = user_data["followers_count"]
        pulish_num = user_data["statuses_count"]
    except Exception as e:
        max_num += 1
        time.sleep(5)
        if max_num < 4:
            logger.info(f'请求失败{uid}:{e}')
            return False, False
    else:
        return fans, pulish_num


def select_data(news_id, spider_yestoday_data, spider_data):

    sql = f"""SELECT count(*), avg(good_count), SUM(good_count), max(good_count), avg(comment_count), SUM(comment_count), max(comment_count), avg(forward_count), SUM(forward_count), max(forward_count), avg(read_count), SUM(read_count), max(read_count),avg(article_read_count) FROM sys_wb_contents_temp WHERE news_id={news_id} and news_time BETWEEN '{spider_yestoday_data} 00:00:00' and '{spider_data} 00:00:00'"""
    results = coon.getOne(sql)

    return results


def select_news():
    sql = """select id, account_id from sys_wb_news"""
    results = coon.getAll(sql)
    return results


def select_best(news_id, yesterday_start_time, yesterday_end_time):
    sql = f"""select news_id from sys_wb_accounts_info where news_id ={news_id} and create_time BETWEEN {yesterday_start_time} and {yesterday_end_time} """
    results = __coon.getOne(sql)
    return results

def select_old_(spider_yestoday_data, spider_data):
    sql = f"""SELECT COUNT(*) from sys_wb_contents_temp where original_source in ("人民日报","新华社","求是","解放军报","光明日报","经济日报","中国日报","中央人民广播电台","中央电视台","中央国际广播电台","科技日报","中国纪检监察报","工人日报","中国青年报","中国妇女报","农民日报","法制日报","中新社") and create_time BETWEEN '{spider_yestoday_data} 00:00:00' and '{spider_data} 00:00:00'"""
    results = coon.getOne(sql)
    return results

# def select_delete(news_id):
#     sql = f"""DELETE from sys_wb_accounts_info where news_id ={news_id} and create_time BETWEEN {yesterday_start_time} and {yesterday_end_time} """
#     __coon.delete(sql)

def change_(item):
    keys_ = item.keys()
    for i in keys_:
        if item[i] == None:
            item[i] = 0
    return item

def wb_start():
    spider_data, spider_yestoday_data, yesterday_start_time, yesterday_end_time = run_time()

    results = select_news()
    # print(results)
    if results:
        for result in results:
            # print(2222,result)
            item = dict()
            news_id, uid = result
            # print(111,news_id)
            fans, pulish_num = weibo_accountspider(uid)
            if select_best(news_id, yesterday_start_time, yesterday_end_time):
                __coon.delete(news_id,  yesterday_start_time, yesterday_end_time)
                logger.info('更新完成')
            if fans:
                item["fans"] = fans
                item["publish_num"] = pulish_num
            else:
                logger.add(f"{datetime.now().strftime('%Y-%m-%d')}.log")
                logger.info(f"失败的id:{news_id}")
                continue
            result_data = select_data(news_id, spider_yestoday_data, spider_data)
            result_data_ = select_original_data(news_id, spider_yestoday_data, spider_data)
            article_data, video_data,blog_data = select_wb_type_data(news_id, spider_yestoday_data, spider_data)
            if result_data and result_data_ and article_data and video_data:
                item["news_id"] = news_id
                item["publish_num_change"] = result_data[0]
                item["likes_num"] = result_data[2]
                item["max_likes_num"] = result_data[3]
                item["read_num"] = result_data[11]
                item["max_read_num"] = result_data[12]
                item["comments_num"] = result_data[5]
                item["max_comments_num"] = result_data[6]
                item["forward_num"] = result_data[8]
                item["max_forward_num"] = result_data[9]
                item["video_publish_num_change"] = video_data[0]
                item["blog_publish_num_change"] = blog_data[0]
                item["article_publish_num_change"] = article_data[0]
                item["original_publish_num_change"] = result_data_[0]
                item["blog_read_num"] = blog_data[2]
                item["original_comments_num"] = result_data_[5]
                item["original_forward_num"] = result_data_[8]

                avg_likes_num = result_data[1]
                avg_read_num = result_data[13]
                avg_comment_num = result_data[4]
            else:
                logger.add(f"{datetime.now().strftime('%Y-%m-%d')}.log")
                logger.info(f"失败的id:{news_id}")
                continue
            old_fans = select_best(news_id, yesterday_start_time, yesterday_end_time)
            if fans and old_fans:
                item["fans_change"] = fans - old_fans[0]
            else:
                item["fans_change"] = 0
            item["adapter_type"] = 'ls'
            item["create_time"] = int(time.time()*1000)

            change_(item)

            item["psi_value"] = get_PSI(item["publish_num_change"])
            item["gi_value"] = get_GI(item['comments_num'])
            item["ci_value"] = get_CI(select_old_(spider_yestoday_data, spider_data)[0])
            item["mii_value"] = get_MII_wb(item,avg_likes_num,avg_read_num,avg_comment_num)

            item['bci'] = get_bci(item)
            # print(item)

            __coon.insert(item)

            # return item


if __name__ == '__main__':
    print(2222)
    wb_start()

    scheduler = BlockingScheduler(timezone='Asia/Shanghai')
    # scheduler.add_job(get, 'cron',second='3')
    scheduler.add_job(wb_start, 'cron', hour='6', minute='00')
    scheduler.add_job(wb_start, 'cron', hour='12', minute='00')
    scheduler.add_job(wb_start, 'cron', hour='18', minute='00')
    scheduler.start()