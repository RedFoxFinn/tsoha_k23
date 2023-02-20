
from tools.database_module import DB as db


def _get_admin_count():
    sql = "SELECT count(*) FROM Admins"
    result = db.session.execute(sql)    # pylint: disable=no-member
    data = result.fetchall()[0]
    return ("admins", data[0])


def _get_chat_count():
    sql = "SELECT count(*) FROM Chats"
    result = db.session.execute(sql)    # pylint: disable=no-member
    data = result.fetchall()[0]
    return ("chats", data[0])


def _get_group_count():
    sql = "SELECT count(*) FROM Groups"
    result = db.session.execute(sql)    # pylint: disable=no-member
    data = result.fetchall()[0]
    return ("groups", data[0])


def _get_moderator_count():
    sql = "SELECT count(*) FROM Moderators"
    result = db.session.execute(sql)    # pylint: disable=no-member
    data = result.fetchall()[0]
    return ("moderators", data[0])


def _get_topic_count():
    sql = "SELECT count(*) FROM Topics"
    result = db.session.execute(sql)    # pylint: disable=no-member
    data = result.fetchall()[0]
    return ("topics", data[0])


def _get_user_count():
    sql = "SELECT count(*) FROM Users"
    result = db.session.execute(sql)    # pylint: disable=no-member
    data = result.fetchall()[0]
    return ("users", data[0])


def _get_request_count():
    sql = "SELECT count(*) FROM Requests"
    result = db.session.execute(sql)    # pylint: disable=no-member
    data = result.fetchall()[0]
    return ("requests", data[0])


def get_statistics(statistics_coverage: str):
    _packaged_statistics = []
    if statistics_coverage == 'BASIC':
        _packaged_statistics.append(_get_chat_count())
        _packaged_statistics.append(_get_topic_count())
    if statistics_coverage == 'BROAD':
        _packaged_statistics.append(_get_chat_count())
        _packaged_statistics.append(_get_topic_count())
        _packaged_statistics.append(_get_moderator_count())
        _packaged_statistics.append(_get_group_count())
        _packaged_statistics.append(_get_user_count())
    if statistics_coverage == 'FULL':
        _packaged_statistics.append(_get_chat_count())
        _packaged_statistics.append(_get_topic_count())
        _packaged_statistics.append(_get_moderator_count())
        _packaged_statistics.append(_get_group_count())
        _packaged_statistics.append(_get_user_count())
        _packaged_statistics.append(_get_admin_count())
        _packaged_statistics.append(_get_request_count())
    return _packaged_statistics
