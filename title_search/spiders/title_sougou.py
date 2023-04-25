# -*- coding: UTF-8 -*-
from until.my_request import start_run_
from lxml import etree
from until.time_utils import get_createTime
import re
from urllib.parse import quote
from settings import ua_list
import random
import asyncio
import datetime
from until.text_until import insert, select_mysql
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
    url = "https://www.sogou.com/sogou"
    params = {
        "query": title,
        "pid": "sogou-wsse-8f646834ef1adefa",
        "duppid": "1",
        "cid": "",
        "interation": "1728053249",
        "s_from": "result_up",
        "tsn": "1",
        "interV": "kKIOkrELjbkRmLkElbkTkKIMkrELjboImLkEk74TkKIRmLkEk78TkKILkY==_-115092183",
        "page": page,
        "ie": "utf8",
        "p": "40230447",
        "dp": "1"
    }
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "referer": f"https://www.sogou.com/sogou?query={quote(title)}&pid=sogou-wsse-8f646834ef1adefa&duppid=1&p=40230447&cid=&interation=1728053249&s_from=result_up&tsn=1&interV=kKIOkrELjbkRmLkElbkTkKIMkrELjboImLkEk74TkKIRmLkEk78TkKILkY%3D%3D_-115092183&sourceid=inttime_day",
        "sec-ch-ua": "\"Not_A Brand\";v=\"99\", \"Google Chrome\";v=\"109\", \"Chromium\";v=\"109\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": random.choice(ua_list)
    }
    response = start_run_(url, headers=headers, params=params, proxy=get_proxy()['https'])
    # print(8888888,response)
    return response, headers


def get_element_str(element):
    return etree.tostring(element, encoding="utf-8", pretty_print=True).decode("utf-8")


async def xpath_jiexi(div, headers):
    div_str = get_element_str(div)
    div_ele = etree.HTML(div_str)
    # print(div_str)
    title = div_ele.xpath('//h3[@class="vr-title"]/a|//h3[@class="vr-title  "]/a')
    if title:
        title = re.sub('<!--.*?-->|<script.*?</script>|<style>.*?</style>|<.*?>|&#13;|\n\s*?\n|\n|\n\s*?|\s*?', '',
                       get_element_str(title[0]), 0, re.M | re.S)
    else:
        return False
    time_ = ''.join(div_ele.xpath(
        '//p[@class="news-from text-lightgray"]/span[2]/text()|//div[@class="fz-mid space-txt"]/span[2]/text()'))
    if not time_.strip():
        time_ = ''.join(div_ele.xpath(
            '//div[@class="citeurl"]/span[@class="cite-date"]/text()|//div[@class="citeurl "]/span[@class="cite-date"]/text()'))
    meiti = ''.join(div_ele.xpath('//div[@class="fz-mid"]/p[@class="news-from text-lightgray"]/span[1]/text()'))
    if not meiti.strip():
        meiti = ''.join(div_ele.xpath(
            '//div[@class="citeurl"]/span[1]/text()|//div[@class="citeurl "]/span[1]/text()'))
    meiti = meiti.split('-')[0].strip()
    url = ''.join(div_ele.xpath('//h3[@class="vr-title"]/a/@href|//h3[@class="vr-title  "]/a/@href'))
    time_ = get_createTime(time_.replace('&nbsp;', '').replace('-', '', 1).strip())
    url = re.findall('replace\("(.*?)"\)', str(start_run_('https://www.sogou.com' + url, headers=headers, proxy=get_proxy()['https'], num=3)), re.S | re.M)
    if url:
        # print(url)
        url = url[0]
        if select_mysql(url):
            return False
        source_ = source_re(str(start_run_(url)))
        if not source_:
            source_ = ''
        return title, time_, meiti, url, source_
    else:
        return False


async def jiexi(html_str, headers):
    html_ele = etree.HTML(html_str)
    html_divs = html_ele.xpath('//div[@class="results"]/div[@class="vrwrap"]')
    if html_divs:
        return await asyncio.wait([xpath_jiexi(div, headers) for div in html_divs])
    else:
        return False
    # for div in html_divs:
    #     div_str = get_element_str(div)
    #     div_ele = etree.HTML(div_str)
    #     # print(div_str)
    #     title = div_ele.xpath('//h3[@class="vr-title"]/a|//h3[@class="vr-title  "]/a')[0]
    #     title = re.sub('<!--.*?-->|<script.*?</script>|<style>.*?</style>|<.*?>|&#13;|\n\s*?\n|\n|\n\s*?|\s*?', '',
    #                    get_element_str(title), 0, re.M | re.S)
    #     time_ = ''.join(div_ele.xpath('//p[@class="news-from text-lightgray"]/span[2]/text()|//div[@class="fz-mid space-txt"]/span[2]/text()'))
    #     if not time_.strip():
    #         time_ = ''.join(div_ele.xpath('//div[@class="citeurl"]/span[@class="cite-date"]/text()|//div[@class="citeurl "]/span[@class="cite-date"]/text()'))
    #     meiti = ''.join(div_ele.xpath('//div[@class="fz-mid"]/p[@class="news-from text-lightgray"]/span[1]/text()'))
    #     if not meiti.strip():
    #         meiti = ''.join(div_ele.xpath(
    #             '//div[@class="citeurl"]/span[1]/text()|//div[@class="citeurl "]/span[1]/text()'))
    #     meiti = meiti.split('-')[0].strip()
    #     url = ''.join(div_ele.xpath('//h3[@class="vr-title"]/a/@href|//h3[@class="vr-title  "]/a/@href'))
    #     time_ = get_createTime(time_.replace('&nbsp;', '').replace('-', '', 1).strip())
    #     url = re.findall('replace\("(.*?)"\)', start_run('https://www.sogou.com/'+url, headers=headers), re.S | re.M)
    #     if url:
    #         # print(url)
    #         url = url[0]
    #         data_list.append([title, time_, meiti, url])
    # return True, data_list


async def mian_sougou(search_title):
    for i in range(1, 11):
        response, headers = get_response(search_title, i)
        if response:
            result = asyncio.run(jiexi(response, headers))
            if result:
                result1, result2 = result
                for res in result1:
                    if res.result():
                        title, time_, meiti, url, source = res.result()
                        re_insert(title, time_, meiti, url, source,  search_title)


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
    item["search_mediun"] = '搜狗搜索'
    item["source_medium"] = source
    insert(item)


if __name__ == '__main__':
    mian_sougou('土耳其地震')