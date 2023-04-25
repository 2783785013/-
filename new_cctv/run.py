from apscheduler.schedulers.background import BlockingScheduler
from main.Cctv_Main import start_

if __name__ == '__main__':
    start_('新闻联播', 22)
    scheduler = BlockingScheduler(timezone="Asia/Shanghai")
    scheduler.add_job(start_, 'cron', hour='19', minute='20', args=['新闻联播', 22])
    scheduler.start()
    # start_()