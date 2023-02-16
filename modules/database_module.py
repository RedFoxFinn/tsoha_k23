
from flask_sqlalchemy import SQLAlchemy

from modules.config_module import DB_URL
from app import application

application.config["SQLALCHEMY_DATABASE_URI"] = DB_URL
DB = SQLAlchemy(application)