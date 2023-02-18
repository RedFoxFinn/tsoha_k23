
from tools.database_module import DB


def register_admin(uid: int, super: bool = False):
    _admin_insert_sql = f"INSERT INTO Admins (user_id, superuser) VALUES ({uid}, True)"
    try:
        DB.session.execute(_admin_insert_sql)
        DB.session.commit()
        return True
    except:
        return False

def check_admin(uid:int):
    _admin_check_sql = f"SELECT id, user_id, superuser FROM Admins WHERE user_id={uid}"
    _admin_check_result = DB.session.execute(_admin_check_sql)
    _admin_data = _admin_check_result.fetchone()
    return _admin_data
