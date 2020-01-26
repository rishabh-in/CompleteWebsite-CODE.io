## CodeCompany/__init__.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
###########################################################

app=Flask(__name__)
app.config["SECRET_KEY"]="mykey"
basedir=os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///"+os.path.join(basedir,"data.sqlite")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
db=SQLAlchemy(app)
Migrate(app,db)
###########################################################
login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view="users.login" ### We will create a users blueprint and then register it.

from CodeCompany.Core.views import core
from CodeCompany.Users.views import users
from CodeCompany.CodePost.views import code_posts
from CodeCompany.Error_Pages.handler import error

app.register_blueprint(core)
app.register_blueprint(error)
app.register_blueprint(code_posts)
app.register_blueprint(users)