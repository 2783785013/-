from apscheduler.schedulers.background import BlockingScheduler
from main.Cctv_Main import start_

if __name__ == '__main__':
    start_('中国新闻', 24)
    # scheduler = BlockingScheduler(timezone="Asia/Shanghai")
    # scheduler.add_job(start_, 'cron', hour='12', minute='00', args=['中国新闻', 24])
    # scheduler.start()
    # start_()