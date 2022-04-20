import os
from config import db
from models import Games

# Data to initialize database with
GAMES = [
    {"name": "Dota 2", "price": 100},

]

# Delete database file if it exists currently
if os.path.exists("games.db"):
    os.remove("games.db")

# Create the database
db.create_all()

# iterate over the PEOPLE structure and populate the database
for person in GAMES:
    p = Games(name=games.get("name"), price=games.get("price"))
    db.session.add(p)

db.session.commit()