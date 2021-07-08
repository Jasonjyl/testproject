"""
The configuration of this project
"""
import os.path


class Config:
    # general
    DEBUG = True

    # database
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:000713@localhost:3306/testproject'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:000713@localhost:3306/testproject'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # by default, it is set as True to track the update of the object
    # and send signals, which needs extra memory, so set it as False when unnecessary

    SQLALCHEMY_ECHO = True  # set it as True when debugging

    SECRET_KEY = 'aiyelianggewangdalaojidiaodi'

    # UPLOAD_PATH = 'photos/'
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    STATIC_DIR = os.path.join(BASE_DIR, 'static')
    TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
    UPLOAD_DIR = os.path.join(STATIC_DIR, 'upload')
    UPLOAD_ICON_DIR = os.path.join(STATIC_DIR, 'upload/icon')


class DevelopmentConfig(Config):
    ENV = 'development'


class ProductionConfig(Config):
    ENV = 'production'
    DEBUG = False


if __name__ == '__main__':
    print(Config.BASE_DIR)
