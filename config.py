import os
basedir = os.path.abspath(os.path.dirname(__file__))

POSTGRES = {
    'user': 'db_svc',
    'pw': 'yEV3L5rccFSmZ9TUq6Hy65qjj7LXetLk328bqsxdXbMphetPdAWNB8JnT4F3a78S',
    'db': 'mud_dev',
    'host': 'localhost',
    'port': '5432',
}

class Config(object):
    ASSETS_FOLDER = None
    SECRET_KEY = 'fuck1n-$h1t_w1zzz@rd$'
    DEBUG = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://{user}:{pw}@{host}:{port}/{db}'.format(**POSTGRES)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    MAIL_FROM_EMAIL = "johnmullins@gmail.com" # For use in application emails