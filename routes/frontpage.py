
from flask import redirect, render_template, flash, session

from app import application
from tools import config_module as config,\
    user_module as users,\
    chat_module as chats


@application.route("/", methods=["GET"])
def frontpage():
    if users.count() == 0:
        flash("Aloitetaan sovelluksen alustaminen...", "warning")
        return redirect("/init_site")
    localized = f"Tervetuloa sovellukseen {config.APP_NAME}"
    headers = {
        "public": "Julkiset",
        "login": "Kirjautumalla",
        "admin": "Rajoitetut"
    }
    _chats = []
    _chats += chats.get_public_chats()
    if session.get("username") is not None and\
            session.get("user_status") in ["ADMIN", "SUPER"]:
        _chats += chats.get_login_restricted_chats()
        _chats += chats.get_age_restricted_chats()
        _chats += chats.get_security_restricted_chats()
    elif session.get("username") is not None:
        _chats += chats.get_login_restricted_chats()
        _chats += chats.get_age_restricted_chats()
    return render_template(
        "index.html",
        text=localized,
        header=headers,
        showable=_chats,
        management="False")
