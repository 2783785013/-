# -*- coding: UTF-8 -*-
# -*- coding: UTF-8 -*-
import pyhttpx
import asyncio
import traceback
from loguru import logger
import httpx
from settings import proxies_info_request
import re
from urllib.parse import urlencode


def get_proxy():
    proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
        "host": proxies_info_request['proxyHost'],
        "port": proxies_info_request['proxyPort'],
        "user": proxies_info_request['proxyUser'],
        "pass": proxies_info_request['proxyPass'],
    }
    return proxyMeta


async def request_on(session, method, seam, url, response_type, headers, params, data, cookies, max_num=5, *args, **kwargs):
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
    :param cookies:
    :param max_num: 最大重试次数
    :param args:
    :param kwargs:
    :return: 响应
    """
    for try_num in range(max_num):
        try:
            async with seam:
                response = await session.request(method, url, headers=headers, params=params, data=data, cookies=cookies, timeout=10)
                if response_type == 'str':
                    result = response.text
                else:
                    result = response.json()
        except Exception as e:
            if try_num == max_num - 1:
                # traceback.print_exc()
                url = url + "?" + urlencode(params) if params else url
                logger.info(f'请求失败了：{url}{e}')
                return False
            else:
                continue
        else:
            if response.status_code == 200:
                return result
            else:
                if try_num == max_num - 1:
                    return False
                else:
                    continue


async def start(urls: list, num, method, response_type, headers, params, data, cookies, *args, **kwargs):
    """
    创建task
    :param urls:
    :param num:
    :param method:
    :param response_type:
    :param headers:
    :param params:
    :param data:
    :param cookies:
    :param args:
    :param kwargs:
    :return:
    """
    seam = asyncio.Semaphore(num)
    # session = httpx.Client(proxies=get_proxy()['https'])
    async with httpx.AsyncClient(proxies=get_proxy(), http2=True) as session:
        tasks = [asyncio.create_task(
            request_on(session, method, seam, url, response_type, headers, params, data, cookies, *args, **kwargs)) for
                 url in urls]
        return await asyncio.wait(tasks)


def start_run(urls: list or str, num=5, method='get', response_type='str', headers=None, params=None, data=None,
              cookies=None, *args, **kwargs):
    """
    启动
    :param urls: 请求urls:list
    :param num: 最大并发数 默认10
    :param method: 请求方式 默认get
    :param response_type: 响应数据类型 默认str, 否则json
    :param headers: 请求头
    :param params:
    :param data:
    :param cookies:
    :param args:
    :param kwargs:
    :return:
    """
    if headers is None:
        headers = dict()
        headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
    if type(urls) == list:
        done, set_ = asyncio.get_event_loop().run_until_complete(
            start(urls, num, method, response_type, headers, params, data, cookies, *args, **kwargs))
        response_list = [d.result() for d in done]
        return response_list
    else:
        done, set_ = asyncio.get_event_loop().run_until_complete(
            start([urls], num, method, response_type, headers, params, data, cookies, *args, **kwargs))
        for d in done:
            return d.result()


if __name__ == '__main__':
    url_1 = 'http://www.szse.cn/api/disc/announcement/detailinfo?random=0.2886918127457223&pageSize=50&pageNum=1&plateCode=szse'
    response1 = start_run(url_1, response_type='json')
    print(response1)