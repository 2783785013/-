from apscheduler.schedulers.background import BlockingScheduler
from wx import wx_start
from wb import wb_start
from dy import dy_start
from PingHu_wx import pinghu_start
import time
import traceback

def run_():
    try:
        get()
        dy_start()
        wx_start()
        wb_start()
        pinghu_start()
    except Exception as e:
        traceback.print_exc()



def get():
    print(5555555)
    print(time.time())


if __name__ == '__main__':
    scheduler = BlockingScheduler(timezone='Asia/Shanghai')
    # scheduler.add_job(get, 'cron',second='3')
    scheduler.add_job(get, 'cron', hour='14',minute='27')
    scheduler.add_job(get, 'cron', hour='14',minute='30')
    scheduler.start()
