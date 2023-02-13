from os import getenv

DB_URL = str(getenv("DATABASE_URL"))
REG_CODE = str(getenv("USER_REGISTRATION_CODE"))
SECRET_KEY = str(getenv("SECRET_KEY"))