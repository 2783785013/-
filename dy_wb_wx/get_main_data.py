import time

import execjs, requests, json, jsonpath
from urllib.parse import urlencode
from loguru import logger
import traceback
from choice_ua import *
import random
# from tenacity import retry, stop_after_attempt
from settings import proxies_info_request

with open('get_XBogus.js', 'r', encoding='utf-8') as f:
    js_str = f.read()


def get_X_bogus(str_):
    ctx = execjs.compile(js_str)
    result = ctx.call('getXBogus', str_)
    # print(result)
    return result


# @retry(stop=stop_after_attempt(5))
def get_data_num(sec_uid):
    # print(1111)
    url = "https://www.douyin.com/aweme/v1/web/user/profile/other/"
    headers = {
        "cookie": "ttwid=1%7Cwt622iFRlnqWbEKx0saVIJTfmIxWb2mFFSdqTTb4U1w%7C1682305104%7C7ed578e0d339cc92740b69e1501a1a695742619db7e4ce7bfcd4793d394b64b1; strategyABtestKey=%221682305105.871%22; passport_csrf_token=9a7ec83d39abb224d659eb3eab6f4d94; passport_csrf_token_default=9a7ec83d39abb224d659eb3eab6f4d94; s_v_web_id=verify_lgu90w0t_sO58aq7p_vL3s_4ItL_BP2v_x0Iu4Ibsb2UV; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtY2xpZW50LWNzciI6Ii0tLS0tQkVHSU4gQ0VSVElGSUNBVEUgUkVRVUVTVC0tLS0tXHJcbk1JSUJEVENCdFFJQkFEQW5NUXN3Q1FZRFZRUUdFd0pEVGpFWU1CWUdBMVVFQXd3UFltUmZkR2xqYTJWMFgyZDFcclxuWVhKa01Ga3dFd1lIS29aSXpqMENBUVlJS29aSXpqMERBUWNEUWdBRWQyL1JuZnZXdGxHUFVGYXhmZUNlbC9BZFxyXG5ycUJHU0M4eVNYbjY3UXlQaTl3ejdYNGNNWjJadEhxaEtxMDgvelM1K2E0VjNkRHRuK21JT3NjN216VmZRS0FzXHJcbk1Db0dDU3FHU0liM0RRRUpEakVkTUJzd0dRWURWUjBSQkJJd0VJSU9kM2QzTG1SdmRYbHBiaTVqYjIwd0NnWUlcclxuS29aSXpqMEVBd0lEUndBd1JBSWdNMWhiblU5ZjB6VEJFUm1MWGJDaEpnN3d1eS9xbzFNbW5pK3VvZU4vS1R3Q1xyXG5JR2ZPNFBIbVU4NTJLMjl1RHBXbVVKN2FYMkNKWTJzdk4xcFZWU0VQY0lyRFxyXG4tLS0tLUVORCBDRVJUSUZJQ0FURSBSRVFVRVNULS0tLS1cclxuIn0=; ttcid=ffedb4ae400a4ab496362a619dab7c4390; tt_scid=b9Aa1VoegJsTCia3zDx9l-RICFDgL0aRbpd4mdPLUSDPFdP1LvM72VVUj.zazHw0d3cb; download_guide=%223%2F20230424%22; pwa2=%222%7C0%22; msToken=6RbZ6_9xOp7YECuaCp5ZuBH62Y9QTFXKd6kaFcxz-WwM-D0VHw5UZTWz_GAqkUGfxDRQ5bugYalpvVXA3Sd1WMWwuLw86qB7mylRrHfQcfRGYqqEYkcL; msToken=lKYy1_uSvyk7hD9cOVo5R4xbVv56wB-ZlDPeTe1ZKlvL4s8hnXhat7jOyWNIw18AYMqyIUAMEZRpLcUPCbrp1TTnu-w6TbcUoFlCnfmYDmIcSVyhk3_G; __ac_nonce=06445f94a00e622a4ab7; __ac_signature=_02B4Z6wo00f01jdK2HAAAIDCt0giMouBXYY3atzAAOmlnt01-2wCuWATZBXCAEFyYIGOFRHcO5FpL1k7MeI7Lu5XrMoZ5UEgqmxu6GZl2RNpmbyLJbB6z8eiuD6JM2rl21w5aq35Av4pnLKj61; home_can_add_dy_2_desktop=%220%22",
        "referer": "https://www.douyin.com/user/MS4wLjABAAAAvL6ZWvqSso-yX-Nxye-afhd4BZA57uWF-qdPwbc2OkU",
        "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
    }
    params = {
        "device_platform": "webapp",
        "aid": "6383",
        "channel": "channel_pc_web",
        "sec_user_id": sec_uid,
        "max_cursor": "0",
        "locate_query": "false",
        "show_live_replay_strategy": "1",
        "count": "10",
        "publish_video_strategy_type": "2",
        "pc_client_type": "1",
        "version_code": "170400",
        "version_name": "17.4.0",
        "cookie_enabled": "true",
        "screen_width": "1920",
        "screen_height": "1080",
        "browser_language": "zh-CN",
        "browser_platform": "Win32",
        "browser_name": "Chrome",
        "browser_version": "112.0.0.0",
        "browser_online": "true",
        "engine_name": "Blink",
        "engine_version": "112.0.0.0",
        "os_name": "Windows",
        "os_version": "10",
        "cpu_core_num": "4",
        "device_memory": "8",
        "platform": "PC",
        "downlink": "10",
        "effective_type": "4g",
        "round_trip_time": "50",
        "webid": "7225445335467525670",
        "msToken": "D6OIuk-Kt_5Zt0Z5X6Sk6yHQWPm_ermLVLeqPWNM9ZRUuMYPePUNX4GNAGCkcbL3pCZfivepvk7zV43vinR5R2Tkh0HTDA-amVGKM-mnUXj9vhfxS_nR",
        # "X-Bogus": "DFSzswVu5D0ANjeqtege0F9WX7nW"
    }
    # dict = random.choice(diffrent_ua)
    # headers = dict['headers']
    # params = dict['params']
    # str_1, str_2, str_3, str_4, str_5 = dict['str_list'],str_1, str_2, str_3, str_4, str_5
    # params['sec_user_id'] = sec_uid
    params['X-Bogus'] = get_X_bogus(urlencode(params))
    response = requests.get(url, headers=headers, params=params)
    response.encoding = response.apparent_encoding
    # print(8888888888888,response.status_code)
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
    # https://www.douyin.com/user/MS4wLjABAAAA5nuPKDI-mpTVaqdQhyNgRWXE5ie_rHi5MgNbcoCMKjY
    # sec_uid = "MS4wLjABAAAA5nuPKDI-mpTVaqdQhyNgRWXE5ie_rHi5MgNbcoCMKjY"
    # sec_uid = "MS4wLjABAAAAvL6ZWvqSso-yX-Nxye-afhd4BZA57uWF-qdPwbc2OkU"
    sec_uid = "MS4wLjABAAAAWWDKr-TwKhM6Cb02cd6PpkE0xZEl4Haua2dVZrLb1Vg"
    get_data_num(sec_uid)
