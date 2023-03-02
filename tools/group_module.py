"""
    group_module.py

    application module for various database tasks related
    to database model 'Group'

    intended use:
        'from tools import group_module as groups'
        'groups.*function*' ie 'groups.count()'
"""
from tools.database_module import DB

GROUP_FETCH_SQL = "SELECT id,gname,restriction FROM Groups"


def get_groups():
    """
        module function to return all groups in the database

        intended use:
            'from tools import group_module as groups'
            'groups.get_groups()'
    """
    _sql = f"{GROUP_FETCH_SQL} ORDER BY gname ASC"
    _result = DB.session.execute(_sql)      # pylint: disable=no-member
    _data = _result.fetchall()
    return _data


def get_group_by_id(id_value: int):
    """
        module function to return group data of a group in database

        intended use:
            'from tools import group_module as groups'
            'groups.get_group_by_id(*id_value*)'
                where id_value is the id of a group in the database
    """
    _sql = f"{GROUP_FETCH_SQL} WHERE id={id_value} ORDER BY gname ASC"
    _result = DB.session.execute(_sql)      # pylint: disable=no-member
    _data = _result.fetchone()
    return _data


def add_group(gname: str, restriction: str, admin_id: int):
    """
        module function to add new group to the database for the application
    """
    _sql = "INSERT INTO Groups (gname,restriction,admin_id) VALUES (:gname,:restriction,:admin_id)"
    _input_data = {
        "gname": gname,
        "restriction": restriction,
        "admin_id": admin_id
    }
    try:
        DB.session.execute(_sql, _input_data)    # pylint: disable=no-member
        DB.session.commit()  # pylint: disable=no-member
        return True
    except:  # pylint: disable=bare-except
        return False


def update_group(id_value: int, gname: str, restriction: str):
    _sql = "UPDATE Groups SET gname=:gname, restriction=:restriction WHERE id=:id"
    _update_data = {
        "id": id_value,
        "gname": gname,
        "restriction": restriction
    }
    try:
        DB.session.execute(_sql, _update_data)    # pylint: disable=no-member
        DB.session.commit()  # pylint: disable=no-member
        return True
    except:  # pylint: disable=bare-except
        return False


def count():
    """
        module function to return number of entries in the database
        related to the model 'Group'

        intended use:
            'from tools import group_module as groups'
            'groups.count()'
    """
    _sql = "SELECT count(*) FROM Groups"
    _result = DB.session.execute(_sql)      # pylint: disable=no-member
    _data = _result.fetchall()[0]
    return _data[0]
