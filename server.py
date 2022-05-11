"""
Main module of the server file
"""

# 3rd party moudles
from flask import render_template, flash, redirect, url_for, request
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from forms import LoginForm, RegistrationForm, EditForm
from models import User, Game, UserGame, Genre, CommunityUser, Community
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
    db_games = Game.query.order_by(Game.name).all()
    db_games_user = UserGame.query.all()
    list_games_stats = []
    max_count = 0
    most_pop_game = Game.query.filter(Game.id == 1).one_or_none()
    for game in db_games:
        id = game.id
        name = game.name
        count = 0
        for con in db_games_user:
            if con.game_id == id:
                count += 1
        if max_count < count:
            most_pop_game = game
            max_count = count
    return render_template("home.html", game=most_pop_game)


@app.route("/deposit/<user_name>")
def deposit(user_name):
    user = User.query.filter(User.name == user_name).one_or_none()
    user.balance = user.balance+100
    db.session.commit()
    db_games = Game.query.order_by(Game.name).all()
    db_games_user = UserGame.query.all()
    list_games_stats = []
    max_count = 0
    most_pop_game = Game.query.filter(Game.id == 1).one_or_none()
    for game in db_games:
        id = game.id
        name = game.name
        count = 0
        for con in db_games_user:
            if con.game_id == id:
                count += 1
        if max_count < count:
            most_pop_game = game
            max_count = count
    return render_template("home.html", game=most_pop_game)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
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
        pic_path = game.pic_path
        data = {"id": id, "name": name, "price": price, "genre": genre, "point": point, "pic_path": pic_path}
        list_games.append(data)
    return render_template('catalog.html', games=list_games)


@app.route('/page_game/<game_id>')
def page_game(game_id):
    game = Game.query.filter(Game.id == game_id).one_or_none()
    if game is None:
        flash('Invalid game')
        return render_template('catalog.html')
    else:
        genre = Genre.query.filter(Genre.id == game.genre_id).one_or_none().name
        data = {
                "name": game.name,
                "price": game.price,
                "genre": genre,
                "point": game.point,
                "pic_path": game.pic_path,
                "text": game.text,
                "developer": game.developer,
                "date": game.date,
                "platform": game.platform}
        return render_template('page_game.html', game=data)


@app.route('/edit/<user_id>', methods=['GET', 'POST'])
@login_required
def edit(user_id):
    form = EditForm()
    print('USER ID: ', user_id)
    if form.validate_on_submit():
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
            update_user = User.query.filter(User.user_id == user_id).one_or_none()
            update_user.name = form.name.data
            update_user.second_name = form.second_name.data
            update_user.country = form.country.data
            update_user.email = form.email.data
            update_user.sex = form.sex.data
            update_user.phone_number = form.phone_number.data
            db.session.commit()
            flash('Congratulations, you are now a edit your profile!')
            return redirect(url_for('user', name=update_user.name))
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.second_name.data = current_user.second_name
        form.country.data = current_user.country
        form.email.data = current_user.email
        form.sex.data = current_user.sex
        form.phone_number.data = current_user.phone_number

    return render_template('edit.html', title='Edit Profile', form=form)


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


@app.route('/<user_name>/buy_game/<game_name>')
@login_required
def buy_game(user_name, game_name):
    user = User.query.filter(
        User.name == user_name
    ).one_or_none()

    if user is None:
        # User not exist
        flash(
            404,
            "User {0} not exist"
        )

    game = Game.query.filter(
        Game.name == game_name
    ).one_or_none()

    # Does such a game exist?
    # No
    if game is None:
        flash(
            404,
            "Game  not exist",
        )

    # You have this game&
    all_your_games = UserGame.query.filter(UserGame.user_id == user.user_id).all()
    previously_purchased_game = False
    for your_game in all_your_games:
        if game.id == your_game.game_id:
            previously_purchased_game = True
    if previously_purchased_game:
        flash(
            "You have this game"

        )
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
    if user.balance < game.price:
        flash(
            "Not enough balance"
        )
        return render_template('page_game.html', game=game)
    new_user_game = UserGame()
    new_user_game.game_id = game.id
    new_user_game.user_id = user.user_id
    db.session.add(new_user_game)
    user.balance -= game.price
    db.session.commit()
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



@app.route('/<name>/my_communities', methods=['GET', 'POST'])
@login_required
def my_communities(name):
    user = User.query.filter_by(name=name).first_or_404()
    if user is None:
        # User not exist
        flash("User  not exist")
    else:
        db_communities = CommunityUser.query.filter(CommunityUser.user_id == user.user_id).all()
        list_communities = []
        for community in db_communities:
            community_for_output = Community.query.filter(
                Community.id == community.community_id
            ).one_or_none()
            name = community_for_output.name
            data = {
                "name": name,
            }
            list_communities.append(data)
        return render_template('my_communities.html', title=' My Communities', communities=list_communities)


@app.route('/communities')
def communities():
    db_community = Community.query.order_by(Community.name).all()
    list_community = []
    for community in db_community:
        db_community_user = CommunityUser.query.filter(CommunityUser.community_id == community.id).all()
        count = 0
        for i in db_community_user:
            count = count+1
        name = community.name
        data = {"name": name, "count": count
                }
        list_community.append(data)
    print(list_community)
    return render_template('communities.html', communities=list_community)


@app.route('/community/<community_name>')
@login_required
def community(community_name):
    comm = Community.query.filter(Community.name == community_name).one_or_none()
    db_comm_users = CommunityUser.query.filter(CommunityUser.community_id == comm.id).all()
    list_users = []
    for i in db_comm_users:
        user = User.query.filter(
            User.id == i.game_id
        ).one_or_none()
        name = user.name
        data = {
            "name": name,
        }
        list_users.append(data)
    return render_template('community.html', users=list_users, comm=comm)


@app.route('/join_community')
@login_required
def join_community(community_name, user_id):
    user = User.query.filter(
        User.user_id == user_id
    ).one_or_none()

    if user is None:
        # User not exist
        flash(
            "User {0} not exist"
        )

    community = Community.query.filter(
        Community.name == community_name
    ).one_or_none()

    if community is None:
        # User not exist
        flash(
            "Community {0} not exist"
        )
    new_user_community = CommunityUser()
    new_user_community.user_id = user.user_id
    new_user_community.community_id = community.id
    db.session.add(new_user_community)
    db.session.commit()
    return render_template('communities.html')


if __name__ == "__main__":
    connex_app.run(debug=True)





