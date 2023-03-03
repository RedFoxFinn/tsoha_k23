
from tools.database_module import DB

ADMIN_FETCH_SQL = "SELECT id, user_id FROM Admins"


def _register_admin(id_value: int):
    _admin_insert_sql = f"INSERT INTO Admins (user_id) VALUES ({id_value})"
    try:
        DB.session.execute(_admin_insert_sql)  # pylint: disable=no-member
        DB.session.commit()  # pylint: disable=no-member
        return True
    except:     # pylint: disable=bare-except
        return False


def _cancel_admin_status(id_value: int, admin_id: int):
    _admin_delete_sql = f"DELETE FROM Admins WHERE id={id_value}"
    _admin_ownership_transfer_sql = f"UPDATE Groups \
        SET admin_id={admin_id} \
        WHERE admin_id={id_value}"
    try:
        DB.session.execute(_admin_delete_sql)   # pylint: disable=no-member
        DB.session.commit()  # pylint: disable=no-member
    except:  # pylint: disable=bare-except
        return None
    try:
        DB.session.execute(
            _admin_ownership_transfer_sql)   # pylint: disable=no-member
        DB.session.commit()  # pylint: disable=no-member
        return True
    except:  # pylint: disable=bare-except
        return False


def change_admin_status(uid: int, admin_id: int):
    _sql = f"{ADMIN_FETCH_SQL} WHERE user_id={uid}"
    _result = DB.session.execute(_sql)  # pylint: disable=no-member
    _data = _result.fetchone()
    if _data is None:
        _outcome = _register_admin(uid)
        return ('REGISTER', _outcome)
    _outcome = _cancel_admin_status(_data[0], admin_id)
    return ('CANCEL', _outcome)


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
