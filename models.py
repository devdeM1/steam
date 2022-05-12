
from config import db, ma, app
from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from datetime import datetime
import os

from flask_sqlalchemy import SQLAlchemy
from wtforms import form, fields, validators
from werkzeug.security import generate_password_hash, check_password_hash


class Game(db.Model):
    __tablename__ = "table_games"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    price = db.Column(db.Integer)
    genre_id = db.Column(db.Integer, ForeignKey('table_genre.id'))
    point = db.Column(db.Integer)
    genre = relationship("Genre")
    pic_path = db.Column(db.String(128), nullable=True)
    text = db.Column(db.String(5000), nullable=True)
    date = db.Column(db.Date, nullable=True)
    developer = db.Column(db.String(128), nullable=True)
    platform = db.Column(db.String(128), nullable=True)
    # Добавить поле ограничение возраста

    def check_year(self):
        flag = False
        print(datetime.now().year - 3)
        if self.date.year >= datetime.now().year - 3:
            flag = True
            return flag
        else:
            return flag


class User(UserMixin, db.Model):
    __tablename__ = "table_users"
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    second_name = db.Column(db.String(32))
    date = db.Column(db.String(32))
    balance = db.Column(db.Integer, default=0)
    country = db.Column(db.String(32))
    sex = db.Column(db.String(32))
    email = db.Column(db.String(120))
    phone_number = db.Column(db.String(120))
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.name)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return str(self.user_id)




  # Flask-Login integration
    # NOTE: is_authenticated, is_active, and is_anonymous
    # are methods in Flask-Login < 0.3.0
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.user_id

    # Required for administrative interface
    def __unicode__(self):
        return self.name


class UserGame(db.Model):
    __tablename__ = 'table_users_games'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('table_users.user_id', ondelete='CASCADE'))
    game_id = db.Column(db.Integer, ForeignKey('table_games.id', ondelete='CASCADE'))


class Genre(db.Model):
    __tablename__ = 'table_genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))


class Community(db.Model):
    __tablename__ = 'table_community'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))


class CommunityUser(db.Model):
    __tablename__ = 'table_community_user'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('table_users.user_id', ondelete='CASCADE'))
    community_id = db.Column(db.Integer, ForeignKey('table_community.id', ondelete='CASCADE'))


class CommunityGame(db.Model):
    __tablename__ = 'table_community_game'
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, ForeignKey('table_games.id',ondelete='CASCADE'))
    community_id = db.Column(db.Integer, ForeignKey('table_community.id', ondelete='CASCADE'))



