
from tools.database_module import DB


def get_topics():
    _sql = "SELECT id,topic FROM Topics"
    _result = DB.session.execute(_sql)  # pylint: disable=no-member
    _data = _result.fetchall()
    return _data


def add_topic(topic: str):
    _search_sql = f"SELECT id FROM Topics WHERE topic='{topic}'"
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
