from config import db, ma
from marshmallow import Schema, fields
from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


class Games(db.Model):
    __tablename__ = "table_games"
    game_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    price = db.Column(db.Integer)
    genre = db.Column(db.String(32))
    point = db.Column(db.Integer)
    # Добавить поле ограничение возраста


class Users(db.Model):
    __tablename__ = "table_users"
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    date = db.Column(db.String(32))
    balance = db.Column(db.Integer)
    country = db.Column(db.String(32))
    sex = db.Column(db.String(32))


class UsersGames(db.Model):
    __tablename__ = 'table_users_games'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('table_users.user_id'))
    game_id = db.Column(db.Integer, ForeignKey('table_games.game_id'))




