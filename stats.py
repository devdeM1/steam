from models import Game, UserGame, User
from flask import abort


def every_game():
    db_games = Game.query.order_by(Game.name).all()
    db_games_user = UserGame.query.all()
    list_games_stats = []

    for game in db_games:
        id = game.id
        name = game.name
        count = 0
        for con in db_games_user:
            if con.game_id == id:
                count +=1
        data = {"game": name, "count": count}
        list_games_stats.append(data)
    return list_games_stats


def all_users():
    count = User.query.count()
    return count


def stats_for_one_game(received_game_name):
    game = Game.query.filter(Game.name == received_game_name).one_or_none()
    db_games_user = UserGame.query.all()
    count = 0
    if game:
        id = game.id
        for con in db_games_user:
            if con.game_id == id:
                count += 1
    else:
        abort(
            404,
            "Game {0} not exist".format(received_game_name)
        )
    return count
