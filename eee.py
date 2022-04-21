from models import UsersGames, Games, Users
import logging


for connect in UsersGames.query.order_by(UsersGames.id):
    game = Games.query.filter(Games.id == connect.id).one_or_none()
    user = Users.query.filter(Users.user_id == connect.user_id).one_or_none()
    print(user.name, 'play in ', game.name)
