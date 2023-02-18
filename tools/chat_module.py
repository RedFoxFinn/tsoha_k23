
from database_module import DB

_chat_fetch_sql = "SELECT C.id AS id,C.cname AS name,C.link AS link,T.topic AS topic,G.gname AS group,G.restriction AS restriction FROM Chats C LEFT JOIN Topics T ON C.topic_id=T.id LEFT JOIN Groups G ON C.group_id=G.id"


def get_chats():
    _sql = _chat_fetch_sql.join('ORDER BY name ASC')
    _result = DB.session.execute(_sql)
    _data = _result.fetchall()
    return _data


def get_public_chats():
    _sql = _chat_fetch_sql.join('WHERE restriction="NONE" ORDER BY name ASC')
    _result = DB.session.execute(_sql)
    _data = _result.fetchall()
    return _data


def get_login_restricted_chats():
    _sql = _chat_fetch_sql.join('WHERE restriction="LOGIN" ORDER BY name ASC')
    _result = DB.session.execute(_sql)
    _data = _result.fetchall()
    return _data


def get_age_restricted_chats():
    _sql = _chat_fetch_sql.join('WHERE restriction="AGE" ORDER BY name ASC')
    _result = DB.session.execute(_sql)
    _data = _result.fetchall()
    return _data


def get_security_restricted_chats():
    _sql = _chat_fetch_sql.join('WHERE restriction="SEC" ORDER BY name ASC')
    _result = DB.session.execute(_sql)
    _data = _result.fetchall()
    return _data


def add_chat(chat_insert_data):
    _insert_sql = f"INSERT INTO Chats (cname,topic_id,group_id,link,moderator_ids) VALUES (:cname,:topic,:group,:link,:moderators)"
    try:
        DB.session.execute(_insert_sql, chat_insert_data)
        DB.session.commit()
        return True
    except:
        return False
