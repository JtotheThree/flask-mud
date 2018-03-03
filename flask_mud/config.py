import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['johnmullins@gmail.com']


class DevConfig(Config):
    DEBUG = True


class TestConfig(Config):
    Debug = False
    TESTING = True

    SQLALCHEMY_DATABASE_URI = 'sqlite:///'


class ProdConfig(Config):
    pass


configs = {
    'dev': DevConfig,
    'test': TestConfig,
    'prod': ProdConfig,
    'default': ProdConfig
}
