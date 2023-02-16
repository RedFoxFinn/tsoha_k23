
from modules.database_module import DB
from tools import data_filter

_chat_fetch_sql = "SELECT C.id AS id,C.cname AS name,C.link AS link,T.topic AS topic,G.gname AS group,G.restriction AS restriction FROM Chats C LEFT JOIN Topics T ON C.topic_id=T.id LEFT JOIN Groups G ON C.group_id=G.id ORDER BY name ASC"

def get_chats():
    _result = DB.session.execute(_chat_fetch_sql)
    _data = _result.fetchall()
    return _data

def get_public_chats():
    _data = get_chats()
    _filtered = data_filter.filter_chats(_data, "PUBLIC")
    return _filtered

def get_login_restricted_chats():
    _data = get_chats()
    _filtered = data_filter.filter_chats(_data, "LOGIN")
    return _filtered

def get_age_restricted_chats():
    _data = get_chats()
    _filtered = data_filter.filter_chats(_data, "AGE")
    return _filtered

def get_security_restricted_chats():
    _data = get_chats()
    _filtered = data_filter.filter_chats(_data, "SECURITY")
    return _filtered

def add_chat(chat_insert_data):
    _insert_sql = f"INSERT INTO Chats (cname,topic_id,group_id,link,moderator_ids) VALUES (:cname,:topic,:group,:link,:moderators)"
    try:
        DB.session.execute(_insert_sql, chat_insert_data)
        DB.session.commit()
        return True
    except:
        return False