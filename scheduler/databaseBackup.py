import subprocess


def backup():
    subprocess.call('/var/www/kidspay/current/config/backup/pg_backup_rotated.sh', shell=True)
