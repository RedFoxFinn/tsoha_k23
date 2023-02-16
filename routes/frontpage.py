
from flask import redirect, render_template, flash, session

from modules.config_module import APP_NAME
from app import application
import modules.user_module as users
import modules.chat_module as chats

@application.route("/", methods=["GET"])
def frontpage():
    if users.count() == 0:
        flash("Aloitetaan sovelluksen alustaminen...","warning")
        return redirect("/init_site")
    else:
        localized = f"Tervetuloa sovellukseen {APP_NAME}"
        headers = {
          "public": "Julkiset",
          "login": "Kirjautumalla",
          "admin": "Rajoitetut"
        }
        _chats = []
        _chats += chats.get_public_chats()
        if session.get("username") != None:
            _chats += chats.get_login_restricted_chats()
            _age = chats.get_age_restricted_chats()
        if session.get("username") != None and session.get("user_status") in ["ADMIN","SUPER"]:
            _chats += chats.get_security_restricted_chats()
        return render_template("index.html", text=localized, header=headers, showable=_chats, management="False")