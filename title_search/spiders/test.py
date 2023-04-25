# from until.my_dowload import down_video
# import asyncio
# import time
# dv = down_video()
# # headers =
# # dv.set_headers(headers)
# start = time.time()
# urls1 = [f'https://cntv.vod.cdn.myqcloud.com/flash/mp4video63/TMS/2023/03/02/76212b2a256d42dd969a71a44149201d_h2642000000nero_aac16-{i}.mp4' for i in range(1, 3)]
# path1 = './'
# asyncio.get_event_loop().run_until_complete(dv.download_much(urls1, path1,down_type=2))
# print(time.time()-start)
from until.my_request import start_run_
from lxml import etree
from urllib.parse import urlencode
from spiders.title_baidu import get_element_str
import re
from gne import GeneralNewsExtractor
import json
from jsonpath import jsonpath
import requests

# url = 'https://mp.weixin.qq.com/s/q_WeN4ZewLOeW_R-hcMmBw'
header = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36"
}


# url = 'https://www.pgm.org.cn/pgm/zhmzfsysz/202209/3ce37d56fe5b47efb801d002095fdf39.shtml'
# respone1 = requests.get(url, headers=header).text


def get_pulish_place(respone):
    try:
        am = re.findall('window.ip_wording = {.*?provinceName:(.*?),.*?provinceId.*?cityId.*?}', respone, re.S | re.M)[
            0]
        pulish_place = am.strip()
    except:
        return ''
    else:
        return pulish_place
# 640a867cae35d709238222aeae

url = 'https://vdn.apps.cntv.cn/api/getHttpVideoInfo.do?pid=640a867cae35d709238222aeae'

response = requests.get(url, headers=header).json()
print(response)
print(jsonpath(response, '$..chapters4..url'))
# print(get_pulish_place(respone1))
# print(respone.encode('utf-8').decode('unicode_escape'))
# ex = GeneralNewsExtractor()
# print(ex.extract(respone))
# content = ''
# html = etree.HTML(respone)
# # strs = html.xpath('//div[@id="js_content"]/section/section/section/section/section[last()]')
# str1 = html.xpath('//div[@id="js_content"]/section/section/section/section//p//text()')
# for s in str1:
#     # if '。' in s:
#     content += s
# print(content)


# strs = get_element_str(strs[0])
# print(strs)


# def match_times(html1):
#     times = re.findall(
#
#     s_ = []
#     for s in times:
#         if s.strip():
#             source = re.sub(f'展期|时间|编辑|<.*?>|综合自|\s+|&nbsp;|：|:', '', s.strip(), 0, re.S | re.M)
#             if source not in s_ and len(source) < 30:
#                 s_.append(source)
#     if s_:
#         return s_[0]
#     else:
#         return False


# def match_place(html2):
#     return re.findall('地点.*?[\u4e00-\u9fa5]+.*?', html2, re.S | re.M)


# print(match_times(respone))
