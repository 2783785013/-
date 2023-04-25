# -*- coding:utf-8 -*-
#  创建人：l
#  创建时间：
#  说明：
#  版权说明：
import time
from datetime import datetime,timedelta
proxies_info_request = {
    'proxyHost': 'http-dyn.abuyun.com',
    'proxyPort': 9020,
    'proxyUser': "HY64T8526RDTH16D",
    'proxyPass': "345CD5C73411338B",
}


def get_proxies():
    proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
        "host": proxies_info_request['proxyHost'],
        "port": proxies_info_request['proxyPort'],
        "user": proxies_info_request['proxyUser'],
        "pass": proxies_info_request['proxyPass'],
    }
    return {"http": proxyMeta, "https": proxyMeta}


is_testing_environment = True

mysql_info = {
    # 'host': '192.168.31.231',
    # 'port': 3306,
    # 'db': 'aiplat',
    # 'user': 'root',
    # 'password': 'Lsg-tech@2018',
    'host': 'hz.lsgcloud.com',
    'port': 13306,
    'user': 'root',
    'password': 'Lsg-tech@2018',
    'db': 'aiplat',
    'charset': 'utf8',
} if is_testing_environment else {
    'host': '10.0.1.35',
    'port': 6033,
    'db': 'gmrb',
    'user': 'root',
    'password': '159Super753Jian'
}

MYSQL_INFO = {
    # 光明网的本地测试环境
    # 'host': '127.0.0.1',
    # 'port': 3306,
    # 'user': 'root',
    # 'password': '123456',
    # 'db': 'aiplat',
    # 'charset': 'utf8',
    'host': '10.0.1.35',
    'port': 6033,
    'user': 'root',
    'password': '159Super753Jian',
    'db': 'gmrb',
    'charset': 'utf8',
} if is_testing_environment else {
    # 线上数据库
    'ip': '10.0.1.35',
    'port': 6033,
    'user': 'root',
    'password': '159Super753Jian',
    'db': 'gmrb',
    'charset': 'utf8',
}

REDIS_CONNECT = {
    'host': '127.0.0.1',
    'port': '6379',
    'db': 6,
    'password': None
}

proxies_info_request = {
    'proxyHost': 'http-dyn.abuyun.com',
    'proxyPort': 9020,
    'proxyUser': "HY64T8526RDTH16D",
    'proxyPass': "345CD5C73411338B",
}
content_table = 'sys_wb_accounts_info'

def run_time():

    spider_data = datetime.now().strftime('%Y-%m-%d')
    # spider_data = (datetime.now(tz=None) - timedelta(days=2)).strftime('%Y-%m-%d')
    spider_yestoday_data = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

    # timestamp = int(time.time()*1000)
    # timestamp = int(str(int(time.mktime(time.strptime(str(spider_data), '%Y-%m-%d'))) + 100)+'000')

    yesterday_start_time = int(str(int(time.mktime(time.strptime(str(spider_data), '%Y-%m-%d')))) + '000')
    yesterday_end_time = int(str(int(time.mktime(time.strptime(str(spider_data), '%Y-%m-%d'))) + 86400) + '000')

    return spider_data, spider_yestoday_data, yesterday_start_time, yesterday_end_time
    # time.sleep(5)
    # print(spider_data)

if __name__ == '__main__':
    print(run_time())