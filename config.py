import os
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_mail import Mail
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







from flask_mail import  Message
MAIL_SERVER = os.environ.get('MAIL_SERVER')
MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
ADMINS = ['maxmed2002@gmail.com']

mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": os.environ['user_email'],
    "MAIL_PASSWORD": os.environ['email_password']
}

app.config.update(mail_settings)

mail = Mail(app)
# Create the SqlAlchemy db instance
db = SQLAlchemy(app)

# Initialize Marshmallow
ma = Marshmallow(app)