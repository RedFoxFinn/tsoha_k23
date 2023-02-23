"""
    moderator_module.py

    application module for various database tasks related
    to database model 'Moderator'

    intended use:
        'from tools import moderator_module as moderators'
        'moderators.*function*' ie 'moderators.count()'
"""
from tools.database_module import DB

MODERATOR_FETCH_SQL_LIMITED = "SELECT id,handle FROM Moderators"
MODERATOR_FETCH_SQL_FULL = "SELECT id,handle,chat_links FROM Moderators"


def add_moderator(handle_value:str,link_value:str):
    _moderator = get_moderator_by_handle(handle_value)
    if _moderator is None:
        _sql = "INSERT INTO Moderators (handle,chat_links) VALUES (:handle,:chat_links)"
        _insert_data = {"handle":handle_value,"chat_links":[link_value]}
        try:
            DB.session.execute(_sql, _insert_data) # pylint: disable=no-member
            DB.session.commit() # pylint: disable=no-member
            return 'ADDED'
        except:   # pylint: disable=bare-except
            return 'ADD - FAILED'
    _update_sql = "UPDATE Moderators SET chat_links=:chat_links WHERE id=:mid"
    _update_data = {"chat_links": _moderator[2]+[link_value],"mid":_moderator[0]}
    try:
        DB.session.execute(_update_sql,_update_data)    # pylint: disable=no-member
        DB.session.commit() # pylint: disable=no-member
        return 'UPDATED'
    except:
        return 'UPDATE - FAILED'


def get_moderator_by_handle(handle_value:str,full_mode:bool=False):
    _sql = f"{MODERATOR_FETCH_SQL_FULL if full_mode else MODERATOR_FETCH_SQL_LIMITED} WHERE handle=:handle"
    _query_data = {"handle":handle_value}
    _result = DB.session.execute(_sql,_query_data)
    _data = _result.fetchone()
    return _data


def get_moderators(full_mode:bool=False):
    """
        module function to fetch all entries on database
        related to the model 'Moderator'
    """
    _sql = f"{MODERATOR_FETCH_SQL_FULL if full_mode else MODERATOR_FETCH_SQL_LIMITED} ORDER BY handle ASC"
    _result = DB.session.execute(_sql)  # pylint: disable=no-member
    _data = _result.fetchall()
    return _data


def count():
    """
        module function to return number of entries in the database
        related to the model 'Moderator'
    """
    _sql = "SELECT count(*) FROM Moderators"
    _result = DB.session.execute(_sql)  # pylint: disable=no-member
    _data = _result.fetchall()[0]
    return _data[0]