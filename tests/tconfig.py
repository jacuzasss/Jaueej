from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from datetime import datetime, timedelta
import os
from os.path import abspath, join

basedir = abspath(os.path.dirname(__file__))


class Config(object):
    ADMIN = 'test@test.com'
    BLOGGING_SITENAME = os.environ.get('SITENAME') or 'LibrePatron'
    BLOGGING_SITEURL = os.environ.get('SITEURL') or 'https://example.com'
    BLOGGING_URL_PREFIX = '/updates'
    BLOGGING_BRANDURL = os.environ.get('BRANDURL')
    BLOGGING_TWITTER_USERNAME = os.environ.get('TWITTER')
    BLOGGING_DISQUS_SITENAME = os.environ.get('DISQUS')
    BLOGGING_GOOGLE_ANALYTICS = os.environ.get('GOOGLE_ANALYTICS')
    BLOGGING_PERMISSIONS = True
    BLOGGING_PERMISSIONNAME = 'admin'
    BLOGGING_PLUGINS = None
    BLOGGING_ALLOW_FILE_UPLOAD = True
    BLOGGING_ESCAPE_MARKDOWN = False
    ISSO_CONFIG_PATH = f'/tmp/{os.urandom(16)}'
    COMMENTS_DB_PATH = os.environ.get('COMMENTS_DB_PATH_TEST') or '/var/lib/db/comments.db'
    PREFERRED_URL_SCHEME = 'https'
    SCHEDULER_BASE = datetime.now() + timedelta(minutes=1)
    SCHEDULER_HOUR = SCHEDULER_BASE.hour
    SCHEDULER_MINUTE = SCHEDULER_BASE.minute
    SECRET_KEY = 'a-very-secret-key'
    SECRET_KEY_LOCATION = f'/tmp/{os.urandom(16)}'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + join(basedir, 'app_test.db')
    SCHEDULER_JOBSTORES = {
            'default': SQLAlchemyJobStore(url=SQLALCHEMY_DATABASE_URI)
        }
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    THEME = 'spacelab'
    SERVER_NAME = 'librepatron.com'
    BCRYPT_LOG_ROUNDS = 4
    TESTING = True
    WTF_CSRF_ENABLED = False
