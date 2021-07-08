from extends import db

import datetime


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    icon = db.Column(db.String(1024))

    # 用户和留言连接，一个用户可以有多个留言
    messages = db.relationship('Message', backref='user', lazy='dynamic')

    def __str__(self):
        # info = 'This is a user named:....' # we can use this way to make an info string of the user
        return '<class User ---> name: ' + self.username + ' >'


class Message(db.Model):
    __tablename__ = 'message'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    text = db.Column(db.String(1024), nullable=False)
    time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)

    # 外键
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __str__(self):
        return '<class Message ---> title: ' + self.title + ' >'
