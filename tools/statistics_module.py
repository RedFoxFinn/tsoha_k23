
from tools.database_module import DB as db
from tools import\
    admin_module as admins,\
    chat_module as chats,\
    group_module as groups,\
    moderator_module as moderators,\
    topics_module as topics,\
    user_module as users


def _get_admin_count():
    _data = admins.count()
    return ("admins", _data)


def _get_chat_count():
    _data = chats.count()
    return ("chats", _data)


def _get_group_count():
    _data = groups.count()
    return ("groups", _data)


def _get_moderator_count():
    _data = moderators.count()
    return ("moderators", _data)


def _get_topic_count():
    _data = topics.count()
    return ("topics", _data)


def _get_user_count():
    _data = users.count()
    return ("users", _data)


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
