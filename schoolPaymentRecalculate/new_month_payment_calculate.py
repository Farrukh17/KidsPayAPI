from datetime import datetime
from schoolPaymentRecalculate import recalculate
from apscheduler.schedulers.background import BackgroundScheduler


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(recalculate.recalculate_school, 'cron', minute=10)
    scheduler.start()
