from flask import make_response, abort
from config import db
from models import Game, Genre


def read_all():
    # Create the list of games from our data
    db_games = Game.query.order_by(Game.name).all()
    list_games = []

    for game in db_games:
        game_id = game.game_id
        name = game.name
        price = game.price
        genre = Genre.query.filter(Genre.id == game.genre_id).one_or_none().name
        point = game.point
        data = {"game_id": game_id, "name": name, "price": price, "genre": genre, "point": point}
        list_games.append(data)
    return list_games


def read_one(received_game_name):
    one_game = Game.query.filter(Game.name == received_game_name).one_or_none()
    if one_game:
        game_id = one_game.game_id
        name = one_game.name
        price = one_game.price
        genre = Genre.query.filter(Genre.id == one_game.genre_id).one_or_none()
        genre = genre.name
        point = one_game.point
        data = {"game_id": game_id, "name": name, "price": price, "genre": genre, "point": point}

        return data
    else:
        abort(
            404,
            "Game {0} not exist".format(received_game_name)
        )


def create(game):
    name = game.get("name")
    price = game.get("price")
    genre = game.get("genre")
    point = game.get("point")

    existing_game = (
        Game.query.filter(Game.name == name).one_or_none()
    )

    existing_genre = (
        Genre.query.filter(Genre.name == genre).one_or_none()
    )
    # Does such a game exist?
    # Yes
    if existing_game:
        abort(
            409,
            "Game {0} already exist".format(name)
        )
    elif existing_genre is None:
        abort(
            409,
            "Genre {0} not exist".format(genre)
        )
    # No
    else:
        new_game = Game()
        new_game.name = name
        new_game.price = price
        new_game.genre_id = existing_genre.id
        new_game.point = point
        db.session.add(new_game)
        db.session.commit()


def update(received_game_name, game):
    # Get the game requested from the db into session
    update_game = Game.query.filter(
        Game.name == received_game_name
    ).one_or_none()

    # Try to find an existing person with the same name as the update
    name = game.get("name")
    price = game.get("price")
    genre = game.get("genre")
    point = game.get("point")

    existing_genre = Genre.query.filter(Genre.name == genre).one_or_none()

    if existing_genre is None:
        abort(
            404,
            "Genre {0} not exist".format(genre)
        )

    existing_game = (
        Game.query.filter(Game.name == name)
        .filter(Game.price == price)
        .filter(Game.genre_id == existing_genre.id)
        .filter(Game.point == point)
        .one_or_none()
    )

    # Are we trying to find a game that does not exist?

    if update_game is None:
        abort(
            404,
            "Game {0} not found".format(received_game_name),
        )

    # Would our update create a duplicate of another game already existing?
    elif (
        existing_game is not None and existing_game.name != received_game_name
    ):
        abort(
            409,
            "Game {name}, price:{price}, genre:{genre}, pont:{point} exists already".format(
                name=name, price=price, genre=genre, point=point
            ),
        )
    # Otherwise go ahead and update!
    else:
        update_game.name = name
        update_game.price = price
        update_game.genre_id = existing_genre.id
        update_game.point = point
        db.session.commit()
        return 200

# Change to received_game_name.Think about connection


def delete(received_game_id):
    # Get the game requested
    game = Game.query.filter(Game.game_id == received_game_id).one_or_none()

    # Did we find a game?
    if game is not None:
        db.session.delete(game)
        db.session.commit()
        return make_response(
            "Game {game_id} deleted".format(game_id=received_game_id), 200
        )

    # Otherwise, nope, didn't find that game
    else:
        abort(
            404,
            "Game not found for Id: {game_id}".format(game_id=received_game_id),
        )




