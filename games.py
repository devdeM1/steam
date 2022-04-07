from flask import make_response, abort
from config import db
from models import Games


def read_all():
    # Create the list of games from our data
    db_games = Games.query.order_by(Games.name).all()
    print(db_games)
    list_games = []
    for game in db_games:
        game_id = game.game_id
        name = game.name
        price = game.price
        genre = game.genre
        point = game.point
        data = {"game_id": game_id, "name": name, "price": price, "genre": genre, "point": point}
        list_games.append(data)
    '''# Serialize the data for the response
    games_schema = GamesSchema(many=True)
    print(games_schema, "   Shema")
    data = games_schema.dump(games)
    print("data:", data)'''
    return list_games


def read_one(received_game_id):
    one_game = Games.query.filter(Games.game_id == received_game_id).one_or_none()
    if one_game:
        game_id = one_game.game_id
        name = one_game.name
        price = one_game.price
        genre = one_game.genre
        point = one_game.point
        data = {"game_id": game_id, "name": name, "price": price, "genre": genre, "point": point}

        return data
    else:
        abort(
            404,
            "Game with {0} id not exist".format(received_game_id)
        )


def create(game):
    name = game.get("name")
    price = game.get("price")
    genre = game.get("genre")
    point = game.get("point")

    existing_game = (
        Games.query.filter(Games.name == name).one_or_none()
    )

    # Does such a game exist?
    # Yes
    if existing_game:
        abort(
            409,
            "Game {0} already exist".format(name)
        )
    # No
    else:
        new_game = Games()
        new_game.name = name
        new_game.price = price
        new_game.genre = genre
        new_game.point = point
        db.session.add(new_game)
        db.session.commit()


def update(received_game_id, game):
    # Get the game requested from the db into session
    update_game = Games.query.filter(
        Games.game_id == received_game_id
    ).one_or_none()

    # Try to find an existing person with the same name as the update
    name = game.get("name")
    price = game.get("price")
    genre = game.get("genre")
    point = game.get("point")

    existing_game = (
        Games.query.filter(Games.name == name)
        .filter(Games.price == price)
        .filter(Games.genre == genre)
        .filter(Games.point == point)
        .one_or_none()
    )

    # Are we trying to find a game that does not exist?
    if update_game is None:
        abort(
            404,
            "Game not found for Id: {received_game_id}".format(received_game_id),
        )

    # Would our update create a duplicate of another game already existing?
    elif (
        existing_game is not None and existing_game.game_id != received_game_id
    ):
        abort(
            409,
            "Game {name} {price} {genre} {point} exists already".format(
                name=name, price=price, genre=genre, point=point
            ),
        )

    # Otherwise go ahead and update!
    else:
        update_game.name = name
        update_game.price = price
        update_game.genre = genre
        update_game.point = point
        db.session.commit()
        return 200


def delete(received_game_id):
    # Get the game requested
    game = Games.query.filter(Games.game_id == received_game_id).one_or_none()

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
            "Game not found for Id: {game_id}".format(person_id=received_game_id),
        )




