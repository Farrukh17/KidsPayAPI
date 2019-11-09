from scheduler import recalculate
from apscheduler.schedulers.background import BackgroundScheduler


def start():
    scheduler = BackgroundScheduler()
    scheduler.shutdown(wait=False)
    # scheduler.add_job(recalculate.recalculate_schools, 'cron', hour=2)  # run every day at 02:00
    # scheduler.start()
