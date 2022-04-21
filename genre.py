from flask import make_response, abort
from config import db
from models import Genre, Game


def read_all():
    # Create the list of genres from our data
    db_genres = Genre.query.order_by(Genre.name).all()
    list_genres = []
    for genre in db_genres:
        id = genre.id
        name = genre.name
        data = {"id": id, "name": name}
        list_genres.append(data)
    return list_genres


def create(genre):
    name = genre.get("name")
    print(name)
    existing_genre = (
        Genre.query.filter(Genre.name == name).one_or_none()
    )

    # Does such a game exist?
    # Yes
    if existing_genre:
        abort(
            409,
            "Genre {0} already exist".format(name)
        )
    # No
    else:
        new_genre = Genre()
        new_genre.name = name
        db.session.add(new_genre)
        db.session.commit()


def read_one(received_genre_name):
    genre = Genre.query.filter(
        Genre.name == received_genre_name
    ).one_or_none()
    if genre:
        id = genre.id
        name = genre.name
        data = {
            "id": id,
            "name": name,
        }
        return data
    else:
        abort(
            404,
            "Genre {0} not exist".format(received_genre_name)
        )


def update(received_genre_name, genre):
    # Get the genre requested from the db into session
    update_genre = Genre.query.filter(
        Genre.name == received_genre_name
    ).one_or_none()

    #
    name = genre.get("name")

    existing_genre = Genre.query.filter(Genre.name == name).one_or_none()


    # Are we trying to find a genre that does not exist?
    if update_genre is None:
        abort(
            404,
            "Genre {0} not found".format(received_genre_name),
        )

    # Would our update create a duplicate of another genre already existing?
    elif (
        existing_genre is not None and existing_genre.name != received_genre_name
    ):
        abort(
            409,
            "Genre {name}  exists already".format(
                name=name
            ),
        )

    # Otherwise go ahead and update!
    else:
        update_genre.name = name
        db.session.commit()
        return 200


def delete(received_genre_name):
    genre = Genre.query.filter(Genre.name == received_genre_name).one_or_none()

    if genre is None:
        abort(
            404,
            "Genre not found for name: {0}".format(received_genre_name),
        )

    # There is at least one game with this genre
    game = Game.query.filter(Game.genre_id == genre.id).one_or_none()
    if game:
        abort(
            404,
            "Please, before deleting this genre, change it in the game {0}".format(game.name),
        )
    else:
        db.session.delete(genre)
        db.session.commit()
        return make_response(
            "Genre {0} deleted".format(received_genre_name), 200
        )
