
from flask_sqlalchemy import SQLAlchemy

from tools.config_module import DB_URL
from app import application

application.config["SQLALCHEMY_DATABASE_URI"] = DB_URL
DB = SQLAlchemy(application)
