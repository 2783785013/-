import requests
from datetime import datetime
from settings import headers
import json
from loguru import logger
import math
import time
from jsonpath import jsonpath


def get_data_list(topid, page=1, data_list='', num=0, bd=''):
    if data_list == '':
        data_list = []
    if bd == '':
        bd = datetime.now().strftime("%Y%m%d")
    url = "https://api.cntv.cn/NewVideo/getVideoListByColumn"
    params = {
        "id": topid,
        "n": "100",
        "sort": "desc",
        "p": page,
        "bd": bd,
        "mode": "2",
        "serviceId": "tvcctv",
        "cb": "cb"
    }
    try:
        headers["referer"] = 'https://tv.cctv.com/'
        reposne = requests.get(url, headers=headers, params=params)
        reposne = reposne.text
        video_data = reposne.encode('utf-8').decode('unicode_escape')[len(params['cb']) + 1:-2]
        video_info = json.loads(video_data, strict=False)
    except Exception as e:
        print(e)
        time.sleep(10)
        num += 0
        if num < 4:
            get_data_list(topid, page, data_list, num)
        else:
            logger.info(f'失败{e}')
            return False
    else:
        total = video_info["data"]["total"]
        new_page = math.ceil(total / 100)
        if new_page != 1:
            page += 1
            data_list += video_info['data']['list']
            if new_page >= page:
                # print(page)
                return get_data_list(topid, page, data_list=data_list)
            else:
                return data_list
        else:
            return video_info['data']['list']


def get_data_list_(topid, num=0):
    url = "https://api.cntv.cn/newLanmu/getVideoListByTopicIdInfo"
    params = {
        "id": topid,
        "serviceId": "tvcctv",
        "t": "jsonp",
        "fd": int(time.time() * 1000),
        "callback": "td3",
        "mode": "1"
    }
    try:
        response = requests.get(url, headers=headers, params=params)
        video_info = json.loads(response.text[4:-2])
    except Exception as e:
        print(e)
        time.sleep(10)
        num += 0
        if num < 4:
            get_data_list(topid, num)
        else:
            logger.info(f'失败{e}')
            return False
    else:
        return video_info['data']['list']


def get_video_urls(guid):
    url = "https://vdn.apps.cntv.cn/api/getHttpVideoInfo.do"
    params = {
        "pid": guid,
        'tsp': int(time.time()),
        # 'uid': 'E1A06985B3703036A73D4770BA285C95'
    }
    response = requests.get(url, headers=headers, params=params).json()
    urls = jsonpath(response, '$..chapters4..url')
    if urls:
        return urls
    else:
        return []


if __name__ == '__main__':
    print(get_data_list_('TOPC1451558976694518'))
    # print(get_video_urls('7d130bc06fac4a26be6d88cccb0303ee'))
