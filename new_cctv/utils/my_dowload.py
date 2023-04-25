# -*- coding: UTF-8 -*-
import asyncio
import aiohttp
from tqdm import tqdm
import os
import time
from loguru import logger
from utils.text_until import MD5_


class down_video(object):
    def __init__(self):
        # 请求头
        self.__headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
        }

    def set_headers(self, new_headers):
        # 设置请求头
        self.__headers = new_headers

    async def __get_content_length(self, session, path, video_url):
        async with session.get(video_url, headers=self.__headers) as response:
            try:
                le = response.headers.get('Content-Length') or response.headers.get('content-length') or 0
                if le and le.isdigit():
                    content_length = int(le)
                    f = open(path, 'wb')
                    f.truncate(content_length)
                    f.close()
                    return content_length
                else:
                    return False
            except:
                logger.info('下载失败')
                return False

    @staticmethod
    async def __down_video(queue, file_path):
        """
        :param queue: 队列
        :return:
        """
        try:
            file_path = file_path
            while not queue.empty():
                task = await queue.get()
                session, file_path, video_url, start, headers = task[0], task[1], task[2], task[3], task[4]
                async with session.get(video_url, headers=headers) as resp:
                    with open(file_path, 'rb+') as f:
                        # 写入位置，指针移到指定位置
                        f.seek(start)
                        async for b in resp.content.iter_chunked(1024 * 1024):
                            f.write(b)
        except:
            logger.info('片段下载失败')
            os.remove(file_path)
            return False, ''
        else:
            return True, file_path

    async def __start_async(self, video_url, file_path, count=16):
        """
        :param video_url:视频地址
        :param file_path: 视频保存位置
        :param count:协程数量
        """
        path_, name = os.path.split(file_path)
        # 判断目录是否存在
        if not os.path.exists(path_):
            os.makedirs(path_)
        async with aiohttp.ClientSession() as session:
            # 文件长度
            content_length = await self.__get_content_length(session, file_path, video_url=video_url)
            if content_length:
                # 将文件按大小分解为任务队列
                queue = asyncio.Queue()
                # [quque.put_nowait()]
                # 每个区块1M大小
                size = 1024 * 10240
                amount = content_length // size or 1
                for i in range(amount):
                    start = i * size
                    if i == amount - 1:
                        end = content_length
                    else:
                        end = start + size
                    if start > 0:
                        start += 1
                    # 设置请求视频位置
                    headers = {
                        'Range': f'bytes={start}-{end}'
                    }
                    # 合并请求头
                    headers.update(self.__headers)
                    queue.put_nowait([session, file_path, video_url, start, headers])

                # with tqdm(total=content_length, unit='', desc=f'下载：{name}', unit_divisor=1024, ascii=True, unit_scale=True) as bar:
                    # 开始协程
                return await asyncio.wait([self.__down_video(queue, file_path) for i in range(count)])
            else:
                return False

    async def main(self, url, file_path, count=32):
        """
        :param url: 视频地址
        :param file_path: 保存地址
        :param count: 协程数量
        """
        result = await self.__start_async(url, file_path, count)
        n = file_path
        if result:
            num = 0
            result1, result2 = result
            for res in result1:
                m, n = res.result()
                if m:
                    num += 1
            if num == count:
                return True, n
            else:
                return False, ''
        else:
            return False, ''

    async def download_much(self, url, path, down_type=1, count=2, name=''):
        if name == '':
            name = MD5_(url)
        dw_list = []
        if type(url) == list:
            urls = url
        else:
            urls = [url]
        if down_type == 1:
            suffix = '.jpg'
        else:
            suffix = '.mp4'
        results = await asyncio.gather(*[self.main(url, path+name+suffix, count)for url in urls])
        for result in results:
            if result[0]:
                dw_list.append(result[1])
        if len(dw_list) == 1:
            return dw_list[0]
        elif len(dw_list) > 1:
            return dw_list
        else:
            return False


if __name__ == '__main__':
    start_time = time.time()
    video_url1 = 'http://www.sse.com.cn/disclosure/listedinfo/announcement/c/new/2023-02-15/603059_20230215_XAIB.pdf'
    urls1 = [
        'https://pics6.baidu.com/feed/b17eca8065380cd72f80575d9cc1033f58828171.jpeg@f_auto?token=04481019780b13eb88989edd0faeefe8',
        'https://pics3.baidu.com/feed/e61190ef76c6a7ef3db2861a04872a56f2de66ff.jpeg@f_auto?token=5da7e8893b8c3d065695a5adb6466df1',
        'https://pics4.baidu.com/feed/4e4a20a4462309f721e68d9c837389f4d6cad63c.jpeg@f_auto?token=e6aee1c39fad59addaf7eecf827abb34'
    ]
    path1 = './test/'

    dv = down_video()
    asyncio.get_event_loop().run_until_complete(dv.download_much(urls1, path1, down_type=3))
    print(time.time() - start_time)
