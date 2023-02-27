
from tools.database_module import DB

TOPIC_FETCH_SQL = "SELECT id,topic FROM Topics"

def get_topics():
    _sql = f"{TOPIC_FETCH_SQL} ORDER BY topic ASC"
    _result = DB.session.execute(_sql)  # pylint: disable=no-member
    _data = _result.fetchall()
    return _data


def add_topic(topic: str):
    _search_sql = f"{TOPIC_FETCH_SQL} WHERE topic='{topic}'"
    _search_result = DB.session.execute(_search_sql)    # pylint: disable=no-member
    _search_data = _search_result.fetchone()
    if _search_data is not None and len(_search_data) > 0:
        return _search_data[0]
    _insert_sql = f"INSERT INTO Topics (topic) VALUES ('{topic}')"
    DB.session.execute(_insert_sql)    # pylint: disable=no-member
    DB.session.commit() # pylint: disable=no-member
    _research_result = DB.session.execute(_search_sql)
    _research_data = _research_result.fetchone()
    return _research_data[0]


def get_topic(topic:str):
    _search_sql = f"{TOPIC_FETCH_SQL} WHERE id={int(topic)}"\
        if topic.isnumeric()\
        else f"{TOPIC_FETCH_SQL} WHERE topic='{topic}'"
    _search_result = DB.session.execute(_search_sql)    # pylint: disable=no-member
    _search_data = _search_result.fetchone()
    return _search_data


def count():
    """
        module function to return number of entries in the database
        related to the model 'Topic'
    """
    _sql = "SELECT count(*) FROM Topics"
    _result = DB.session.execute(_sql)  # pylint: disable=no-member
    _data = _result.fetchall()[0]
    return _data[0]
