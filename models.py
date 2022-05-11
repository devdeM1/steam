
from config import db, ma, app
from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from flask_login import UserMixin

import os
from flask import Flask, url_for, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from wtforms import form, fields, validators
import flask_admin as admin

from flask_admin.contrib import sqla
from flask_admin import helpers, expose
from werkzeug.security import generate_password_hash, check_password_hash


class Game(db.Model):
    __tablename__ = "table_games"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    price = db.Column(db.Integer)
    genre_id = db.Column(db.Integer, ForeignKey('table_genre.id'))
    point = db.Column(db.Integer)
    genre = relationship("Genre")
    pic = db.Column(db.String(128))
    # Добавить поле ограничение возраста


class User(UserMixin, db.Model):
    __tablename__ = "table_users"
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    second_name = db.Column(db.String(32))
    date = db.Column(db.String(32))
    balance = db.Column(db.Integer)
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


'''   # Flask-Login integration
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
'''

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


'''# Define login and registration forms (for flask-login)
class LoginForm(form.Form):
    login = fields.StringField(validators=[validators.DataRequired()])
    password = fields.PasswordField(validators=[validators.DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

    def validate_login(self, field):
        user = self.get_user()

        if user is None:
            raise validators.ValidationError('Invalid user')

        # we're comparing the plaintext pw with the the hash from the db
        if not check_password_hash(user.password, self.password.data):
        # to compare plain text passwords use
        # if user.password != self.password.data:
            raise validators.ValidationError('Invalid password')

    def get_user(self):
        return db.session.query(User).filter_by(login=self.login.data).first()


class RegistrationForm(form.Form):
    login = fields.StringField(validators=[validators.DataRequired()])
    email = fields.StringField()
    password = fields.PasswordField(validators=[validators.DataRequired()])

    def validate_login(self, field):
        if db.session.query(User).filter_by(login=self.login.data).count() > 0:
            raise validators.ValidationError('Duplicate username')


# Initialize flask-login
def init_login():
    login_manager = login.LoginManager()
    login_manager.init_app(app)

    # Create user loader function
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.query(User).get(user_id)


# Create customized model view class
class MyModelView(sqla.ModelView):

    def is_accessible(self):
        return login.current_user.is_authenticated


# Create customized index view class that handles login & registration
class MyAdminIndexView(admin.AdminIndexView):

    @expose('/')
    def index(self):
        if not login.current_user.is_authenticated:
            return redirect(url_for('.login_view'))
        return super(MyAdminIndexView, self).index()

    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        # handle user login
        form = LoginForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = form.get_user()
            login.login_user(user)
        print("CURRECT USER  ", login.current_user.is_authenticated)
        if login.current_user.is_authenticated:
            return redirect(url_for('.index'))
        link = '<p>Don\'t have an account? <a href="' + url_for('.register_view') + '">Click here to register.</a></p>'
        print("link: ", link)
        self._template_args['form'] = form
        self._template_args['link'] = link
        return super(MyAdminIndexView, self).index()

    @expose('/register/', methods=('GET', 'POST'))
    def register_view(self):
        form = RegistrationForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = User()

            form.populate_obj(user)
            # we hash the users password to avoid saving it as plaintext in the db,
            # remove to use plain text:
            user.password = generate_password_hash(form.password.data)
            print("USER PASSWORD", user.password)
            db.session.add(user)
            db.session.commit()

            login.login_user(user)
            return redirect(url_for('.index'))
        link = '<p>Already have an account? <a href="' + url_for('.login_view') + '">Click here to log in.</a></p>'
        self._template_args['form'] = form
        self._template_args['link'] = link
        return super(MyAdminIndexView, self).index()

    @expose('/logout/')
    def logout_view(self):
        login.logout_user()
        return redirect(url_for('.index'))


# Flask views
@app.route('/')
def index():
    return render_template('index.html')


# Initialize flask-login
init_login()

'''