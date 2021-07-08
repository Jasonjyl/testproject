import datetime
import logging
import os
from logging.handlers import RotatingFileHandler

import pymysql

from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from apps.user.model import User, Message
from config import Config
from extends import db

user_bp = Blueprint('user', __name__)

# 用于登录功能的SQL注入漏洞
sql_db = pymysql.connect(host="127.0.0.1",
                         user="root",
                         password="000713",
                         db="testproject",
                         port=3306)

cursor = sql_db.cursor()


def getMessages():
    messages_list = Message.query.all()
    return messages_list


@user_bp.route('/', methods=['GET', 'POST'])
def index():
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
    userid = request.cookies.get('userid', None)
    message_list = getMessages()

    message_user_dict = {}
    for message in message_list:
        author_id = message.author_id
        user = User.query.get(author_id)
        message_user_dict[message.id] = user.username

    if userid:
        user = User.query.get(userid)
        return render_template('index.html', user=user, message_list=message_list, message_user_dict=message_user_dict)
    return render_template('index.html', message_list=message_list, message_user_dict=message_user_dict)


# here we implement register, login
@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        repassword = request.form.get('repassword')

        if password == repassword:
            user = User()
            user.username = username
            # user.password = generate_password_hash(password)
            user.password = password

            db.session.add(user)
            db.session.commit()

            # return '注册成功'
            response = redirect('/')
            response.set_cookie('userid', str(user.id), max_age=1800)  # half an hour
            return response
        else:
            return '两次输入的密码不一致，请重新注册'

    return render_template('register.html')


@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    # user login
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        print("!!!!!!!!!!!!!!!!!!!")
        print("!!!!!!!!!!!!!!!!!!!")
        print(f"select * from user where username='{username}' and password='{password}'")
        print("!!!!!!!!!!!!!!!!!!!")
        print("!!!!!!!!!!!!!!!!!!!")
        # sql = cursor.execute("SELECT * FROM user WHERE username='{username}'".format(username=username))
        sql = cursor.execute(f"select * from user where username='{username}' and password='{password}'")

        # '; drop database bbs; --
        user = cursor.fetchone()  # 使用 fetchone() 方法获取单条数据.
        # user = User.query.filter(User.username == username).first()

        if user:
            # if check_password_hash(user.password, password):
            # if user.password == password:
            if user[1] == password:
                # 1. cookie 机制实现
                response = redirect(url_for('user.index'))
                # response.set_cookie('userid', str(user.id), max_age=1800)  # half an hour
                response.set_cookie('userid', str(user[0]), max_age=1800)  # half an hour
                return response

            else:
                return render_template('login.html', message='用户名或密码错误')
        else:
            return render_template('login.html', message='用户名或密码错误')

    return render_template('login.html')


@user_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    response = redirect(url_for('user.index'))
    response.delete_cookie('userid')
    return response


@user_bp.route('/writeMessage', methods=['GET', 'POST'])
def writeMessage():
    title = request.args.get('title')
    text = request.args.get('text')
    time = datetime.datetime.now()

    message = Message()
    message.title = title
    message.text = text
    message.time = time

    userid = request.cookies.get('userid', None)
    if userid:
        user = User.query.get(userid)
        message.author_id = userid
        db.session.add(message)
        db.session.commit()
        return redirect(url_for('user.index'))
    else:
        flash('请先登录')
        return redirect(url_for('user.index'))


@user_bp.route('/update', methods=['GET', 'POST'])
def update():
    userid = request.cookies.get('userid', None)
    user = User()
    if userid:
        user = User.query.get(userid)
    if request.method == 'POST':
        userid = request.cookies.get('userid', None)
        if userid:
            user = User.query.get(userid)
        username = request.form.get('username')
        password = request.form.get('password')
        repassword = request.form.get('repassword')
        newpassword = request.form.get('newpassword')
        icon = request.files.get('icon')

        validate_types = ['png', 'jpeg', 'jpg', 'JPEG', 'JPG']

        if icon.filename.split('.')[-1] not in validate_types:
            flash('图片类型不符（png, JPEG, jpeg, jpg）')
            return render_template('update.html', user=user)
        icon_name = secure_filename(icon.filename)
        icon_path = os.path.join(Config.UPLOAD_ICON_DIR, icon_name)
        icon.save(icon_path)

        path = 'upload/icon'
        user.icon = os.path.join(path, icon_name)

        db.session.commit()
        return render_template('update.html', id=userid, user=user)
    return render_template('update.html', id=userid, user=user)


@user_bp.route('/display/<id>', methods=['GET', 'POST'])
def display(id):
    user = User.query.get(id)
    return render_template('display.html', user=user)


@user_bp.route('/xss')
def xss():
    return render_template('xss.html')


@user_bp.route('/test')
def test():
    if request.method == 'GET':
        data = request.args.get('id')
        print(data)
        return data
    return 'Test-Test'


@user_bp.route('/xsstest')
def xsstest():
    if request.method == 'GET':
        data = request.args.get('title')
        return render_template('xsstest.html', data=data)
    return render_template('xsstest.html')
