# -*- coding: UTF-8 -*-
from until.my_request import start_run_
from lxml import etree
from until.time_utils import get_createTime
import re
from until.text_until import insert, select_mysql
import datetime
import asyncio
from settings import proxies_info_request
import nest_asyncio
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
    url = "https://news.so.com/ns"
    params = {
        "q": title,
        "pn": page,
        "rank": "pdate",
        "j": "0",
        "nso": "20",
        "tp": "13",
        "nc": "0",
        "src": "page"
    }
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "referer": "https://news.so.com/ns?q=%E5%9C%9F%E8%80%B3%E5%85%B67.8%E7%BA%A7%E5%9C%B0%E9%9C%87&pn=4&rank=pdate&j=0&nso=20&tp=13&nc=0&src=page",
        "sec-ch-ua": "\"Not_A Brand\";v=\"99\", \"Google Chrome\";v=\"109\", \"Chromium\";v=\"109\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
    }
    response = start_run_(url, headers=headers, params=params, proxy=get_proxy()['https'])
    return response


def get_element_str(element):
    return etree.tostring(element, encoding="utf-8", pretty_print=True).decode("utf-8")


async def xpath_jiexi(div):
    div_str = get_element_str(div)
    div_ele = etree.HTML(div_str)
    try:
        title = div_ele.xpath('//h3[@class="js-title"]|//div[@class="r-c-tit js-title"]/span')[0]
        title = re.sub('<!--.*?-->|<script.*?</script>|<style>.*?</style>|<.*?>|&#13;|\n\s*?\n|\n|\n\s*?|\s*?', '',
                       get_element_str(title), 0, re.M | re.S)
        time_ = ''.join(
            div_ele.xpath('//div[@class="info r-c-info"]/span[2]/text()|//div[@class="info b-info"]/span[2]/text()'))
        meiti = ''.join(
            div_ele.xpath('//div[@class="info r-c-info"]/span[1]/text()|//div[@class="info b-info"]/span[1]/text()'))
        url = ''.join(div_ele.xpath('//li/a/@href'))
        if 'http' not in url:
            # print(html_str)
            title = div_ele.xpath('//h3[@class="js-title"]/a|//div[@class="r-c-tit js-title"]/a')[0]
            title = re.sub('<!--.*?-->|<script.*?</script>|<style>.*?</style>|<.*?>|&#13;|\n\s*?\n|\n|\n\s*?|\s*?', '',
                           get_element_str(title), 0, re.M | re.S)
            time_ = ''.join(div_ele.xpath(
                '//div[@class="info r-c-info"]/span[3]/text()|//div[@class="info b-info"]/span[3]/text()'))
            meiti = ''.join(div_ele.xpath(
                '//div[@class="info r-c-info"]/span[1]/text()|//div[@class="info b-info"]/span[1]/text()'))
            url = ''.join(div_ele.xpath('//li/h3/a/@href'))
        if '年' in time_ or '月' in time_:
            return False, True, '', '', ''
        time_ = get_createTime(time_)
        if url:
            if select_mysql(url):
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
    html_divs = html_ele.xpath('//div[@id="main"]/div/ul/li')
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
    item["search_mediun"] = '360搜索'
    item["source_medium"] = source
    insert(item)


async def mian_360(search_title):
    for i in range(1, 12):
        response = get_response(search_title, i)
        if response:
            result = asyncio.run(jiexi(response))
            if result:
                result1, result2 = result
                for res in result1:
                    title, time_, meiti, url, source = res.result()
                    if title and time_ and meiti and url:
                        re_insert(title, time_, meiti, url, source, search_title)
                    else:
                        continue


if __name__ == '__main__':
    mian_360('土耳其地震')
    # print(jiexi(get_response('土耳其7.8级地震', 1)))