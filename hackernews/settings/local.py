from .base import *

DEBUG = env('DEBUG')
SECRET_KEY = env('SECRET_KEY')
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

INSTALLED_APPS += [
    # third party apps
    'django_q',
    'django_extensions',
    'django.contrib.humanize',
    

    # core apps
    'hackernews.apps.news.apps.NewsConfig',
    'api.apps.ApiConfig',
    'hackernews.scheduler.apps.SchedulerConfig'
]

DATABASES = {
    'default': 
        env.db_url('SQLITE_URL',default=f"sqlite:///{BASE_DIR / '../local-sqlite.db'}")  
    }

ASGI_APPLICATION = 'hackernews.asgi.application'

Q_CLUSTER = {
    'name': 'hackersCluster',
    'timeout': 90,
    'retry': 120,
    'cpu_affinity': 1,
    'redis': {
        'host': 'localhost',
        'port': 6379,
        'db': 0,
        'password': None,
        'socket_timeout': None,
        'charset': 'utf-8',
        'errors': 'strict',
        'unix_socket_path': None
    }
}