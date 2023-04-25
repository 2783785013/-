# -*- coding: UTF-8 -*-
import aiohttp
import asyncio
import traceback
from urllib.parse import urlencode
from loguru import logger
# from until.text_until import insert
from until.my_mysql_add import MySql
import re
import json
import datetime
__conn = MySql()


async def request_on(session, method, seam, url, response_type, headers, params, data, cookies, proxy, max_num=5, *args,
                     **kwargs):
    """
    发出请求
    :param session:
    :param method:
    :param seam:
    :param url:
    :param response_type:
    :param headers:
    :param params:
    :param data:
    :param proxy:
    :param cookies:
    :param max_num: 最大重试次数
    :param args:
    :param kwargs:
    :return: 响应
    """
    for try_num in range(max_num):
        try:
            async with seam:
                async with session.request(method, url, headers=headers, params=params, data=data, cookies=cookies,
                                           proxy=proxy, timeout=10, verify_ssl=False) as response:
                    if response_type == 'str':
                        result = await response.text()
                    else:
                        result = await response.json()
        except Exception as e:
            if try_num == max_num - 1:
                # traceback.print_exc()
                url = url+"?" + urlencode(params) if params else url
                logger.info(f'请求失败了：{url}{e}')
                return False
            else:
                continue
        else:
            if response.status == 200:
                return result
            else:
                if try_num == max_num - 1:
                    return False
                else:
                    continue


async def start(urls: list, num, method, response_type, headers, params, data, cookies, proxy, *args, **kwargs):
    """
    创建task
    :param urls:
    :param num:
    :param method:
    :param response_type:
    :param headers:
    :param params:
    :param data:
    :param proxy:
    :param cookies:
    :param args:
    :param kwargs:
    :return:
    """
    seam = asyncio.Semaphore(num)
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.create_task(
            request_on(session, method, seam, url, response_type, headers, params, data, cookies, proxy, *args,
                       **kwargs)) for url in urls]
        return await asyncio.wait(tasks)


def start_run_(urls: list or str, num=5, method='get', response_type='str', headers=None, params=None, data=None,
               proxy=None, cookies=None, *args, **kwargs):
    """
    启动
    :param urls: 请求urls:list
    :param num: 最大并发数 默认5
    :param method: 请求方式 默认get
    :param response_type: 响应数据类型 默认str, 否则json
    :param headers: 请求头
    :param params:
    :param data:
    :param proxy:
    :param cookies:
    :param args:
    :param kwargs:
    :return:
    """
    if headers is None:
        headers = dict()
        headers[
            'User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
    if type(urls) == list:
        done, set_ = asyncio.get_event_loop().run_until_complete(
            start(urls, num, method, response_type, headers, params, data, cookies, proxy, *args, **kwargs))
        response_list = [d.result() for d in done]
        return response_list
    else:
        done, set_ = asyncio.get_event_loop().run_until_complete(
            start([urls], num, method, response_type, headers, params, data, cookies, proxy, *args, **kwargs))
        for d in done:
            return d.result()


if __name__ == '__main__':
    # url_1 = 'https://m.weibo.cn/status/MtRdZ0j8R?mblogid=MtRdZ0j8R&luicode=10000011&lfid=1076035031134493'
    # url_2 = 'https://www.zh.gov.cn/col/col1229624743/index.html'
    # url_3 = 'https://proxy.cztvclo/api/fusion/pc/news/list?appId=1024&channelId=506&limit=10&page=1'
    # a, b = asyncio.run(start([url_3], response_type='1'))
    # for c in a:
    #     print(c.result())
    # print(request_one(url_3, response_type='1'))
    # for a in start_run_(url_1):
    #     if not a:
    #         print(a)
    def source_re(aaa, text):
        source = re.findall(f'{aaa}：.*?[\u4e00-\u9fa5]+.*?|{aaa}:.*?[\u4e00-\u9fa5]+.*?', text, re.S | re.M)
        # print(source)
        if ''.join(source).strip():
            s_ = []
            for s in source:
                if s.strip():
                    source = re.sub(f'{aaa}：|{aaa}:|编辑|<.*?>|综合自|\s+|&nbsp;', '', s.strip(), 0, re.S | re.M)
                    if source not in s_ and len(source) < 30:
                        s_.append(source)
            if s_:
                return s_[0]
            else:
                return False
        else:
            return False

    def set_title(content):
        result1 = re.findall('【.*?】', content)
        result2 = re.findall('#.*#', ddd[0]["status"]["text"], re.S | re.M)
        set_title_length = len(content) if len(content) < 20 else 20
        if result1:
            title1 = re.sub(f'<.*?>|&nbsp;', '', result1[0], 0, re.S | re.M)
        else:
            if result2:
                title1 = re.sub(f'<.*?>|&nbsp;', '', result2[0], 0, re.S | re.M)
            else:
                title1 = content[:set_title_length]
        return title1


    def insert(item):
        """
        插入数据库
        :param item:
        :return:
        """
        keys = ', '.join(item.keys())
        values = ', '.join(['%s'] * len(item))
        sql = f'''insert into sys_exhibition_infomation ({keys}) values ({values})'''
        try:
            __conn.insertOne(sql, tuple(item.values()))
            __conn.end()
            logger.info(f"入库成功----> {item['title']}")
        except Exception as e:
            print(e)
            logger.info(f"入库失败----> {item['title']}")

    def match_time(aaa, text):
        source = re.findall(f'{aaa}:.*?日.*?日|{aaa}：.*?日.*?日', text, re.S | re.M)
        if ''.join(source).strip():
            s_ = []
            for s in source:
                if s.strip():
                    source = re.sub(f'{aaa}：|{aaa}:|编辑|<.*?>|综合自|\s+|&nbsp;', '', s.strip(), 0, re.S | re.M)
                    if source not in s_ and len(source) < 30:
                        s_.append(source)
            if s_:
                return s_[0]
            else:
                return False
        else:
            return False


    def get_new_content(str_):
        amd = re.sub(
            '<!--.*?-->|<script.*?</script>|<spanyes.*?>|</spanyes.*?>|<w:.*?>|</w:.*?>|<font.*?>|</font>|<o:p.*?>|</o:p>|<style>.*?</style>|style=".*?"|d=".*?"|heihgt=".*?"|width=".*?"|color=".*?"|bgcolor=".*?"',
            '', str_, 0, re.M | re.S)
        return amd
    sql = """SELECT source_name, net_url FROM sys_wb_contents WHERE content like '%画展%' or content like '%瓷器展%'  or content like '%文物展%' or content like '%联展%' or content like '%特展%' or content like '%精品展%' or content like '%作品展%' or content like '%特展%' or content like '%事迹展%' or content like '%艺术展%' or content like '%专题展%' or content like '%图片展%' or content like '%陈列展%' or content like '%文化展%' or content like '%史料展%' or content like '%特展%' or content like '%精神展%' or content like '%物证展%' or content like '%剪纸展%' or content like '%特展%' or content like '%铜器展%' or content like '%昆虫展%' or content like '%特展%' or content like '%钱币展%' or content like '%特展%' or content like '%交流展%' or content like '%珍品展%' or content like '%特展%' or content like '%纸币展%' or content like '%藏品展%' or content like '%史实展%' or content like '%锁具展%' or content like '%线上展%'"""
    result = __conn.getAll(sql)
    for res in result:
        # print(start_run_(res[1]))
        sss = re.findall('render_data = (\[.*\])\[0\]', start_run_(res[1]), re.S | re.M)
        ddd = json.loads(sss[0])
        # print(ddd[0]["status"]["text"])
        title = set_title(ddd[0]["status"]["text"])
        organizer = source_re('主办单位', ddd[0]["status"]["text"])
        exhibition_address = source_re('展出地点', ddd[0]["status"]["text"])
        times = match_time('展出时间', ddd[0]["status"]["text"])
        if res[0] == '故宫博物院':
            museum_id = 147
        else:
            museum_id = 82
        if times:
            times_ = times.split('—')
            if len(times_) == 2:
                start_time = times.split('—')[0].replace('年', '-').replace('月', '-').replace('日', '-')[:-1]
                end_time = times.split('—')[1].replace('年', '-').replace('月', '-').replace('日', '-')[:-1]
            else:
                start_time = ''
                end_time = ''
        else:
            start_time = ''
            end_time = ''
        items = dict()
        items['museum_id'] = museum_id
        items['title'] = title
        items['url'] = res[1]
        items['cover_url'] = ';'.join([f'https://wx4.sinaimg.cn/orj360/{i}' for i in ddd[0]["status"]["pic_ids"]])
        items['price'] = ''
        items['start_time'] = start_time
        items['stop_time'] = end_time
        items['exhibition_address'] = exhibition_address if exhibition_address else ''
        items['Introduction'] = get_new_content(ddd[0]["status"]["text"])
        items['organizer'] = organizer if organizer else ''
        items['exhibition_type'] = 2
        items['create_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # print(items)
        insert(items)
        # break
