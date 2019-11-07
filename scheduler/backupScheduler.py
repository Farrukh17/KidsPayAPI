from scheduler import databaseBackup
from apscheduler.schedulers.background import BackgroundScheduler


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(databaseBackup.backup, 'cron', hour=0)  # run every day at 00:00
    scheduler.start()
