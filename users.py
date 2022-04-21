from flask import make_response, abort
from config import db
from models import User, Game, UserGame, Community, CommunityUser, Genre


def read_all():
    # Create the list of games from our data
    db_users = User.query.all()
    print(db_users)
    list_users = []
    for user in db_users:
        user_id = user.user_id
        name = user.name
        date = user.date
        balance = user.balance
        country = user.country
        sex = user.sex
        data = {
            "user_id": user_id,
            "name": name,
            "date": date,
            "balance": balance,
            "country": country,
            "sex": sex
            }
        list_users.append(data)
    return list_users


def create(user):
    name = user.get("name")
    date = user.get("date")
    balance = user.get("balance")
    country = user.get("country")
    sex = user.get("sex")

    existing_user = (
        User.query.filter(User.name == name).one_or_none()
    )

    # Does such a game exist?
    # Yes
    if existing_user:
        abort(
            409,
            "User {0} already exist".format(name)
        )
    # No
    else:
        new_user = User()
        new_user.name = name
        new_user.date = date
        new_user.balance = balance
        new_user.country = country
        new_user.sex = sex
        db.session.add(new_user)
        db.session.commit()


def read_one(received_user_name):
    user = User.query.filter(
        User.name == received_user_name
    ).one_or_none()
    print(user)
    if user:
        user_id = user.user_id
        name = user.name
        date = user.date
        balance = user.balance
        country = user.country
        sex = user.sex
        data = {
            "user_id": user_id,
            "name": name,
            "date": date,
            "balance": balance,
            "country": country,
            "sex": sex}

        return data
    else:
        abort(
            404,
            "User with {0} id not exist".format(received_user_name)
        )


def update(received_user_name, user):
    # Get the user requested from the db into session
    update_user = User.query.filter(
        User.name == received_user_name
    ).one_or_none()

    #
    name = user.get("name")
    date = user.get("date")
    balance = user.get("balance")
    country = user.get("country")
    sex = user.get("sex")

    existing_user = (
        User.query.filter(User.name == name)
        .filter(User.date == date)
        .filter(User.balance == balance)
        .filter(User.country == country)
        .filter(User.sex == sex)
        .one_or_none()
    )

    # Are we trying to find a user that does not exist?
    if update_user is None:
        abort(
            404,
            "User not found for name: {0}".format(received_user_name),
        )

    # Would our update create a duplicate of another user already existing?
    elif (
        existing_user is not None
    ):
        abort(
            409,
            "User {name} {date} {balance} {country} {sex} exists already".format(
                name=name,
                date=date,
                balance=balance,
                country=country,
                sex=sex
            ),
        )

    # Otherwise go ahead and update!
    else:
        update_user.name = name
        update_user.date = date
        update_user.balance = balance
        update_user.country = country
        update_user.sex = sex
        db.session.commit()
        return 200


# Change to received_user_name.Think about connection
def delete(received_user_name):
    # Get the user requested
    user = User.query.filter(User.name == received_user_name).one_or_none()

    # Did we find a user?
    if user is not None:
        db.session.delete(user)
        db.session.commit()
        return make_response(
            "User {user} deleted".format(user=received_user_name), 200
        )

    # Otherwise, nope, didn't find that user
    else:
        abort(
            404,
            "User {0} not found".format(received_user_name),
        )


def add_game(user_name, game_name):
    user = User.query.filter(
        User.name == user_name
    ).one_or_none()

    if user is None:
        # User not exist
        abort(
            404,
            "User {0} not exist".format(user_name),
        )

    game = Game.query.filter(
        Game.name == game_name
    ).one_or_none()

    # Does such a game exist?
    # No
    if game is None:
        abort(
            404,
            "Game {0} not exist(SALAM)".format(game_name),
        )
    new_user_game = UserGame()
    new_user_game.game_id = game.id
    new_user_game.user_id = user.user_id
    db.session.add(new_user_game)
    db.session.commit()


def join_the_community(user_name, community_name):
    user = User.query.filter(
        User.name == user_name
    ).one_or_none()

    if user is None:
        # User not exist
        abort(
            404,
            "User {0} not exist".format(user_name),
        )

    community = Community.query.filter(
        Community.name == community_name
    ).one_or_none()

    if community is None:
        # User not exist
        abort(
            404,
            "Community {0} not exist".format(community_name),
        )
    new_user_community = CommunityUser()
    new_user_community.user_id = user.user_id
    new_user_community.community_id = community.id
    db.session.add(new_user_community)
    db.session.commit()


def view_community(user_name):
    user = User.query.filter(
        User.name == user_name
    ).one_or_none()

    if user is None:
        # User not exist
        abort(
            404,
            "User {0} not exist".format(user_name),
        )
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
        return list_communities


def view_games(user_name):
    user = User.query.filter(
        User.name == user_name
    ).one_or_none()

    if user is None:
        # User not exist
        abort(
            404,
            "User {0} not exist".format(user_name),
        )
    else:
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
        return list_games

