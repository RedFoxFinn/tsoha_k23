
from flask_sqlalchemy import SQLAlchemy

from src.modules.config_module import DB_URL
from src.app import application

application.config["SQLALCHEMY_DATABASE_URI"] = DB_URL
DB = SQLAlchemy(application)
