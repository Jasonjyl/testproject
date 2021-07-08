import logging
import os
from logging.handlers import RotatingFileHandler

from flask import Flask

import config
from apps.user.view import user_bp
from extends import db, bootstrap


def create_app():  # create the app that is connected to the server
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config.from_object(config.DevelopmentConfig)

    db.init_app(app)  # connect the SQLAlchemy object with the app
    # db.create_all(app=app)
    bootstrap.init_app(app)  # bind the bootstrap with the app

    # Blueprint
    app.register_blueprint(user_bp)
    # app.register_blueprint(message_bp)

    # app.logger.setLevel(logging.INFO)
    #
    # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    #
    # file_handler = RotatingFileHandler(os.path.join(config.Config.BASE_DIR, 'logs/catchatlog.log'),
    #                                    maxBytes=10 * 1024 * 1024, backupCount=10)
    # file_handler.setFormatter(formatter)
    # file_handler.setLevel(logging.INFO)
    #
    # if not app.debug:
    #     app.logger.addHandler(file_handler)
    # 设置日志的记录等级
    logging.basicConfig(level=logging.DEBUG)  # 调试debug级
    # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
    file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024 * 1024 * 100, backupCount=10)
    # 创建日志记录的格式 日志等级 输入日志信息的文件名 行数 日志信息
    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象（flask app使用的）添加日志记录器
    logging.getLogger().addHandler(file_log_handler)

    return app
