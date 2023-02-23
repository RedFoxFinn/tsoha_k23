"""
    group_module.py

    application module for various database tasks related
    to database model 'Group'

    intended use:
        'from tools import group_module as groups'
        'groups.*function*' ie 'groups.count()'
"""
from tools.database_module import DB


def get_groups():
    """
        module function to return all groups in the database

        intended use:
            'from tools import group_module as groups'
            'groups.get_groups()'
    """
    _sql = "SELECT id,gname,restriction FROM Groups ORDER BY gname ASC"
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
    _sql = f"SELECT id,gname,restriction FROM Groups WHERE id={id_value}"
    _result = DB.session.execute(_sql)      # pylint: disable=no-member
    _data = _result.fetchone()
    return _data


def count():
    """
        module function to return number of groups added to the database

        intended use:
            'from tools import group_module as groups'
            'groups.count()'
    """
    _sql = "SELECT count(*) FROM Groups"
    _result = DB.session.execute(_sql)      # pylint: disable=no-member
    _data = _result.fetchall()[0]
    return _data[0]
