"""
    routes/init_page.py

    module for routing to applications initialization page
"""
from flask import redirect, render_template

from tools import config_module as config, user_module as users
from app import application


@application.route("/init_site")
def init_site():
    """
        module function responsible for routing to applications
        initialization page
    """
    data = users.count()
    if data == 0:
        localized = [f"Tervetuloa sovellukseen {config.APP_NAME}",
                     "Aloita alustan käyttöönotto määrittämällä ylläpitäjä", "Aloita määritys"]
        return render_template(
            "initialization.html",
            text=localized[0],
            notice=localized[1],
            submit=localized[2])
    return redirect('/login')
