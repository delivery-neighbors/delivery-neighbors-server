from apscheduler.schedulers.background import BackgroundScheduler

from neighbor.jobs.jobs import schedule_api


def start():
    print("jobs.updater.jobs")
    scheduler = BackgroundScheduler()
    scheduler.add_job(schedule_api, 'cron', minute=0)  # 매 시간 0분 될 때마다 실행
    # scheduler.add_job(schedule_api, 'interval', seconds=1)  # 시간 간격 별로 실행
    scheduler.start()
