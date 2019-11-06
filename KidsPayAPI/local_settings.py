

DEBUG = False

''' 
    A list of all the people who get code error notifications. When DEBUG=False and 
    AdminEmailHandler is configured in LOGGING (done by default), Django emails these people the details of exceptions 
    raised in the request/response cycle.
'''
ADMINS = [('Farrukh', 'xamidovf@list.ru'), ('Umar', 'international-2014@mail.ru')]

ALLOWED_HOSTS = ['185.196.214.122', 'kidspay.uz', 'localhost']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'kidspaydatabase',
        'USER': 'kidspay',
        'PASSWORD': 'kidspay23',
        'HOST': '127.0.0.1',
        'PORT': '5452',
    }
}




