# -*- coding: UTF-8 -*-
from until.new_request import start_run
from lxml import etree
from until.time_utils import get_createTime
import re
from until.my_request import start_run_
from loguru import logger
from until.text_until import insert, select_mysql
import datetime
import asyncio
import nest_asyncio
from settings import proxies_info_request, ua_list, baidu_cookie
import random
nest_asyncio.apply()


def get_proxy():
    proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
        "host": proxies_info_request['proxyHost'],
        "port": proxies_info_request['proxyPort'],
        "user": proxies_info_request['proxyUser'],
        "pass": proxies_info_request['proxyPass'],
    }
    return {"http": proxyMeta, "https": proxyMeta}


def get_response(title, page):
    url = "https://www.baidu.com/s"
    params = {
        "tn": "news",
        "rtt": "4",
        "bsst": "1",
        "cl": "2",
        "wd": title,
        "medium": "0",
        "x_bfe_rqs": "03E80",
        "x_bfe_tjscore": "0.100000",
        "tngroupname": "organic_news",
        "newVideo": "12",
        "goods_entry_switch": "1",
        "rsv_dl": "news_b_pn",
        "pn": 10 * page
    }
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Host": "www.baidu.com",
        "Pragma": "no-cache",
        # 'Cookie': random.choice(baidu_cookie),
        "Referer": "https://www.baidu.com",
        "sec-ch-ua": "\"Not_A Brand\";v=\"99\", \"Google Chrome\";v=\"109\", \"Chromium\";v=\"109\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": random.choice(ua_list)
    }
    response = start_run(url, headers=headers, params=params)
    # print(888888,response)
    return response


def get_element_str(element):
    return etree.tostring(element, encoding="utf-8", pretty_print=True).decode("utf-8")


async def xpath_jiexi(div):
    try:
        div_str = get_element_str(div)
        div_ele = etree.HTML(div_str)
        title = div_ele.xpath('//h3[@class="news-title_1YtI1 "]/a')[0]
        title = re.sub('<!--.*?-->|<script.*?</script>|<style>.*?</style>|<.*?>|&#13;|\n\s*?\n|\n|\n\s*?|\s*?', '',
                       get_element_str(title), 0, re.M | re.S)
        time_ = ''.join(div_ele.xpath(
            '//div[@class="c-span3"]/span[1]/text()|//div[@class="c-span-last c-span12"]/span[1]/text()|//div[@class="c-span-last c-span9 content_BL3zl"]/span[1]/text()'))
        meiti = ''.join(div_ele.xpath('//div[@class="news-source_Xj4Dv"]/a/span/text()'))
        url = ''.join(div_ele.xpath('//h3[@class="news-title_1YtI1 "]/a/@href'))
        if '年' in time_ or '月' in time_:
            if len(time_) < 13:
                return False, True, '', '', ''
            else:
                return False, False, '', '', ''
        time_ = get_createTime(time_)
        if url:
            if select_mysql(url):
                # print(title, time_, meiti, url)
                return False, False, '', '', ''
            source_ = source_re(str(start_run_(url)))
            if not source_:
                source_ = ''
        else:
            return False, False, '', '', ''
    except:
        return False, False, '', '', ''
    else:
        return title, time_, meiti, url, source_


async def jiexi(html_str):
    html_ele = etree.HTML(html_str)
    html_divs = html_ele.xpath(
        '//div[@class=" result-op c-container xpath-log new-pmd "]|//div[@class="result-op c-container xpath-log new-pmd"]')
    if html_divs:
        return await asyncio.wait([xpath_jiexi(div) for div in html_divs])
    else:
        return False


def source_re(text):
    source = re.findall('来源：.*?[\u4e00-\u9fa5]+.*?|来源:.*?[\u4e00-\u9fa5]+.*?', text, re.S | re.M)
    # print(source)
    if ''.join(source).strip():
        s_ = []
        for s in source:
            if s.strip():
                source = re.sub('来源：|来源:|编辑|<.*?>|综合自|\s+|&nbsp;', '', s.strip(), 0, re.S | re.M)
                if source not in s_ and len(source) < 13:
                    s_.append(source)
        if s_:
            return s_[0]
        else:
            return False
    else:
        return False


def re_insert(title, time_, meiti, url, source, search_title):
    item = dict()
    item["search_title"] = search_title
    item["title"] = title
    item["title_time"] = time_
    item["medium"] = meiti
    item["title_url"] = url
    item["create_time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    item["search_mediun"] = '百度'
    item["source_medium"] = source
    insert(item)


async def mian_baidu(search_title):
    i = 0
    m = True
    while m:
        response = get_response(search_title, i)
        if response:
            if '百度安全验证' not in response:
                result = asyncio.run(jiexi(response))
                if result:
                    result1, result2 = result
                    for res in result1:
                        title, time_, meiti, url, source = res.result()
                        if title and time_ and meiti and url:
                            re_insert(title, time_, meiti, url, source, search_title)
                        elif time_:
                            m = False
                        else:
                            continue
                    if i == 20:
                        break
                    i += 1
                    continue
                else:
                    if i == 20:
                        break
                    i += 1
                    logger.info(f'请求失败{search_title}')
                    continue
            else:
                if i == 20:
                    break
                i += 1
                logger.info(f'请求失败{search_title}')
                mian_baidu1(search_title)
                break
        else:
            if i == 20:
                break
            i += 1
            logger.info(f'请求失败{search_title}')
            continue


def mian_baidu1(search_title):
    i = 0
    m = True
    while m:
        print(i, 'jfdsjg')
        response = get_response(search_title, i)
        if response:
            if '百度安全验证' not in response:
                result = asyncio.run(jiexi(response))
                if result:
                    result1, result2 = result
                    for res in result1:
                        title, time_, meiti, url, source = res.result()
                        # print(title)
                        if title and time_ and meiti and url:
                            re_insert(title, time_, meiti, url, source, search_title)
                        elif time_:
                            m = False
                        else:
                            continue
                    if i == 20:
                        break
                    i += 1
                    continue
                else:
                    if i == 20:
                        break
                    i += 1
                    logger.info('请求失败')
                    continue
            else:
                if i == 20:
                    break
                i += 1
                logger.info('请求失败')
                break
        else:
            if i == 20:
                break
            i += 1
            logger.info('请求失败')
            continue


if __name__ == '__main__':
    mian_baidu1('习近平复信希腊学者')
