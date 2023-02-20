
from tools.database_module import DB


def register_admin(uid: int, superuser: bool = False):
    _admin_insert_sql = f"INSERT INTO Admins (user_id, superuser) VALUES ({uid}, {superuser})"
    try:
        DB.session.execute(_admin_insert_sql)  # pylint: disable=no-member
        DB.session.commit() # pylint: disable=no-member
        return True
    except:     # pylint: disable=bare-except
        return False


def check_admin(uid: int):
    _admin_check_sql = f"SELECT id, user_id, superuser FROM Admins WHERE user_id={uid}"
    _admin_check_result = DB.session.execute(_admin_check_sql)   # pylint: disable=no-member
    _admin_data = _admin_check_result.fetchone()
    return _admin_data
