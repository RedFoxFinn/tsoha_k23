
from flask import redirect, render_template

from modules import config_module as config, database_module as database
from src.app import application


@application.route("/init_site")
def init_site():
    sql = "SELECT count(*) FROM Users"
    result = database.DB.session.execute(sql)
    data = result.fetchall()[0]
    if data[0] == 0:
        localized = [f"Tervetuloa sovellukseen {config.APP_NAME}",
                     "Aloita alustan käyttöönotto määrittämällä ylläpitäjä", "Aloita määritys"]
        return render_template("initialization.html", text=localized[0], notice=localized[1], submit=localized[2])
    return redirect('/login')
