from paymentsScheduler import recalculate
from apscheduler.schedulers.background import BackgroundScheduler


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(recalculate.recalculate_schools, 'interval', days=1)  # run every day
    scheduler.start()
