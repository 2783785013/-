from utils.my_mysql_add import MySql
from settings import mysql_info, run_time
import time
from datetime import datetime, timedelta
from get_ci_data import *
from loguru import logger

from apscheduler.schedulers.background import BlockingScheduler


coon = MySql()
__coon = MySql(mysql_info, 'sys_pinghu_wx_article_info')


def select_wx_content(news_id):
    datetime_yestoday = (datetime.now() - timedelta(days=4)).strftime('%Y-%m-%d')
    datetime_now = datetime.now().strftime('%Y-%m-%d')
    # sql = f"""-- select title, url, sn, idx, read_count, look_count, good_count, news_time from sys_wx_contents_temp where news_id={news_id} and create_time BETWEEN '{datetime_yestoday} 00:00:00' and '{datetime_now} 00:00:00' """
    sql = f"""select title, url, sn, idx, read_count, look_count, good_count, news_time from sys_wx_contents_temp where news_id={news_id} and create_time BETWEEN '{datetime_yestoday} 00:00:00' and '{datetime_now} 00:00:00' """
    results = coon.getAll(sql)
    # print(333333,results)
    return results


# def select_pinghu_wx_info(sn):
#     sql = f"""select read_count, looking_count, good_count, wci from sys_pinghu_wx_info where article_id={sn} order by create_time desc limit 1"""
#     result = __coon.getOne(sql)
#     return result

def select_pinghu_wx_info(sn):
    sql = f"""select read_count, looking_count, good_count, wci from sys_pinghu_wx_article_info where article_id='{sn}' order by create_time desc limit 1"""
    result = __coon.getOne(sql)
    # print(6666,result)
    return result


def select_best(news_id, yesterday_start_time, yesterday_end_time):
    sql = f"""select news_id from sys_pinghu_wx_article_info where news_id ={news_id} and create_time BETWEEN {yesterday_start_time} and {yesterday_end_time} """
    results = __coon.getOne(sql)
    return results



def change_(item):
    keys_ = item.keys()
    for i in keys_:
        if item[i] == None:
            item[i] = 0
    return item


def pinghu_start():
    spider_data, spider_yestoday_data, yesterday_start_time, yesterday_end_time = run_time()

    pinghu_id_list = ['1149', '1150', '1151', '1152', '1153', '1154', '1155', '1156', '1157', '1158', '1159', '1160',
                      '1161', '1162', '1163', '1164', '1165', '1166', '1167', '1168', '1169', '1170', '1171', '1172',
                      '1173', '1174', '1175', '1176', '1177', '1178', '1179', '1180', '1181', '1182', '1183', '1184',
                      '1185', '1186', '1187', '1188', '1189', '1190', '1191', '1192', '1193', '1194', '1195', '1196',
                      '1197', '1198', '1199', '1200', '1201', '1202', '1203', '1204', '1205', '1206', '1207', '1208',
                      '1209', '1210', '1211', '1212', '1213']
    for pinghu_id in pinghu_id_list:
        # print(1111,pinghu_id)
        results_data = select_wx_content(pinghu_id)
        if select_best(pinghu_id, yesterday_start_time, yesterday_end_time):
            __coon.delete(pinghu_id, yesterday_start_time, yesterday_end_time)
            logger.info('更新完成')
        # print(22222,results_data)
        if results_data:
            for result_data in results_data:
                # print(55555,result_data)
                item = dict()
                title, url, sn, idx, read_count, look_count, good_count, news_time = result_data
                item["news_id"] = pinghu_id
                item["article_id"] = sn
                item["read_count"] = read_count
                item["good_count"] = good_count
                item["looking_count"] = look_count
                item["adapter_type"] = 'ls'
                item["create_time"] = int(time.time() * 1000)
                item["title"] = title
                item["url"] = url
                item["news_time"] = news_time
                if idx == 1:
                    item['is_top'] = 1
                else:
                    item['is_top'] = 0
                best_data = select_pinghu_wx_info(sn)
                change_(item)
                if best_data:
                    old_read_count, old_looking_count, old_good_count, wci = best_data
                    item["read_count_change"] = read_count - old_read_count
                    item["good_count_change"] = good_count - old_good_count
                    item["looking_count_change"] = look_count - old_looking_count
                    item["wci"] = get_wci_ph(item)
                    item["wci_change"] = item["wci"] - wci
                else:
                    item["read_count_change"] = 0
                    item["good_count_change"] = 0
                    item["looking_count_change"] = 0
                    item["wci"] = get_wci_ph(item)
                    item["wci_change"] = 0
                # print(item)
                __coon.insert(item)
                # return item


if __name__ == '__main__':
    print(4444)
    pinghu_start()

    scheduler = BlockingScheduler(timezone='Asia/Shanghai')
    scheduler.add_job(pinghu_start, 'cron', hour='9', minute='30')
    scheduler.add_job(pinghu_start, 'cron', hour='14', minute='30')
    scheduler.start()
