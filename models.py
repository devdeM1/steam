from config import db, ma
from marshmallow import Schema, fields
from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


class Game(db.Model):
    __tablename__ = "table_games"
    game_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    price = db.Column(db.Integer)
    genre_id = db.Column(db.Integer, ForeignKey('table_genre.id'))
    point = db.Column(db.Integer)
    # Добавить поле ограничение возраста


class User(db.Model):
    __tablename__ = "table_users"
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    date = db.Column(db.String(32))
    balance = db.Column(db.Integer)
    country = db.Column(db.String(32))
    sex = db.Column(db.String(32))


class UserGame(db.Model):
    __tablename__ = 'table_users_games'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('table_users.user_id'))
    game_id = db.Column(db.Integer, ForeignKey('table_games.game_id'))


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
    user_id = db.Column(db.Integer, ForeignKey('table_users.user_id'))
    community_id = db.Column(db.Integer, ForeignKey('table_community.id'))


class CommunityGame(db.Model):
    __tablename__ = 'table_community_game'
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, ForeignKey('table_games.game_id'))
    community_id = db.Column(db.Integer, ForeignKey('table_community.id'))
