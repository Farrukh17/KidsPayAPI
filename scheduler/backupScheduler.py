from scheduler import databaseBackup
from apscheduler.schedulers.background import BackgroundScheduler


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(databaseBackup.backup, 'interval', days=1)  # run every day
    scheduler.start()
