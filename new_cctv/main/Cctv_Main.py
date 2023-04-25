from spider.xwlb_spider import get_likenum, get_video_info_
from spider.Cctv_Spider import *
from main.xwlb_main import redis_, get_spidernews, MD5_, select_cf, insert, timeStamp_to_time, get_video_item
from utils.my_dowload import down_video
import asyncio
import os
import subprocess
from settings import save_path

dv = down_video()


def start_main(topid, columns, item, id_, stop_time):
    while True:
        if int(str(datetime.now())[11:13]) > stop_time - 1:
            logger.info(f'{datetime.now().strftime("%Y%m%d")}{columns}抓取完成')
            return True
        datas_list = get_data_list(topid)
        if datas_list:
            last_ = False
            for datas in datas_list:
                if not redis_.S_isMember(f'cctv_video_id:{datetime.now().strftime("%Y%m%d")}', datas["id"]):
                    if datas["brief"]:
                        if '本期节目主要内容' not in datas["brief"]:
                            result_ = get_item(item, datas, id_)
                            if result_:
                                last_ = True
                        elif '本期节目主要内容' in datas["brief"] and len(datas_list) == 1:
                            logger.info(f'{datetime.now().strftime("%Y%m%d")}{columns}抓取完成')
                            get_item(item, datas, id_)
                            return True
                        else:
                            redis_.S_add(f'cctv_video_id:{datetime.now().strftime("%Y%m%d")}', datas["id"])
                    else:
                        continue
                else:
                    continue
            if last_:
                logger.info('完成一轮')
        else:
            time.sleep(3 * 60)
        time.sleep(2 * 60)


def get_item(item, datas, id_):
    if item["columns"] in ['焦点访谈', '新闻联播']:
        datas = get_video_info_(datas["id"])
        item_data = get_video_item(item, datas)
        if item_data:
            item_data = creat_time_and_likenum(datas, item_data)
            item_data["video_local"] = ''
            return insert_item(datas, item_data)
        else:
            return False
    else:
        item_data = get_video_info(item, datas)
        if item_data:
            # print(datas["id"])
            video_urls = get_video_urls(datas["guid"])
            data_time = datetime.now().strftime("%Y-%m-%d")
            out_path = f'{save_path}/{data_time}/{id_}/{datas["id"]}.mp4'
            new_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(new_loop)
            if len(video_urls) == 1:
                result_ = asyncio.get_event_loop().run_until_complete(
                    dv.download_much(video_urls[0], f'{save_path}/{data_time}/{id_}/', down_type=3,
                                     name=datas['id']))
                if result_:
                    file_path = result_
                else:
                    file_path = ''
            elif len(video_urls) > 1:
                timestamp = int(time.time())
                for video_ in video_urls:
                    result_ = asyncio.get_event_loop().run_until_complete(
                        dv.download_much(video_, f'{save_path}/{data_time}/{id_}/{timestamp}/', down_type=3))
                    if result_:
                        with open(f'{save_path}/{data_time}/{id_}/{timestamp}/{datas["id"]}.txt', 'a') as f1:
                            f1.write(f"file '{result_}'\n")
                file_txt = f'{save_path}/{data_time}/{id_}/{timestamp}/{datas["id"]}.txt'
                ss = merging_video_audio(file_txt, out_path)
                if ss:
                    file_path = out_path
                else:
                    file_path = ''
            else:
                return False
        else:
            return False
        if file_path:
            item_data = creat_time_and_likenum(datas, item_data)
            item_data['video_local'] = file_path.replace('Z:', 'https://www.lsgcloud.com/gmrb')
            return insert_item(datas, item_data)
        else:
            return False


def insert_item(datas, item):
    insert_result = insert(item)
    if insert_result:
        redis_.S_add(f'cctv_video_id:{datetime.now().strftime("%Y%m%d")}', datas["id"])
        return True
    else:
        return False


def creat_time_and_likenum(datas, item_data):
    likenum = get_likenum(datas["id"])
    if likenum:
        item_data["likenum"] = likenum
    else:
        item_data["likenum"] = 0
    item_data["create_time"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return item_data


def get_video_info(item, video_info):
    item["title"] = video_info["title"]
    item["intro"] = video_info["brief"].strip()
    item["content"] = ''
    item["thumb_url"] = video_info["image"]
    item["video_url"] = video_info["url"]
    # print(video_info["url"])
    item["news_time"] = timeStamp_to_time(video_info["focus_date"])
    item["md5_url"] = MD5_(item["intro"])
    if select_cf(item["intro"], item["md5_url"]):
        return item
    else:
        redis_.S_add(f'cctv_video_id:{datetime.now().strftime("%Y%m%d")}', video_info["id"])
        return []


def merging_video_audio(file_txt, output_path, ffmpeg_path=r'D:/FFmpeg/bin'):
    """
    视频文件合并，使用了ffmpeg的api
    :param file_txt: 合并文件
    :param output_path: 输出位置
    :param ffmpeg_path: ffmpeg安装路径
    """
    res = ''
    cmd = f'{ffmpeg_path}/ffmpeg.exe -f concat  -safe 0 -i {file_txt} -acodec copy -vcodec copy {output_path} -loglevel quiet'
    try:
        res = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        res_ = res.wait(timeout=15)
    except Exception as e:
        if 'timed out' in str(e):
            res.kill()
            os.remove(output_path)
            time.sleep(2)
            merging_video_audio(file_txt, output_path)
        else:
            return False
    else:
        if res_ == 0:
            return True
        else:
            return False


def start_(columns, stop_time):
    item = dict()
    results = get_spidernews(columns)
    if results:
        id_, source_name, souce_url, channel, columns, column_id = results
        item["video_id"] = id_
        item['source_name'] = source_name
        item["channel"] = channel
        item["columns"] = columns
        while True:
            print('启动')
            result = start_main(column_id, columns, item, id_, stop_time)
            if result:
                return None
    else:
        logger.info(f'请在sys_sp_news表添加{columns}')


if __name__ == '__main__':
    start_main('TOPC1451558532019883')
