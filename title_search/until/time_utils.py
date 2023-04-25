# -*- coding: UTF-8 -*-
# @author: ylw
# @file: time_utils
# @time: 2021-9-6
# @desc:
import re
import time
import datetime


def match_timeStr(timeStr):
    """
    22分钟前   2小时前   2天前
    :param timeStr:
    :return:
    """


def getTimeBeforeMin(minute, format_):
    t = time.localtime(time.time() - minute * 60)
    return time.strftime(format_, t)


def get_createTime(createTime):
    if "分钟前" in createTime:
        createTime = createTime[0:createTime.__len__() - 3]
        createTime = getTimeBeforeMin(int(createTime), "%Y-%m-%d %H:%M:%S")
    elif "小时前" in createTime:
        createTime = createTime[0:createTime.__len__() - 3]
        createTime = getTimeBeforeMin(int(createTime) * 60, "%Y-%m-%d %H:%M:%S")
    elif '今天' in createTime:
        createTime = createTime[2:createTime.__len__()]
        if createTime == '':
            createTime = getTimeBeforeMin(0, "%Y-%m-%d") + ' ' + "00:00:01"
        else:
            createTime = getTimeBeforeMin(0, "%Y-%m-%d") + ' ' + createTime + ":00"
    elif "昨天" in createTime:
        createTime = createTime[2:createTime.__len__()]
        if createTime == '':
            createTime = getTimeBeforeMin(24 * 60, "%Y-%m-%d") + ' ' + "00:00:01"
        else:
            createTime = getTimeBeforeMin(24 * 60, "%Y-%m-%d") + ' ' + createTime + ":00"
    elif "刚刚" in createTime:
        createTime = getTimeBeforeMin(0, "%Y-%m-%d %H:%M:%S")
    elif "前天" in createTime:
        createTime = createTime[2:createTime.__len__()]
        if createTime == '':
            createTime = getTimeBeforeMin(2*24 * 60, "%Y-%m-%d") + ' ' + "00:00:01"
        else:
            createTime = getTimeBeforeMin(2*24 * 60, "%Y-%m-%d") + ' ' + createTime + ":00"
    elif '天前' in createTime:
        createTime = createTime[:-2]
        createTime = getTimeBeforeMin(int(createTime) * 24 * 60, "%Y-%m-%d %H:%M:%S")
    elif re.findall('\d{4}年\d{1,2}月\d{1,2}日', createTime):
        createTime = createTime.replace('年', '-').replace('月', '-').replace('日', '')

    return createTime


def get_now_time(mode='%Y-%m-%d %H:%M:%S'):
    return datetime.datetime.now().strftime(mode)


def get_file_time():
    return datetime.datetime.now().strftime('%Y_%m_%d')


def get_now_timestamp():
    return int(time.time())


def time_sub(t1, t2):
    """
    做时间减法
    :return: 差值 单位 S
    """
    d1 = datetime.datetime.strptime(t1, '%Y-%m-%d %H:%M:%S')
    d2 = datetime.datetime.strptime(t2, '%Y-%m-%d %H:%M:%S')
    delta = d1 - d2
    return delta.total_seconds()


def time_achine(now_time: str, **kwargs):
    """
    时光机，当前使时间向前，向后
    :param now_time: 现在时间：2021-11-22 10:13:00
    :param kwargs: 字典类型 参数看 datetime.timedelta 方法的参数
    :return:
    """
    now_time = datetime.datetime.strptime(now_time, "%Y-%m-%d %H:%M:%S")
    return (now_time + datetime.timedelta(**kwargs)).strftime("%Y-%m-%d %H:%M:%S")


def timeStamp_to_time(timeStamp: int):
    """
    时间戳转换为时间
    """
    if not timeStamp:
        return get_now_time(mode='%Y-%m-%d %H:%M:%S')

    if len(str(timeStamp)) >= 10:
        timeStamp = int(str(timeStamp)[:10])
    dateArray = datetime.datetime.fromtimestamp(timeStamp)
    return dateArray.strftime("%Y-%m-%d %H:%M:%S")


def time_to_timeStamp(time_: str):
    """
    时间转换为时间戳
    """
    try:
        timeArray = time.strptime(time_, "%Y-%m-%d %H:%M:%S")
    except Exception as e:
        timeArray = time.strptime(time_, "%Y-%m-%d %H:%M")
    return int(time.mktime(timeArray))


def change_time_type(s_time, module='%a %b %d %H:%M:%S %z %Y'):
    """
    :param s_time: 'Wed Jan 27 17:36:01 +0800 2021'
    :param module: 格式
    :return: 2021-01-27 17:36:01
    """
    std_create_time = datetime.datetime.strptime(s_time, module)
    return str(std_create_time).split('+', 1)[0]


def get_daytime():
    return datetime.datetime.now().strftime('%Y-%m-%d')


if __name__ == '__main__':
    az = '今天'
    print(get_createTime(az))
    # print(timeStamp_to_time(int(1656287640000)))
    print(time_to_timeStamp('2022-4-23'))
