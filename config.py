import os
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

basedir = os.path.abspath(os.path.dirname(__file__))

# Create the connexion application instance
connex_app = connexion.App(__name__, specification_dir=basedir)

# Get the underlying Flask app instance
app = connex_app.app


# Build the Sqlite ULR for SqlAlchemy
database_url = "postgresql+psycopg2://user_postgres:qwerty123255@db:5432/user_postgres"

# Configure the SqlAlchemy part of the app instance
app.config["SQLALCHEMY_ECHO"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'super secret key'

# set optional bootswatch theme
app.config['BASIC_AUTH_USERNAME'] = 'devdem'
app.config['BASIC_AUTH_PASSWORD'] = 'devdemisadmin'
app.config['BASIC_AUTH_FORCE'] = True
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'



# Create the SqlAlchemy db instance
db = SQLAlchemy(app)

# Initialize Marshmallow
ma = Marshmallow(app)