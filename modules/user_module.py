
from modules.database_module import DB

def register(new_username:str, new_password_hash:str):
    _user_data_insert = "INSERT INTO Users (uname, pw_hash) VALUES (:un, :hash)"
    _user_data_request = "SELECT id, uname FROM Users WHERE uname=:un"
    _insert_data = {"un": new_username, "hash": new_password_hash}
    _request_data = {"un": new_username}
    try:
        DB.session.execute(_user_data_insert, _insert_data)
        DB.session.commit()
        _user_result = DB.session.execute(_user_data_request, _request_data)
        _user_data = _user_result.fetchone()
        return _user_data
    except:
        return None

def count():
    _sql = "SELECT count(*) FROM Users"
    _result = DB.session.execute(_sql)
    _data = _result.fetchall()[0]
    return _data[0]

def user_data(uname:str):
    _sql = f"SELECT id, uname, pw_hash FROM Users WHERE uname='{uname}'"
    _result = DB.session.execute(_sql)
    _data = _result.fetchone()
    return _data