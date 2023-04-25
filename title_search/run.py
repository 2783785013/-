from spiders.title_360 import mian_360
from spiders.title_baidu import mian_baidu
from spiders.title_sougou import mian_sougou
import asyncio
import time
import threading
from until.my_redis import Redis_util

redis_ = Redis_util(0, 10)


async def search_start(search_title):
    """
    :param search_title:
    :return:
    """
    result = await asyncio.gather(*[mian_sougou(search_title), mian_baidu(search_title), mian_360(search_title)])
    print(result)


def async_start():
    """
    协程启动
    :return:
    """
    while True:
        search_title = redis_.S_pop('sys_title_search')

        if search_title:
            with open('1.txt', 'a+', encoding='utf-8') as f:
                f.write(search_title)
            if search_title[0] == '"' and search_title[-1] == '"':
                search_title = search_title[1:-1]
            new_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(new_loop)
            loop = asyncio.get_event_loop()
            loop.run_until_complete(search_start(search_title))
        else:
            print('无数据,暂停半小时')
            time.sleep(60 * 30)


def run():
    """
    3条线程
    :return:
    """
    thread_list = []
    for i in range(2):
        thread_ = threading.Thread(target=async_start)
        thread_list.append(thread_)
    for t in thread_list:
        t.start()


if __name__ == '__main__':
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(search_start('内蒙古阿拉善左旗煤矿坍塌事故：4人死亡 尚有49人失联'))
    run()
    # print(redis_.S_len('sys_title_search'))
    # with open('1.txt', 'r', encoding='utf-8') as f:
    #     for i in f.read().split('""'):
    #         redis_.S_add('sys_title_search', i)
