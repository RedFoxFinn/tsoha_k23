"""
    config_module.py

    applications configuration provider module

    provides all essential configuration options for application to use
"""
from os import getenv

DB_URL = str(getenv("DATABASE_URL"))
REG_CODE = str(getenv("USER_REGISTRATION_CODE"))
SECRET_KEY = str(getenv("SECRET_KEY"))
APP_NAME = str(getenv("CUSTOM_APP_NAME"))\
    if getenv("CUSTOM_APP_NAME") is None\
    or len(getenv("CUSTOM_APP_NAME")) == 0 else "ChatList"
PW_RESET = str(getenv("PW_RESET_PLACEHOLDER_VALUE"))
