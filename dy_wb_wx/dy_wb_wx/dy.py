from datetime import datetime,timedelta
from get_secUid import get_secUid
from utils.my_mysql_add import MySql
from loguru import logger
import traceback
from settings import mysql_info
from settings import run_time
from get_main_data import get_data_num
import time
from get_ci_data import *
from get_four_data import *
from apscheduler.schedulers.background import BlockingScheduler

coon = MySql()
coon_1 = MySql(mysql_info,'sys_dy_accounts_info')

def update(item,values):
    keys_list = list(item.keys())
    for i in range(len(keys_list)):
        item[keys_list[i]] = list(values)[i]

    return item

def get_url():
    # sql = '''select id,url from sys_dy_news'''
    sql = '''select id,url from sys_dy_news '''
    data = coon.getAll(sql)
    return data

def change_(item):
    keys_ = item.keys()
    for i in keys_:
        if item[i] == None:
            item[i] = 0
    return item

def get_data(id, sec_uid, spider_yestoday_data, spider_data):
    item = {}
    all_likes_num, fans, publish_num = get_data_num(sec_uid)

    sql_1 = f"""SELECT sum(comment_count),max(comment_count),sum(forward_count),max(forward_count),sum(good_count),max(good_count),avg(comment_count),avg(good_count),count(*) FROM `sys_dy_contents_temp` WHERE news_id = {id} and news_time BETWEEN '{spider_yestoday_data} 00:00:00' and '{spider_data} 00:00:00' """

    result_data = coon.getOne(sql_1)
    # print(111,result_data)
    sql_2 = f"""select fans from sys_dy_accounts_info WHERE news_id = {id}  order by create_time desc LIMIT 1 """
    data = coon_1.getOne(sql_2)
    # print(222,data)

    if data:
        fans_yesterday = data[0]
        item['fans_change'] = fans - fans_yesterday
    else:
        item['fans_change'] = 0

    item['news_id'] = id
    item['fans'] = fans
    item['publish_num'] = publish_num
    item['all_likes_num'] = all_likes_num
    item['likes_num'] = result_data[4]
    item['max_likes_num'] = result_data[5]
    item['comments_num'] = result_data[0]
    item['max_comments_num'] = result_data[1]
    item['forward_num'] = result_data[2]
    item['max_forwar_num'] = result_data[3]

    item['publish_num_change'] = result_data[8]
    item['adapter_type'] = 'ls'
    # item['create_time'] = timestamp
    item['create_time'] = int(time.time()*1000)

    avg_comment_num = result_data[6]
    avg_likes_num = result_data[7]

    change_(item)

    item['psi_value'] = get_PSI(item['publish_num_change'])
    item['ci_value'] = get_CI(1)
    item['gi_value'] = get_GI(item['comments_num'])
    item['mii_value'] = get_MII_dy(item,avg_comment_num,avg_likes_num)

    item['dci'] = get_dci(item)

    # print(66666666,item)

    return item

def select_best(news_id, yesterday_start_time,  yesterday_end_time):

    sql = f"""select * from sys_dy_accounts_info where news_id ={news_id} and create_time BETWEEN {yesterday_start_time} and {yesterday_end_time} """
    results = coon_1.getOne(sql)
    return results

# def select_delete(news_id):
#     sql = f"""DELETE from sys_dy_accounts_info where news_id ={news_id} and create_time BETWEEN {yesterday_start_time} and {yesterday_end_time} """
#     coon_1.

# def select_updata(news_id):
#     sql = f"""select news_id from sys_dy_accounts_info_copy1 where news_id ={news_id} and create_time BETWEEN {yesterday_start_time} and {yesterday_end_time} """
#     results = coon_1.getOne(sql)
#     return results

def dy_start():
    spider_data, spider_yestoday_data, yesterday_start_time, yesterday_end_time = run_time()

    for i in get_url():
        # print(i)
        id_, url = i
        sec_uid = get_secUid(url)
        try:
            if get_data_num(sec_uid):
                if select_best(id_, yesterday_start_time,  yesterday_end_time):
                    coon_1.delete(id_, yesterday_start_time, yesterday_end_time)
                    logger.info('更新完成')
                        # break
                coon_1.insert(get_data(id_, sec_uid, spider_yestoday_data, spider_data))
                # time.sleep(10)
        except Exception as e:
            traceback.print_exc()

if __name__ == '__main__':
    print(1111)
    dy_start()

    scheduler = BlockingScheduler(timezone='Asia/Shanghai')
    scheduler.add_job(dy_start, 'cron', hour='6', minute='00')
    scheduler.add_job(dy_start, 'cron', hour='12', minute='00')
    scheduler.add_job(dy_start, 'cron', hour='18', minute='00')
    scheduler.start()
