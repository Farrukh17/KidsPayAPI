import subprocess


def backup():
    subprocess.call('../config/backup/pg_backup_rotated.sh', shell=True)
