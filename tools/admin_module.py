
from tools.database_module import DB

ADMIN_FETCH_SQL = "SELECT id, user_id FROM Admins"


def register_admin(uid: int):
    _admin_insert_sql = f"INSERT INTO Admins (user_id) VALUES ({uid})"
    try:
        DB.session.execute(_admin_insert_sql)  # pylint: disable=no-member
        DB.session.commit()  # pylint: disable=no-member
        return True
    except:     # pylint: disable=bare-except
        return False


def check_admin(uid: int):
    _admin_check_sql = f"{ADMIN_FETCH_SQL} WHERE user_id={uid}"
    _admin_check_result = DB.session.execute(
        _admin_check_sql)   # pylint: disable=no-member
    _admin_data = _admin_check_result.fetchone()
    return _admin_data


def check_admin_by_uname(uname: str):
    _sql = f"{ADMIN_FETCH_SQL} WHERE user_id=(SELECT id FROM Users WHERE uname='{uname}')"
    _result = DB.session.execute(_sql)  # pylint: disable=no-member
    _data = _result.fetchone()
    return _data


def count():
    """
        module function to return number of entries in the database
        related to the model 'Admin'
    """
    _sql = "SELECT count(*) FROM Admins"
    _result = DB.session.execute(_sql)  # pylint: disable=no-member
    _data = _result.fetchall()[0]
    return _data[0]
