
from flask import redirect, render_template

from modules.config_module import APP_NAME
from app import application
from modules.database_module import DB

@application.route("/init_site")
def init_site():
    sql = "SELECT count(*) FROM Users"
    result = DB.session.execute(sql)
    data = result.fetchall()[0]
    if data[0] == 0:
        localized = [f"Tervetuloa sovellukseen {APP_NAME}", "Aloita alustan käyttöönotto määrittämällä ylläpitäjä", "Aloita määritys"]
        return render_template("initialization.html", text=localized[0], notice=localized[1], submit=localized[2])
    else:
        return redirect('/login')