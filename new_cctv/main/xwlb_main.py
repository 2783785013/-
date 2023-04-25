from spider.xwlb_spider import *
from utils.my_redis import Redis_util
from utils.text_until import MD5_, insert, timeStamp_to_time, __conn
redis_ = Redis_util(18, 10)


def mian(url, columns, item, stop_time):
    if get_max_data(url=url):
        while True:
            if int(str(datetime.now())[11:13]) > stop_time-1:
                logger.info(f'{datetime.now().strftime("%Y%m%d")}{columns}抓取完成')
                return True
            id_list = get_xwlb_list(f'http://tv.cctv.com/lm/xwlb/day/{datetime.now().strftime("%Y%m%d")}.shtml',
                                    columns)
            if id_list:
                # if id_list == '今日更新完毕':
                #     logger.info(f'{datetime.now().strftime("%Y%m%d")}{columns}抓取完成')
                #     return True
                last_ = False
                for id_ in id_list:
                    if not redis_.S_isMember(f'cctv_video_id:{datetime.now().strftime("%Y%m%d")}', id_):
                        video_data = get_video_info_(id_)
                        item_data = get_video_item(item, video_data)
                        if item_data:
                            likenum = get_likenum(id_)
                            if likenum:
                                item_data["likenum"] = likenum
                            else:
                                item_data["likenum"] = 0
                            item_data["video_local"] = ''
                            item_data["create_time"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            last_ = True
                            insert_result = insert(item_data)
                            if insert_result:
                                redis_.S_add(f'cctv_video_id:{datetime.now().strftime("%Y%m%d")}', id_)
                        else:
                            continue
                if last_:
                    logger.info('完成一轮')
            else:
                time.sleep(2 * 60)
            time.sleep(2 * 60)
    else:
        time.sleep(2 * 60)
        return False


def get_spidernews(columns):
    sql = f"""select id, source_name, souce_url, channel, columns, column_id from sys_sp_news where columns='{columns}'"""
    result = __conn.getOne(sql)
    return result


def select_cf(intro, md5_):
    sql = f"""select * from sys_sp_contents where intro='{intro}' or md5_url='{md5_}'"""
    result = __conn.getOne(sql)
    # print(result)
    if result:
        return False
    else:
        return True


def get_video_item(item, video_info):
    """
    提取字段对应的数据
    :param item:
    :param video_info:
    :return:
    """
    item["title"] = video_info["title"]
    item["intro"] = video_info["brief"].strip()
    item["thumb_url"] = video_info["frame_url"]
    item["content"] = video_info["content"]
    item["video_url"] = video_info["url"]
    item["news_time"] = video_info["focus_date"]
    item["md5_url"] = MD5_(item["intro"])
    if select_cf(item["intro"], item["md5_url"]):
        return item
    else:
        redis_.S_add(f'cctv_video_id:{datetime.now().strftime("%Y%m%d")}', video_info["id"])
        return False


def start_(columns, stop_time):
    item = dict()
    results = get_spidernews(columns)
    id_, source_name, souce_url, channel, columns, column_id = results
    item["video_id"] = id_
    item['source_name'] = source_name
    item["channel"] = channel
    item["columns"] = columns
    while True:
        result = mian(souce_url, columns, item, stop_time)
        if result:
            break


if __name__ == '__main__':
    # print(get_spidernews('新闻联播'))
    print(select_cf('习近平抵达莫斯科开始对俄罗斯进行国事访问。'))
