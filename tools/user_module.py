"""
    user_module.py

    application module for various database tasks related
    to database model 'User'

    intended use:
        'from tools import user_module as users'
        'users.*function*' ie 'users.count()'
"""
from tools.database_module import DB

USER_FETCH_SQL_LIMITED = "SELECT id,uname FROM Users"
USER_FETCH_SQL_FULL = "SELECT id,uname,pw_hash FROM Users"

def register(new_username: str, new_password_hash: str):
    """
        module function for registering new user
        to the application and add them to the database

        intended use:
            'from tools import user_module as users'
            'users.register(*new_username*,*new_password_hash*)'
                where the password hash has already been generated in password_tools
    """
    _user_data_insert = "INSERT INTO Users (uname, pw_hash) VALUES (:un, :hash)"
    _user_data_request = f"{USER_FETCH_SQL_LIMITED} WHERE uname=:un"
    _insert_data = {"un": new_username, "hash": new_password_hash}
    _request_data = {"un": new_username}
    try:
        DB.session.execute(_user_data_insert, _insert_data) # pylint: disable=no-member
        DB.session.commit() # pylint: disable=no-member
        _user_result = DB.session.execute(_user_data_request, _request_data)    # pylint: disable=no-member
        _user_data = _user_result.fetchone()
        return _user_data
    except:     # pylint: disable=bare-except
        return None


def count():
    """
        module function to return number of registered users added to the database

        intended use:
            'from tools import user_module as users'
            'users.count()'
    """
    _sql = "SELECT count(*) FROM Users"
    _result = DB.session.execute(_sql)  # pylint: disable=no-member
    _data = _result.fetchall()[0]
    return _data[0]


def user_by_id(id_value: int, full_mode:bool=False):
    """
        module function to return user data of a registered user from database

        intended use:
            'from tools import user_module as users'
            'users.user_data(*uname*)'
                where uname is the username to search from database
    """
    _sql = f"{USER_FETCH_SQL_FULL if full_mode else USER_FETCH_SQL_LIMITED} FROM Users WHERE id={id_value}"
    _result = DB.session.execute(_sql)  # pylint: disable=no-member
    _data = _result.fetchone()
    return _data


def user_by_uname(uname: str, full_mode:bool=False):
    """
        module function to return user data of a registered user from database

        intended use:
            'from tools import user_module as users'
            'users.user_data(*uname*)'
                where uname is the username to search from database
    """
    _sql = f"{USER_FETCH_SQL_FULL if full_mode else USER_FETCH_SQL_LIMITED} FROM Users WHERE uname='{uname}'"
    _result = DB.session.execute(_sql)  # pylint: disable=no-member
    _data = _result.fetchone()
    return _data
