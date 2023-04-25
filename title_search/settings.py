# -*- coding: UTF-8 -*-
proxies_info_request = {
    'proxyHost': 'http-dyn.abuyun.com',
    'proxyPort': 9020,
    'proxyUser': "HY64T8526RDTH16D",
    'proxyPass': "345CD5C73411338B",
}

is_test = True


REDIS_CONNECT = {
    'host': '121.5.62.79',
    'port': '16379',
    'db': 0,
    'password': 'Lsg-tech@2018'
}
# REDIS_CONNECT = {
#     'host': '127.0.0.1',
#     'port': '6379',
#     'db': 2,
#     'password': None
# } if is_test else {
#     'host': '10.0.1.44',
#     'port': 6338,
#     'db': 1,
#     'password': 'admin@NBwhy0504',
# }

MYSQL_INFO = {
    # # 测试数据库
    # 'ip': '192.168.31.231',
    # 'port': 3306,
    # 'user': 'root',
    # 'password': 'Lsg-tech@2018',
    # 'db': 'bwg',
    # 'charset': 'utf8',
    # 'use_unicode': True
    # 光明网的本地测试环境
    'ip': 'hz.lsgcloud.com',
    'port': 13306,
    'user': 'root',
    'password': 'Lsg-tech@2018',
    'db': 'aiplat',
    'charset': 'utf8',
    'use_unicode': True

} if is_test else {
    # 线上数据库
    'ip': '10.0.1.35',
    'port': 6033,
    'user': 'root',
    'password': '159Super753Jian',
    'db': 'gmrb',
    'charset': 'utf8',
}

content_table = 'sys_title_search'

ua_list = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1623.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.15 (KHTML, like Gecko) Chrome/24.0.1295.0 Safari/537.15',
    'Mozilla/5.0 (Windows NT 6.4; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; rv:6.0) Gecko/20100101 Firefox/19.0',
    'Opera/9.80 (Windows NT 6.0; U; pl) Presto/2.7.62 Version/11.01',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1866.237 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1464.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.15 (KHTML, like Gecko) Chrome/24.0.1295.0 Safari/537.15',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1866.237 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; rv:21.0) Gecko/20100101 Firefox/21.0',
    'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.60 Safari/537.17',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.62 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.62 Safari/537.36',
    'Mozilla/5.0 (Windows; U; Windows NT 6.0; fr-FR) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36 Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1500.55 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; rv:21.0) Gecko/20100101 Firefox/21.0',
    'Mozilla/5.0 (Windows; U; Windows NT 6.0; fr-FR) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2309.372 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2309.372 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:16.0.1) Gecko/20121011 Firefox/21.0.1',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.2 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20130401 Firefox/21.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1623.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.62 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; rv:21.0) Gecko/20130326 Firefox/21.0',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2117.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.3319.102 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1464.0 Safari/537.36',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; ru-RU) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36 Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1866.237 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.14 (KHTML, like Gecko) Chrome/24.0.1292.0 Safari/537.14',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1623.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.15 (KHTML, like Gecko) Chrome/24.0.1295.0 Safari/537.15',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.16 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2309.372 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.15 (KHTML, like Gecko) Chrome/24.0.1295.0 Safari/537.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1664.3 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1467.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1500.55 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.15 (KHTML, like Gecko) Chrome/24.0.1295.0 Safari/537.15',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:23.0) Gecko/20131011 Firefox/23.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1623.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
    'Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.16 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.3319.102 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; rv:21.0) Gecko/20100101 Firefox/21.0'
]

baidu_cookie = [
    'BAIDUID=243E09E281018766F78DF62DDDEBF874:FG=1; BIDUPSID=4B861996CF79AD3BF418665A5E4AEC1E; PSTM=1653543232; ZFY=sVGdQ:Bqm3qXgLCfh:B8BNieGQaI4OvtWmaOoip2PW:B9o:C; channel=baidusearch; BAIDUID_BFESS=243E09E281018766F78DF62DDDEBF874:FG=1; BD_HOME=1; delPer=0; BD_CK_SAM=1; PSINO=7; BD_UPN=12314753; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BA_HECTOR=2185al248124a52h0l0405qk1hutogi1l; baikeVisitId=bf8ab2bc-b58b-4321-bc3d-dee65e05b610; BDRCVFR[S4-dAuiWMmn]=I67x6TjHwwYf0; H_PS_645EC=61a3iFSce0BQUWOce1IKN3WJiqHjcrUd7t870Ky6TcC7xWIhL9z2HiGwJ2I61L98Bg; BDRCVFR[C0p6oIjvx-c]=YaW3xZxuu8DfAF9pywdIAqsnH0; BDSVRTM=330; H_PS_PSSID=36559_38105_38057_37911_38149_37989_38177_38174_36806_37937_38089_37958_38102_38008_37881',
    'BIDUPSID=513C4B90C43DECA3D72F3B508C654123; PSTM=1676513107; BAIDUID=513C4B90C43DECA362878CC8E97E8C41:FG=1; BD_UPN=12314753; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; H_PS_PSSID=36559_38059_37906_38149_37989_38179_38174_36803_37928_26350_38137_38008_37881; BA_HECTOR=808k0k018k848585812k2hs81hus06b1k; delPer=0; BD_CK_SAM=1; PSINO=5; ZFY=fJzRU82v:AYh08iwugmU1POBaVae8PA4a2GbiUCqIcpU:C; BAIDUID_BFESS=513C4B90C43DECA362878CC8E97E8C41:FG=1; BD_HOME=1; baikeVisitId=30e02d3a-64d7-4e9a-9259-85b4358aef2f; ab_sr=1.0.1_NDI4MjA1YjBmMTEwZWY5YmU1YTY0MzAxZDdlNWJhZWM3ZGI0ZGRiYjQyNDJmZWQxOGUwYTJiMTVhZTRkNGE2ZTVjMjA5NDM3NTE0ZWQ1N2IwYWI3MWU5ZjVmYjdiODIxNDVmOWZlNGE1OGIzZmRiMjgzMmUwMGUzOGIyZDFlZGYxMzcwNzg0NDQxZWQ5Zjk5ZGYyODI3MmYwNWFlYzdlMA==; COOKIE_SESSION=38_0_7_7_6_18_0_0_7_6_2_2_64749_0_97_0_1676597605_0_1676597508%7C9%230_0_1676597508%7C1; kleck=e706e8c2b9d22f8d503a3616a606b63b; H_PS_645EC=dd13Nc%2BkZ7509%2BT9WrSVJkcjWYcWINKHU3zsiU%2BYf%2F6VzstG6THPQS66jio; WWW_ST=1676599977617',
    'BIDUPSID=513C4B90C43DECA3D72F3B508C654123; PSTM=1676513107; BAIDUID=513C4B90C43DECA362878CC8E97E8C41:FG=1; BD_UPN=12314753; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; H_PS_PSSID=36559_38059_37906_38149_37989_38179_38174_36803_37928_26350_38137_38008_37881; ab_sr=1.0.1_YWVmZTAyYTk3ZWUyMTA2MTdlZjFmZDVhMWVmYjUwMGU5MDEzMTA1NDMwYTVmYTgxOTRlOTBlNjRkNmZkZjZkNWVjZjZlMGJlZTE5YTRjZjM1NzU5YTRiZDIxNGU0NjgwYTRmMjBhYmY5ZTA2OWU4NWQ2MTFkMGM4YTIyOTZlZTJjNjZhNjE1MDczZWE0ZTJjMDkwY2Q1OTBjN2ZhZjRjOQ==; BA_HECTOR=808k0k018k848585812k2hs81hus06b1k; delPer=0; BD_CK_SAM=1; PSINO=5; ZFY=fJzRU82v:AYh08iwugmU1POBaVae8PA4a2GbiUCqIcpU:C; BAIDUID_BFESS=513C4B90C43DECA362878CC8E97E8C41:FG=1; H_PS_645EC=eb588Q41ZexRQSmwoech3LEY2%2FrXUkAxAVTHFpj%2B2pvvMFYoibA5aC%2B96LU; BDSVRTM=150'
]
