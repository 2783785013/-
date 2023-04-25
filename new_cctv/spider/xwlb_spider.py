import requests
from settings import headers
from lxml import etree
import json
from loguru import logger
from datetime import datetime
import time


def get_max_data(url, num=0):
    """
    判断当天新闻联播是否更新
    :param url:
    :param num:
    :return:
    """
    try:
        reposne = requests.get(url=url, headers=headers)
        html = etree.HTML(reposne.text)
        result = html.xpath('//div[@class="rilititle"]/p/text()')
        # print(result)
        max_data = result[0].replace('年', '-').replace('月', '-').replace('日', '')
    except Exception as e:
        num += 1
        if num < 4:
            get_max_data(url, num)
        else:
            logger.info(f'请求失败{e}')
            return False
    else:
        if max_data.strip() == datetime.now().strftime('%Y-%m-%d'):
            return True
        else:
            return False


def get_xwlb_list(url, columns, num=0):
    """
    获取列表页的id
    :param url:
    :param columns:
    :param num:
    :return:
    """
    urls = []
    try:
        reposne = requests.get(url=url, headers=headers)
        html = etree.HTML(reposne.text)
        urls_element = html.xpath('//li/a')
        for url_ele in urls_element:
            url_div = etree.tostring(url_ele, encoding="utf-8", pretty_print=True).decode("utf-8")
            if f'《{columns}》' not in url_div and datetime.now().strftime('%Y%m%d') not in url_div:
                urls.append(etree.HTML(url_div).xpath('//a/@href')[0])
            # else:
            #     return '今日更新完毕'
    except Exception as e:
        num += 1
        if num < 4:
            get_max_data(url, num)
        else:
            logger.info(f'请求失败{e}')
            return False
    else:
        if urls:
            return [i.split('/')[-1].replace('.shtml', '') for i in urls]
        else:
            return False


def get_video_info_(videoid, num=0):
    """
    获取新闻联播视频的详细
    :param videoid:
    :param num:
    :return:
    """
    url = "https://api.cntv.cn/Article/newContentInfo"
    params = {
        "serviceId": "tvcctv",
        "id": videoid,
        "cb": f"abcde{videoid}"
    }
    try:
        reposne = requests.get(url=url, headers=headers, params=params)
        video_data = reposne.text.replace(f'{params["cb"]}', '')[1:-2]
        video_info = json.loads(video_data)
    except Exception as e:
        num += 1
        if num < 4:
            get_max_data(url, num)
        else:
            logger.info(f'请求失败{e}')
            return False
    else:
        if video_info:
            return video_info["data"]
        else:
            return False


def get_likenum(videoid, num=0):
    """
    提取点赞数
    :param videoid:
    :param num:
    :return:
    """
    url = "https://common.itv.cntv.cn/praise/get"
    params = {
        "type": "other",
        "id": videoid,
        "r": int(time.time() * 1000),
        "jsonp_callback": "hqdianzan"
    }
    try:
        reposne = requests.get(url=url, headers=headers, params=params)
        likenum_data = reposne.text.replace(f'{params["jsonp_callback"]}', '')[1:-2]
        video_info = json.loads(likenum_data)
    except Exception as e:
        num += 1
        if num < 4:
            get_max_data(url, num)
        else:
            logger.info(f'请求失败{e}')
            return False
    else:
        if video_info:
            return video_info["data"]["num"]
        else:
            return False


if __name__ == '__main__':
    print(get_video_info_('VIDEmRUMIRre9BaGJd1K13cX230320'))
