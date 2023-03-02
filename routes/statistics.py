
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
        "restriction_chats": "keskusteluryhmiä rajoitustasoittain",
        "NONE": "julkinen",
        "AGE": "ikärajoitettu",
        "LOGIN": "kirjautuminen",
        "SEC": "turvaluokitettu",
        "average_chats": "keskusteluryhmiä rajoitustasoilla keskimäärin",
        "topics": "aiheita",
        "moderators": "keskusteluryhmien ylläpitäjiä",
        "groups": "ryhmiä",
        "users": "käyttäjiä",
        "admins": "ylläpitäjiä"
    }
    _user = session.get("username")
    _status = session.get("user_status")
    _stats = None
    if _user is not None and _status == "ADMIN":
        _stats = statistics.get_statistics(logged=True, full_coverage=True)
    elif _user is not None:
        _stats = statistics.get_statistics(logged=True)
    else:
        _stats = statistics.get_statistics(logged=False)
    _localized_stats = [
        (
            localized_fields[key],
            value 
                if type(value) in [int,float]
                else [(localized_fields[val[0]],val[1]) for val in value]
        ) for (key, value) in _stats]
    _sorted_localized = sorted(_localized_stats, key= lambda value: value[0])
    return render_template("statistics.html", local=localized, stats=_sorted_localized)
