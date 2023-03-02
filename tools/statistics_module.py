
from tools import\
    admin_module as admins,\
    chat_module as chats,\
    group_module as groups,\
    topics_module as topics,\
    user_module as users


def _get_admin_count():
    _data = admins.count()
    return ("admins", _data)


def _get_chat_count():
    _data = chats.count()
    return ("chats", _data)


def _get_chat_count_by_restriction():
    _data = chats.count_by_restrictions()
    return ("restriction_chats", _data)


def _get_average_chat_count_per_restriction():
    _data = chats.average_chats_per_restriction()
    return ("average_chats", _data)


def _get_group_count():
    _data = groups.count()
    return ("groups", _data)


def _get_topic_count():
    _data = topics.count()
    return ("topics", _data)


def _get_user_count():
    _data = users.count()
    return ("users", _data)


def _get_moderator_count():
    _data = chats.count_moderators()
    return ("moderators", _data)


def get_statistics(logged: bool = False, full_coverage: bool = False):
    _packaged_statistics = []
    _packaged_statistics.append(_get_chat_count())
    _packaged_statistics.append(_get_topic_count())
    if logged:
        _packaged_statistics.append(_get_group_count())
        _packaged_statistics.append(_get_moderator_count())
        _packaged_statistics.append(_get_average_chat_count_per_restriction())
        if full_coverage:
            _packaged_statistics.append(_get_user_count())
            _packaged_statistics.append(_get_admin_count())
            _packaged_statistics.append(_get_chat_count_by_restriction())
    return _packaged_statistics
