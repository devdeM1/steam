import os
from config import db
from models import Game, User, UserGame, Genre, Community, CommunityUser, CommunityGame
from werkzeug.security import generate_password_hash


# Data to initialize database with
GAMES = [
    {"name": "Dota 2", "price": 0, "genre": "Strategy", "point": 5},
    {"name": "Hearthstone", "price": 7, "genre": "Strategy"},
    {"name": "ELDEN RING", "price": 35, "genre": "RPG", "point": 9},
    {"name": "Rogue Legacy 2", "price": 10, "genre": "Indie", "point": 8},
    {"name": "NARAKA: BLADEPOINT", "price": 10, "genre": "PvP", "point": 7},
    {"name": "Hollow Knight", "price": 4, "genre": "Indie", "point": 9},
    {"name": "iRacing", "price": 7, "genre": "Simulation", "point": 8},
    {"name": "Deep Rock Galactic", "price": 7, "genre": "PvE", "point": 9},
    {"name": "The Stanley Parable: Ultra Deluxe", "price": 12, "genre": "Walking Simulator", "point": 9},
    {"name": "Slay the Spire", "price": 5, "genre": "Card Game", "point": 10},
    {"name": "Peglin", "price": 10, "genre": "Pinball", "point": 8},
    {"name": "Dread Hunger", "price": 15, "genre": "Survival", "point": 6},
    {"name": "Valheim", "price": 8, "genre": "Survival", "point": 9},
    {"name": "Nioh 2 – The Complete Edition", "price": 33, "genre": "JRPG", "point": 8},
    {"name": "Dune: Spice Wars", "price": 15, "genre": "Building", "point": 8},
    {"name": "Dorfromantik", "price": 6, "genre": "Puzzle", "point": 9},
    {"name": "Wallpaper Engine", "price": 3, "genre": "Indie", "point": 10},
    {"name": "STAR WARS™ Complete Collection", "price": 45, "genre": "RPG", "point": 9},
    {"name": "Phasmophobia", "price": 8, "genre": "Horror", "point": 9},
    {"name": "Underdog Detective Complete Season", "price": 14, "genre": "RPG", "point": 7},
    {"name": "Northgard", "price": 4, "genre": "RTS", "point": 9},
    {"name": "Rust", "price": 20, "genre": "Survival", "point": 9},
    {"name": "Raft", "price": 13, "genre": "Crafting", "point": 9},
    {"name": "Northgard: The Viking Age Edition", "price": 17, "genre": "RTS", "point": 8},
    {"name": "Dinosaur Fossil Hunter", "price": 10, "genre": "Building", "point": 7},
    {"name": "Noita", "price": 9, "genre": "Roguelike", "point": 9},
    {"name": "Gunfire Reborn", "price": 8, "genre": "Action", "point": 7},
    {"name": "Dead Cells: Road to the Sea Bundle", "price": 12, "genre": "Indie", "point": 8},
    {"name": "Stardew Valley", "price": 10, "genre": "RPG", "point": 10},
    {"name": "Project Hospital Collection", "price": 13, "genre": "Strategy", "point": 8},
    {"name": "Ready or Not", "price": 25, "genre": "Tactical", "point": 9},
    {"name": "ARK: Ultimate Survivor Edition", "price": 32, "genre": "RPG", "point": 7, "pic_path": "ARK: Ultimate Survivor Edition"},
    {"name": "Escape Simulator", "price": 7, "genre": "Puzzle", "point": 9},
    {"name": "God of War", "price": 40, "genre": "Combat", "point": 10},
    {"name": "Project Zomboid", "price": 11, "genre": "Zombies", "point": 9},
    {"name": "Vampire Survivors", "price": 2, "genre": "RPG", "point": 10},
    {"name": "Squad", "price": 23, "genre": "War", "point": 9},
    {"name": "Dead Cells", "price": 8, "genre": "Roguelite", "point": 10},
    {"name": "Terraria", "price": 7, "genre": "2D", "point": 9.6},
    {"name": "King Arthur: Knight's Tale", "price": 21, "genre": "Strategy", "point": 8.3},
    {"name": "Project Hospital", "price": 5, "genre": "Building", "point": 9.1},
    {"name": "The Forest", "price": 11, "genre": "Horror", "point": 9.6},
    {"name": "The Planet Crafter", "price": 11.49, "genre": "Simulation", "point": 9.6},
    {"name": "Euro Truck Simulator 2", "price": 2.74, "genre": "Simulation", "point": 9.7},
    {"name": "WARNO", "price": 30, "genre": "PvP", "point": 8},
    {"name": "No Man's Sky", "price": 35, "genre": "Space", "point": 8},
    {"name": "JUNKPUNK", "price": 6, "genre": "Building", "point": 7},
    {"name": "Wildermyth", "price": 9, "genre": "Choices Matter", "point": 9},
    {"name": "Core Keeper", "price": 8, "genre": "2D", "point": 9, "pic_path": "Core Keeper"},
    {"name": "Cultivation Tales", "price": 11, "genre": "Sandbox", "point": 3, "pic_path":"Cultivation Tales"},
    {"name": "Pummel Party", "price": 8, "genre": "Co-op", "point": 9},
    {"name": "Atelier Ryza: Ever Darkness & the Secret Hideout", "price": 14, "genre": "Anime", "point": 7 ,"pic_path": "Atelier Ryza: Ever Darkness & the Secret Hideout"},
    {"name": "Farming Simulator 22", "price": 35, "genre": "Co-op", "point": 9},
    {"name": "Enter the Gungeon", "price": 4, "genre": "Roguelike", "point": 9},
    {"name": "Danganronpa 1/2/V3", "price": 13, "genre": "Adventure", "point": 7, "pic_path": "Danganronpa"},
    {"name": "Satisfactory", "price": 15, "genre": "Crafting", "point": 9},
    {"name": "World War 3", "price": 8, "genre": "Modern", "point": 7},
    {"name": "Death's Door", "price": 8, "genre": "RPG", "point": 9},
    {"name": "Factorio", "price": 12, "genre": "Crafting", "point": 9},
    {"name": "Barotrauma", "price": 3, "genre": "Submarine", "point": 9, "pic_path":"Barotrauma"},
    {"name": "Risk of Rain 2: Survivors of the Void", "price": 8, "genre": "Co-op", "point": 8},
    {"name": "Nioh: Complete Edition", "price": 6, "genre": "Ninja", "point": 7},
    {"name": "Fall Guys: Ultimate Knockout", "price": 11, "genre": "PvP", "point": 7},
    {"name": "BeamNG.drive", "price": 13, "genre": "Driving", "point": 9, "pic_path":"BeamNG.drive"},
    {"name": "Hades", "price": 13, "genre": "Mythology", "point": 9},
    {"name": "Don't Starve Together", "price": 8, "genre": "Crafting", "point": 9},
    {"name": "Car Mechanic Simulator 2021", "price": 10, "genre": "Driving", "point": 9, "pic_path": "Car Mechanic Simulator 2021"},
    {"name": "Skul: The Hero Slayer", "price": 7, "genre": "2D", "point": 9},
    {"name": "7 Days to Die", "price": 15, "genre": "Open World", "point": 8, 'pic_path': "7days"},
    {"name": "WARRIORS OROCHI 4 Ultimate Deluxe Edition", "price": 20, "genre": "Action", "point": 7},
    {"name": "WorldBox - God Simulator", "price": 10, "genre": "Sandbox", "point": 9},
    {"name": "Mount & Blade II: Bannerlord", "price": 30, "genre": "Action", "point": 9},
    {"name": "Beat Saber", "price": 15, "genre": "Moddable", "point": 9,'pic_path':"Beat Saber"},
    {"name": "Kingdom Two Crowns", "price": 2, "genre": "Indie", "point": 9},
    {"name": "Euro Truck Simulator 2 - Iberia", "price": 10, "genre": "Indie", "point": 7},
    {"name": "Sable", "price": 8, "genre": "Indie", "point": 9},
    {"name": "TEKKEN 7", "price": 10, "genre": "Arcade", "point": 7},
    {"name": "Bounty game", "price": 8, "genre": "Action", "point": 8, "pic_path": "Bounty game"},
    {"name": "Inscryption", "price": 13, "genre": "Adventure", "point": 10},
    {"name": "SCUM", "price": 16, "genre": "Zombies", "point": 8},
    {"name": "DayZ", "price": 45, "genre": "Zombies", "point": 9, "pic_path": "DayZ"},
    {"name": "Teardown", "price": 11, "genre": "Voxel", "point": 9},
    {"name": "Stacklands", "price": 3, "genre": "Card Battler", "point": 9},
    {"name": "Garry's Mod", "price": 7, "genre": "Co-op", "point": 10},
    {"name": "Acquitted", "price": 3, "genre": "Shooter", "point": 10, "pic_path": "acquitted"},
    {"name": "UBOAT", "price": 15, "genre": "War", "point": 8},
    {"name": "Witch It", "price": 3, "genre": "Indie", "point": 8},
    {"name": "Underdog Detective-Episode 6 to 17", "price": 11, "genre": "RPG", "point": 5},
    {"name": "Frostpunk", "price": 4, "genre": "Survival", "point": 9},
    {"name": "Prehistoric Kingdom", "price": 15, "genre": "Sandbox", "point": 8},
    {"name": "Mirror 2: Project X Bundle", "price": 5, "genre": "RPG", "point": 7},
    {"name": "Streets of Rogue", "price": 4, "genre": "Action", "point": 10},
    {"name": "Unrailed!", "price": 3, "genre": "Co-op", "point": 9},
    {"name": "Bloons TD 6", "price": 6, "genre": "Co-op", "point": 10, "pic_path": "Bloons TD 6"},
    {"name": "DARK SOULS™: REMASTERED", "price": 40, "genre": "RPG", "point": 8, "pic_path":"DARK SOULS : REMASTERED"},
    {"name": "Subnautica", "price": 1, "genre": "Survival", "point": 10},
    {"name": "Metal Mind", "price": 8, "genre": "Roguelite", "point": 8},
]

USERS = [
    {"name": "Maks",
     "date": "02.02.2002",
     "balance": 100,
     "country": "Belarus",
     "sex": "men",
     "login": "maks",
     "password": "1111",
     "email": "kyky@qq.com"},
    {"name": "Dima",
     "date": "03.03.2003",
     "balance": 777,
     "country": "Belarus",
     "sex": "men",
     "login": "dima",
     "password": "1234",
     "email": "kyky@qq.com"
     },
    {"name": "Nikita",
     "date": "08.12.2001",
     "balance": 0,
     "country": "Belarus",
     "sex": "men",
     "login": "nikita0812",
     "password": "1111",
     "email": "kykyq@qq.com"},
    {"name": "Andrei",
     "date": "18.02.1999",
     "balance": 100,
     "country": "Germany",
     "sex": "men",
     "login": "andreya",
     "password": "1111",
     "email": "kykyw@qq.com"},
    {"name": "Alex",
     "date": "08.07.1989",
     "balance": 100,
     "country": "USA",
     "sex": "men",
     "login": "alexqwe",
     "password": "1111",
     "email": "kykye@qq.com"},
    {"name": "Polina",
     "date": "02.12.2002",
     "balance": 100,
     "country": "Belarus",
     "sex": "women",
     "login": "impolina",
     "password": "1111",
     "email": "kykyr@qq.com"},
    {"name": "Tania",
     "date": "30.10.2012",
     "balance": 100,
     "country": "Russia",
     "sex": "women",
     "login": "tania322",
     "password": "1111",
     "email": "kykyy@qq.com"},
    {"name": "Vika",
     "date": "02.02.2002",
     "balance": 100,
     "country": "Belarus",
     "sex": "women",
     "login": "4ikavika",
     "password": "1111",
     "email": "kykyi@qq.com"},
    {"name": "Kristina",
     "date": "02.03.2002",
     "balance": 100,
     "country": "Belarus",
     "sex": "women",
     "login": "kristinka",
     "password": "1111",
     "email": "kykyasd@qq.com"},
    {"name": "Fillip",
     "date": "02.10.2002",
     "balance": 100,
     "country": "Belarus",
     "sex": "man",
     "login": "fillipgod",
     "password": "1111",
     "email": "kyky8@qq.com"},
    {"name": "Ksenia",
     "date": "02.02.2002",
     "balance": 100,
     "country": "Ukraine",
     "sex": "women",
     "login": "ksushatop",
     "password": "1111",
     "email": "kykqwer@qq.com"},
    {"name": "Felix",
     "date": "02.02.2002",
     "balance": 100,
     "country": "Belarus",
     "sex": "man",
     "login": "ymnuikotfelixnaidet",
     "password": "1111",
     "email": "kyky123@qq.com"},

]

USERS_GAMES = [
    {"game_name": "Hearthstone", "user_name": "Maks"},
    {"game_name": "Dota 2", "user_name": "Dima"},
    {"game_name": "Hearthstone", "user_name": "Dima"},
    {"game_name": "Peglin", "user_name": "Dima"},
    {"game_name": "SCUM", "user_name": "Dima"},
    {"game_name": "Witch It", "user_name": "Dima"},
]
'''{"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "Witch It", "user_name": "Maks"},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "SCUM", "user_name": "Dima"},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "Witch It", "user_name": "Dima"},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
'''

GENRES = [
    {"name": "Strategy"},
    {"name": "Shooter"},
    {"name": "RPG"},
    {"name": "Indie"},
    {"name": "PvP"},
    {"name": "Simulation"},
    {"name": "PvE"},
    {"name": "Walking Simulator"},
    {"name": "Card Game"},
    {"name": "Pinball"},
    {"name": "Survival"},
    {"name": "JRPG"},
    {"name": "Building"},
    {"name": "Puzzle"},
    {"name": "Horror"},
    {"name": "RTS"},
    {"name": "Crafting"},
    {"name": "Roguelike"},
    {"name": "Tactical"},
    {"name": "Combat"},
    {"name": "Zombies"},
    {"name": "War"},
    {"name": "Roguelite"},
    {"name": "2D"},
    {"name": "Space"},
    {"name": "Choices Matter"},
    {"name": "Sandbox"},
    {"name": "Co-op"},
    {"name": "Anime"},
    {"name": "Adventure"},
    {"name": "Modern"},
    {"name": "Action"},
    {"name": "Submarine"},
    {"name": "Ninja"},
    {"name": "Driving"},
    {"name": "Mythology"},
    {"name": "Open World"},
    {"name": "Moddable"},
    {"name": "Arcade"},
    {"name": "Voxel"},
    {"name": "Card Battler"},
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
        point=game.get("point"),
        pic_path=game.get("pic_path")
    )
    db.session.add(p)

for user in USERS:
    u = User(
        name=user.get("name"),
        date=user.get("date"),
        balance=user.get("balance"),
        country=user.get("country"),
        sex=user.get("sex"),
        email=user.get("email")
    )
    db.session.add(u)

for connect in USERS_GAMES:
    game = Game.query.filter(Game.name == connect.get("game_name")).one_or_none()
    user = User.query.filter(User.name == connect.get("user_name")).one_or_none()
    c = UserGame(
        game_id=game.id,
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
        game_id=game.id
    )
    db.session.add(c_g)

db.session.commit()
