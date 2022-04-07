import os
from config import db
from models import Games, Users, UsersGames


# Data to initialize database with
GAMES = [
    {"name": "Dota 2", "price": 100, "genre": "strategy", "point": 5},
    {"name": "CS", "price": 1000},
    {"name": "Hardstown", "price": 777},
]

USERS = [
    {"name": "Maks", "date": "02.02.2002", "balance": 100, "country": "Belarus", "sex": "man"},
    {"name": "Dima", "date": "03.03.2003", "balance": 777, "country": "Belarus", "sex": "man"},
]

USERS_GAMES = [
    {"game_id": MAKS, "user_id": 1},
    {"game_id": 3, "user_id": 1},
    {"game_id": 1, "user_id": 2},
    {"game_id": 2, "user_id": 2},
    {"game_id": 3, "user_id": 2}
]

db.drop_all()
# Create the database
db.create_all()

# iterate over the PEOPLE structure and populate the database
for game in GAMES:
    p = Games(
        name=game.get("name"),
        price=game.get("price"),
        genre=game.get("genre"),
        point=game.get("point")
    )
    db.session.add(p)

for user in USERS:
    u = Users(
        name=user.get("name"),
        date=user.get("date"),
        balance=user.get("balance"),
        country=user.get("country"),
        sex=user.get("sex")
    )
    db.session.add(u)

for connect in USERS_GAMES:
    c = UsersGames(
        game_id=connect.get("game_id"),
        user_id=connect.get("user_id")
    )
    db.session.add(c)
db.session.commit()
