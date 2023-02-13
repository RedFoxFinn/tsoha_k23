from os import getenv

DB_URL = str(getenv("DATABASE_URL"))
REG_CODE = str(getenv("USER_REGISTRATION_CODE"))
SECRET_KEY = str(getenv("SECRET_KEY"))
APP_NAME = str(getenv("CUSTOM_APP_NAME")) if getenv("CUSTOM_APP_NAME") != None or len(getenv("CUSTOM_APP_NAME")) == 0 else "ChatList"