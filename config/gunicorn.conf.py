import multiprocessing

bind = '127.0.0.1:8000'
workers = multiprocessing.cpu_count() * 2 + 1
pid = '/var/www/kidspay/shared/run/gunicorn.pid'
log_level = 'debug'
errorlog = '-'
accesslog = '-'
access_log_format = '%(u)s %(t)s "%(r)s" %(s)s %(b)s"'
