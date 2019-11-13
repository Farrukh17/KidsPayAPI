from scheduler import databaseBackup
from apscheduler.schedulers.background import BackgroundScheduler


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(databaseBackup.backup, 'cron', hour=10, minute=22, id='pd_backup', replace_existing=True)  # run every day at 00:00
    scheduler.start()
