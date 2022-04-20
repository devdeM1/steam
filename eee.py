from models import UsersGames, Games, Users
import logging


for connect in UsersGames.query.order_by(UsersGames.game_id):
    game = Games.query.filter(Games.game_id == connect.game_id).one_or_none()
    user = Users.query.filter(Users.user_id == connect.user_id).one_or_none()
    print(user.name, 'play in ', game.name)
