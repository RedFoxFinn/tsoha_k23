"""
    chat_module.py

    application module for various database tasks related
    to database model 'Chat'

    intended use:
        'from tools import chat_module as chats'
        'chats.*function*' ie 'chats.count()'
"""
from tools.database_module import DB

CHAT_FETCH_SQL = "SELECT C.id AS id,\
                        C.cname AS name,\
                        C.link AS link,\
                        T.topic AS topic,\
                        G.gname AS group,\
                        G.restriction AS restriction \
                        FROM Chats C LEFT JOIN Topics T ON C.topic_id=T.id \
                        LEFT JOIN Groups G ON C.group_id=G.id"


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


def add_chat(chat_insert_data):
    _insert_sql = "INSERT INTO Chats (cname,topic_id,group_id,link,moderator_ids) \
        VALUES (:cname,:topic,:group,:link,:moderators)"
    try:
        DB.session.execute(_insert_sql, chat_insert_data)   # pylint: disable=no-member
        DB.session.commit() # pylint: disable=no-member
        return True
    except:     # pylint: disable=bare-except
        return False


def count():
    """
        module function to return number of entries in the database
        related to the model 'Chat'
    """
    _sql = "SELECT count(*) FROM Chats"
    _result = DB.session.execute(_sql)  # pylint: disable=no-member
    _data = _result.fetchall()[0]
    return _data[0]
