import os
from config import db
from models import Game, User, UserGame, Genre, Community, CommunityUser, CommunityGame


# Data to initialize database with
GAMES = [
    {"name": "Dota 2", "price": 100, "genre": "strategy", "point": 5},
    {"name": "CS", "price": 1000, "genre": "shooter"},
    {"name": "Hearthstone", "price": 777, "genre": "strategy"},
]

USERS = [
    {"name": "Maks", "date": "02.02.2002", "balance": 100, "country": "Belarus", "sex": "man"},
    {"name": "Dima", "date": "03.03.2003", "balance": 777, "country": "Belarus", "sex": "man"},
]

USERS_GAMES = [
    {"game_name": "CS", "user_name": "Dima"},
    {"game_name": "Hearthstone", "user_name": "Maks"},
    {"game_name": "Dota 2", "user_name": "Dima"},
    {"game_name": "Hearthstone", "user_name": "Dima"}
]

GENRES = [
    {"name": "strategy"},
    {"name": "shooter"}
]

COMMUNITY = [
    {"name": "Party 12 vs 12 Doka 2"},
    {"name": "easy-peasy, lemon squeezy"}
]

COMMUNITY_USER = [
    {"community_name": "Party 12 vs 12 Doka 2", "user_name": "Dima"},
    {"community_name": "Party 12 vs 12 Doka 2", "user_name": "Maks"},
    {"community_name": "easy-peasy, lemon squeezy", "user_name": "Dima"},
]

COMMUNITY_GAME = [
    {"community_name": "Party 12 vs 12 Doka 2", "game_name": "Dota 2"},
    {"community_name": "Party 12 vs 12 Doka 2", "game_name": "CS"},
    {"community_name": "easy-peasy, lemon squeezy", "game_name": "Hearthstone"},
]

db.drop_all()
# Create the database
db.create_all()

# iterate over the PEOPLE structure and populate the database
for genre in GENRES:
    g = Genre(
        name=genre.get("name")
    )
    db.session.add(g)

for game in GAMES:
    genre = Genre.query.filter(Genre.name == game.get("genre")).one_or_none()

    p = Game(
        name=game.get("name"),
        price=game.get("price"),
        genre_id=genre.id,
        point=game.get("point")
    )
    db.session.add(p)

for user in USERS:
    u = User(
        name=user.get("name"),
        date=user.get("date"),
        balance=user.get("balance"),
        country=user.get("country"),
        sex=user.get("sex")
    )
    db.session.add(u)

for connect in USERS_GAMES:
    game = Game.query.filter(Game.name == connect.get("game_name")).one_or_none()
    user = User.query.filter(User.name == connect.get("user_name")).one_or_none()
    c = UserGame(
        game_id=game.game_id,
        user_id=user.user_id
    )
    db.session.add(c)

for community in COMMUNITY:
    com = Community(
        name=community.get("name")
    )
    db.session.add(com)

for community_user in COMMUNITY_USER:
    community = Community.query.filter(Community.name == community_user.get("community_name")).one_or_none()
    user = User.query.filter(User.name == community_user.get("user_name")).one_or_none()
    c_u = CommunityUser(
        community_id=community.id,
        user_id=user.user_id
    )
    db.session.add(c_u)

for community_game in COMMUNITY_GAME:
    community = Community.query.filter(Community.name == community_game.get("community_name")).one_or_none()
    game = Game.query.filter(Game.name == community_game.get("game_name")).one_or_none()
    c_g = CommunityGame(
        community_id=community.id,
        game_id=game.game_id
    )
    db.session.add(c_g)

db.session.commit()
