"""
Main module of the server file
"""

# 3rd party moudles
from flask import render_template, flash, redirect, url_for, request
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from forms import LoginForm, RegistrationForm
from models import User
from flask_admin import Admin
from config import db, app
from flask_admin.contrib.sqla import ModelView
from flask_basicauth import BasicAuth
from werkzeug.urls import url_parse
import flask_admin as admin
'''from models import MyAdminIndexView'''

# local modules
import config

# Get the application instance
connex_app = config.connex_app

login = LoginManager(app)
login.login_view = 'login'


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

'''
basic_auth = BasicAuth(app)


@connex_app.route('/secret')
@basic_auth.required
def secret_view():
    return render_template('secret.html')
'''
'''
admin = admin.Admin(app, 'Example: Auth',
                    index_view=MyAdminIndexView(),
                    base_template='my_master.html',
                    template_mode='bootstrap4')
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Game, db.session))
admin.add_view(ModelView(Genre, db.session))
# Add administrative views here
'''
# Read the swagger.yml file to configure the endpoints
connex_app.add_api("swagger.yml")


@app.route("/")
def home():
    """
    This function just responds to the browser URL
    localhost:5000/
    :return:        the rendered template "home.html"
    """
    return render_template("home.html")


@app.route("/home")
def home1():
    """
    This function just responds to the browser URL
    localhost:5000/
    :return:        the rendered template "home.html"
    """
    return render_template("home.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.name.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('home'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(name=form.name.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == "__main__":
    connex_app.run(debug=True)





