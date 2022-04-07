import os
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

basedir = os.path.abspath(os.path.dirname(__file__))

# Create the connexion application instance
connex_app = connexion.App(__name__, specification_dir=basedir)

# Get the underlying Flask app instance
app = connex_app.app

# Build the Sqlite ULR for SqlAlchemy
database_url = "postgresql+psycopg2://user_postgres:qwerty123255@localhost:5432/user_postgres"

# Configure the SqlAlchemy part of the app instance
app.config["SQLALCHEMY_ECHO"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Create the SqlAlchemy db instance
db = SQLAlchemy(app)

# Initialize Marshmallow
ma = Marshmallow(app)