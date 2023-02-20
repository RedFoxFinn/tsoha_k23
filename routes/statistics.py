
from flask import render_template, session

from app import application
from tools import statistics_module as statistics


@application.route("/statistics")
def stats():
    localized = {
        "text": "Statistiikka"
    }
    localized_fields = {
        "chats": "keskusteluryhmiä",
        "topics": "aiheita",
        "moderators": "keskusteluryhmien ylläpitäjiä",
        "groups": "ryhmiä",
        "users": "käyttäjiä",
        "admins": "ylläpitäjiä",
        "requests": "toimenpidepyynnöt"
    }
    _user = session.get("username")
    _status = session.get("user_status")
    _stats = None
    if _user is not None and _status in ["ADMIN", "SUPER"]:
        _stats = statistics.get_statistics(statistics_coverage="FULL")
    elif _user is not None:
        _stats = statistics.get_statistics(statistics_coverage="BROAD")
    else:
        _stats = statistics.get_statistics(statistics_coverage="BASIC")
    _localized_stats = [(localized_fields[key], value)
                        for (key, value) in _stats]
    return render_template("statistics.html", local=localized, stats=_localized_stats)
