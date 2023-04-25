from apscheduler.schedulers.background import BlockingScheduler
from main.Cctv_Main import start_

if __name__ == '__main__':
    start_('新闻直播间', 19)
    scheduler = BlockingScheduler(timezone="Asia/Shanghai")
    scheduler.add_job(start_, 'cron', hour='1', minute='00', misfire_grace_time=60, args=['新闻直播间', 19])
    scheduler.start()
