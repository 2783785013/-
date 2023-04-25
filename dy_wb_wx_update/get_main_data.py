import time

import execjs, requests, json, jsonpath
from urllib.parse import urlencode
from loguru import logger
import traceback
from choice_ua import *
import random
from tenacity import retry, stop_after_attempt
from settings import proxies_info_request

with open('get_XBogus.js', 'r', encoding='utf-8') as f:
    js_str = f.read()

def get_X_bogus(str_, str_1, str_2, str_3, str_4, str_5):
    ctx = execjs.compile(js_str)
    result = ctx.call('getXBogus',str_, str_1, str_2, str_3, str_4, str_5)
    # print(result)
    return result


# @retry(stop=stop_after_attempt(2))
def get_data_num(sec_uid):
    url = "https://www.douyin.com/aweme/v1/web/user/profile/other/"
    dict = random.choice(diffrent_ua)
    headers = dict['headers']
    params = dict['params']
    str_1, str_2, str_3, str_4, str_5 = dict['str_list']
    params['sec_user_id'] = sec_uid
    if params.get('X-Bogus'):
        del params['X-Bogus']
    params['X-Bogus'] = get_X_bogus(urlencode(params),str_1, str_2, str_3, str_4, str_5)

    response = requests.get(url, headers=headers, params=params)
    response.encoding = response.apparent_encoding
    # print(response.text)
    if response.status_code == 200:
        data = json.loads(response.text)
        # print(111111,data)

        all_likes_num = jsonpath.jsonpath(data, '$..total_favorited')
        fans = jsonpath.jsonpath(data, '$..mplatform_followers_count')
        publish_num = jsonpath.jsonpath(data, '$..aweme_count')
        if all_likes_num and fans and publish_num:
            return all_likes_num[0], fans[0], publish_num[0]
    else:
        traceback.print_exc()
        logger.info(f'请求失败 --> {sec_uid}')





if __name__ == '__main__':
    # print(execjs.get().name)
    #https://www.douyin.com/user/MS4wLjABAAAA5nuPKDI-mpTVaqdQhyNgRWXE5ie_rHi5MgNbcoCMKjY
    # sec_uid = "MS4wLjABAAAA5nuPKDI-mpTVaqdQhyNgRWXE5ie_rHi5MgNbcoCMKjY"
    # sec_uid = "MS4wLjABAAAAvL6ZWvqSso-yX-Nxye-afhd4BZA57uWF-qdPwbc2OkU"
    for i in range(2):
        sec_uid = "MS4wLjABAAAAWWDKr-TwKhM6Cb02cd6PpkE0xZEl4Haua2dVZrLb1Vg"
        get_data_num(sec_uid)


