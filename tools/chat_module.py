"""
    chat_module.py

    application module for various database tasks related
    to database model 'Chat'

    intended use:
        'from tools import chat_module as chats'
        'chats.*function*' ie 'chats.count()'
"""
from tools.database_module import DB
from tools.user_module import USER_FETCH_SQL_LIMITED as USER_FETCH_SQL

CHAT_FETCH_SQL = "SELECT C.id AS id,\
    C.cname AS name,\
    C.link AS link,\
    T.topic AS topic,\
    G.gname AS group,\
    G.restriction AS restriction,\
    U.uname AS moderator,\
    U.dm_link AS dm \
    FROM Chats C LEFT JOIN Topics T ON C.topic_id=T.id \
    LEFT JOIN Groups G ON C.group_id=G.id \
    LEFT JOIN Users U ON C.moderator_id=U.id"

CHAT_STAISTICS_FETCH_SQL = "SELECT C.id AS id,\
    C.topic_id AS topic,\
    C.group_id AS group,\
    G.restriction AS restriction,\
    C.moderator_id AS moderator \
    FROM Chats C LEFT JOIN Groups G ON C.group_id=G.id"

MODERATOR_ID_FETCH_SQL = "SELECT DISTINCT moderator_id FROM Chats"


def get_chats():
    _sql = f"{CHAT_FETCH_SQL} ORDER BY name ASC"
    _result = DB.session.execute(_sql)  # pylint: disable=no-member
    _data = _result.fetchall()
    return _data


def get_public_chats():
    _sql = f"{CHAT_FETCH_SQL} WHERE restriction='NONE' ORDER BY name ASC"
    _result = DB.session.execute(_sql)  # pylint: disable=no-member
    _data = _result.fetchall()
    return _data


def get_login_restricted_chats():
    _sql = f"{CHAT_FETCH_SQL} WHERE restriction='LOGIN' ORDER BY name ASC"
    _result = DB.session.execute(_sql)  # pylint: disable=no-member
    _data = _result.fetchall()
    return _data


def get_age_restricted_chats():
    _sql = f"{CHAT_FETCH_SQL} WHERE restriction='AGE' ORDER BY name ASC"
    _result = DB.session.execute(_sql)  # pylint: disable=no-member
    _data = _result.fetchall()
    return _data


def get_security_restricted_chats():
    _sql = f"{CHAT_FETCH_SQL} WHERE restriction='SEC' ORDER BY name ASC"
    _result = DB.session.execute(_sql)  # pylint: disable=no-member
    _data = _result.fetchall()
    return _data


def get_chat_moderators():
    _sql = f"SELECT M.moderator_id AS id, U.uname AS handle, U.dm_link AS dm \
        FROM ({MODERATOR_ID_FETCH_SQL}) AS M \
        LEFT JOIN ({USER_FETCH_SQL}) AS U \
        ON M.moderator_id=U.id"
    _result = DB.session.execute(_sql)  # pylint: disable=no-member
    _data = _result.fetchall()
    return _data


def add_chat(chat_insert_data: dict):
    _insert_sql = "INSERT INTO Chats (cname,topic_id,group_id,link,moderator_id) \
        VALUES (:cname,:topic,:group,:link,:moderator)"
    try:
        DB.session.execute(
            _insert_sql, chat_insert_data)   # pylint: disable=no-member
        DB.session.commit()  # pylint: disable=no-member
        return True
    except:     # pylint: disable=bare-except
        return False


def update_chat(chat_update_data: dict):
    _sql = "Update Chats SET cname=:cname,\
        topic_id=:topic,\
        group_id=:group,\
        link=:link,\
        moderator_id=:moderator \
        WHERE id=:id"
    try:
        DB.session.execute(_sql, chat_update_data)  # pylint: disable=no-member
        DB.session.commit()  # pylint: disable=no-member
        return True
    except:  # pylint: disable=bare-except
        return False


def remove_chat(id_value: int):
    _sql = f"DELETE FROM Chats WHERE id={id_value}"
    try:
        DB.session.execute(_sql)    # pylint: disable=no-member
        DB.session.commit()  # pylint: disable=no-member
        return True
    except:  # pylint: disable=bare-except
        return False


def get_chat_by_id(id_value: int):
    _sql = f"{CHAT_FETCH_SQL} WHERE C.id={id_value}"
    _result = DB.session.execute(_sql)  # pylint: disable=no-member
    _data = _result.fetchone()
    return _data


def count():
    """
        module function to return number of entries in the database
        related to the model 'Chat'
    """
    _sql = "SELECT count(*) FROM Chats"
    _result = DB.session.execute(_sql)  # pylint: disable=no-member
    _data = _result.fetchall()[0]
    return _data[0]


def count_moderators():
    """
        module function to return number of distinct moderators
        set for the chats
    """
    _sql = f"SELECT count(*) FROM ({MODERATOR_ID_FETCH_SQL}) AS M"
    _result = DB.session.execute(_sql)  # pylint: disable=no-member
    _data = _result.fetchall()[0]
    return _data[0]


def count_by_restrictions():
    """
        module function to return number of chats with
        respective restriction defined by the group set for the chat
    """
    _sql = f"SELECT \
        GR.restriction,\
        (SELECT count(*) FROM ({CHAT_FETCH_SQL} WHERE restriction=GR.restriction) AS C) \
        FROM (SELECT DISTINCT restriction FROM Groups) AS GR"
    _result = DB.session.execute(_sql)    # pylint: disable=no-member
    _data = _result.fetchall()
    return _data


def average_chats_per_restriction():
    """
        module function to calculate average number of chats
        per restriction
    """
    _sql = f"SELECT \
        avg((SELECT count(*) FROM ({CHAT_FETCH_SQL} WHERE restriction=GR.restriction) AS C)) \
        FROM (SELECT DISTINCT restriction FROM Groups) AS GR"
    _result = DB.session.execute(_sql)  # pylint: disable=no-member
    _data = _result.fetchall()[0]
    return round(float(_data[0]), 1)
