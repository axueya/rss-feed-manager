import datetime

from flask import Flask
from flask_marshmallow import Marshmallow
from flask_redis import FlaskRedis
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields
from sqlalchemy.dialects.mysql import LONGTEXT

import config_local as config

app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)
ma = Marshmallow(app)
redis_cache = FlaskRedis()

"""
用户表
"""


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(255))
    inserttime = db.Column(db.DateTime, nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.inserttime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        return {'id': self.id, 'username': self.username}

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def __repr__(self):
        return "<User %r>" % self.id


"""
Channel表
"""


class Channel(db.Model):
    __tablename__ = "channel"
    uuid = db.Column(db.String(255), primary_key=True)
    url = db.Column(db.String(255))
    categories = db.Column(db.String(255))
    tags = db.Column(db.String(255))
    title = db.Column(db.String(255))
    inserttime = db.Column(db.DateTime)

    def __repr__(self):
        return "<Channel %r>" % self.url


"""
subscription
"""


class Subscription(db.Model):
    __tablename__ = "subscription"

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    channel_id = db.Column(db.String(255), db.ForeignKey('channel.uuid'), primary_key=True)
    inserttime = db.Column(db.DateTime)
    user = db.relationship('User')
    channel = db.relationship('Channel')

    def __repr__(self):
        return "<Subscription {}-{}>".format(self.user_id, self.channel_id)


class Article(db.Model):
    __tablename__ = "article"
    url = db.Column(db.String(255), primary_key=True)
    uuid = db.Column(db.String(255))
    channel_uuid = db.Column(db.String(255), db.ForeignKey('channel.uuid'))
    channel_url = db.Column(db.String(255))
    channel_title = db.Column(db.String(255))
    content = db.Column(LONGTEXT)
    title = db.Column(db.String(255))
    summary = db.Column(LONGTEXT)
    updated = db.Column(db.DateTime)
    inserttime = db.Column(db.DateTime)

    def __repr__(self):
        return "<Article %r>" % self.url


class UserSchema(ma.ModelSchema):
    class Meta:
        model = User


class ChannelSchema(ma.ModelSchema):
    class Meta:
        model = Channel


class SubscriptionSchema(ma.ModelSchema):
    class Meta:
        model = Subscription

    include_fk = True


class UserSubscriptionSchema(ma.ModelSchema):
    user_id = fields.Integer()
    channel_id = fields.String()
    channel_url = fields.String()
    inserttime = fields.DateTime()
    title = fields.String()
    tags = fields.String()
    categories = fields.String()
    url = fields.String()


class ArticleSchema(ma.ModelSchema):
    channel_uuid = fields.String()
    channel_url = fields.String()
    channel_title = fields.String()
    title = fields.String()
    uuid = fields.String()
    url = fields.String()
    content = fields.String()
    summary = fields.String()
    updated = fields.DateTime()


if __name__ == "__main__":
    db.drop_all()
    db.create_all()
