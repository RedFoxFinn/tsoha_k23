
from database_module import DB


def get_groups():
    _sql = "SELECT id,gname,restriction FROM Groups"
    _result = DB.session.execute(_sql)
    _data = _result.fetchall()
    return _data


def get_group_by_id(id: int):
    _sql = f"SELECT id,gname,restriction FROM Groups WHERE id={id}"
    _result = DB.session.execute(_sql)
    _data = _result.fetchone()
    return _data
