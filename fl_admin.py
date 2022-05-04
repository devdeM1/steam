from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqlamodel import ModelView

admin = Admin(app)
admin.add_view(ModelView(User, db.session))