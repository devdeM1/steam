"""
Main module of the server file
"""

# 3rd party moudles
from flask import render_template, flash, redirect, url_for, request
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from forms import LoginForm, RegistrationForm, EditForm
from models import User, Game, UserGame, Genre
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


@app.route('/user/<name>')
@login_required
def user(name):
    user = User.query.filter_by(name=name).first_or_404()
    library = UserGame.query.filter(UserGame.user_id == user.user_id).all()
    list_games = []
    for game_user in library:
        game = Game.query.filter(
            Game.id == game_user.game_id
        ).one_or_none()
        genre = Genre.query.filter(Genre.id == game.genre_id).one_or_none().name
        name = game.name
        data = {
            "name": name,
            "genre": genre,
        }
        list_games.append(data)
    return render_template('user.html', user=user, games=list_games)


@app.route('/catalog')
def catalog():
    db_games = Game.query.order_by(Game.name).all()
    list_games = []

    for game in db_games:
        id = game.id
        name = game.name
        price = game.price
        genre = Genre.query.filter(Genre.id == game.genre_id).one_or_none().name
        point = game.point
        data = {"id": id, "name": name, "price": price, "genre": genre, "point": point}
        list_games.append(data)
    return render_template('catalog.html', title='Hello everybody' ,games=list_games)


@app.route('/edit/<user_id>', methods=['GET', 'POST'])
@login_required
def edit(user_id):
    form = EditForm()
    print('USER ID: ', user_id)
    if form.validate_on_submit():
        new_user = User(name=form.name.data,
                        second_name=form.second_name.data,
                        country=form.country.data,
                        sex=form.sex.data,
                        email=form.email.data,
                        phone_number=form.phone_number.data,
                        )
        existing_user = (
            User.query.filter(User.name == form.name.data)
                .filter(User.second_name == form.second_name.data)
                .filter(User.country == form.country.data)
                .filter(User.email == form.email.data)
                .filter(User.sex == form.sex.data)
                .filter(User.phone_number == form.phone_number.data)
                .one_or_none()
        )
        # Are we trying to find a user that does not exist?
        if existing_user is not None:
            flash('This user already exist!')
            return render_template('edit.html', form=form)
        else:
            print('JOIN in else')
            update_user = User.query.filter(User.user_id == user_id).one_or_none()
            print('UPDATE USER:', update_user)
            update_user.name = form.name.data
            update_user.second_name = form.second_name.data
            update_user.country = form.country.data
            update_user.email = form.email.data
            update_user.sex = form.sex.data
            update_user.phone_number = form.phone_number.data
            db.session.commit()
            flash('Congratulations, you are now a edit your profile!')
            return redirect(url_for('user', name=update_user.name))
    return render_template('edit.html', form=form)


@app.route('/<name>/my_games', methods=['GET', 'POST'])
@login_required
def my_games(name):
    user = User.query.filter_by(name=name).first_or_404()
    library = UserGame.query.filter(UserGame.user_id == user.user_id).all()
    list_games = []
    for game_user in library:
        game = Game.query.filter(
            Game.id == game_user.game_id
        ).one_or_none()
        genre = Genre.query.filter(Genre.id == game.genre_id).one_or_none().name
        name = game.name
        data = {
            "name": name,
            "genre": genre,
        }
        list_games.append(data)
    return render_template('my_games.html', games=list_games)

if __name__ == "__main__":
    connex_app.run(debug=True)





