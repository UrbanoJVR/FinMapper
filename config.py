import os


class Config:
    # SECRET_KEY = os.environ.get('SECRET_KEY')
    SECRET_KEY = 'NOBODY_KNOWS'
    UPLOAD_DIR = '/tmp'
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'data.sqlite') + '?foreign_keys=ON'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    pass


class TestConfig(Config):
    SECRET_KEY = 'NOBODY_KNOWS'
    UPLOAD_DIR = '/tmp'
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

    @staticmethod
    def init_app(app):
        pass

class TestItConfig(Config):
    SECRET_KEY = 'NOBODY_KNOWS'
    UPLOAD_DIR = '/tmp'
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'data-test.sqlite') + '?foreign_keys=ON'
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    pass


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'test': TestConfig,
    'test-it': TestItConfig,
    'default': DevelopmentConfig
}
