"""
Main module of the server file
"""

# 3rd party moudles
from flask import render_template
from flask_admin import Admin
from config import db, app
from models import User, Game, Genre
from flask_admin.contrib.sqla import ModelView
from flask_basicauth import BasicAuth
import flask_admin as admin
from models import MyAdminIndexView

# local modules
import config


# Get the application instance
connex_app = config.connex_app

# set optional bootswatch theme
app.config['BASIC_AUTH_USERNAME'] = 'devdem'
app.config['BASIC_AUTH_PASSWORD'] = 'devdemisadmin'
app.config['BASIC_AUTH_FORCE'] = True
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

basic_auth = BasicAuth(app)


admin = admin.Admin(app, 'Example: Auth',
                    index_view=MyAdminIndexView(),
                    base_template='my_master.html',
                    template_mode='bootstrap4')
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Game, db.session))
admin.add_view(ModelView(Genre, db.session))
# Add administrative views here

# Read the swagger.yml file to configure the endpoints
connex_app.add_api("swagger.yml")


# create a URL route in our application for "/"
@connex_app.route("/")
def home():
    """
    This function just responds to the browser URL
    localhost:5000/
    :return:        the rendered template "home.html"
    """
    return render_template("home.html")


if __name__ == "__main__":
    connex_app.run(debug=True)


@connex_app.route('/secret')
@basic_auth.required
def secret_view():
    return render_template('secret.html')