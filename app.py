from flask import Flask
from flask import abort, redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy

from modules.config_module import DB_URL, REG_CODE

from tools.password_tools import validate_password_on_login, validate_passwords_on_change, validate_password_on_register

application = Flask(__name__)
application.config["SQLALCHEMY_DATABASE_URI"] = DB_URL
DB = SQLAlchemy(application)

@application.route("/")
def frontpage():
    localized = "Tervetuloa käyttämään ChatListiä"
    return render_template("index.html", message=localized)

@application.route("/init_site")
def init_site():
    localized = ["Tervetuloa käyttämään ChatListiä", "Aloita alustan käyttöönotto määrittämällä ylläpitäjä", "Aloita määritys"]
    return render_template("initialization.html", message=localized[0], notice=localized[1], submit=localized[2])

@application.route("/login")
def login():
    localized = ["Kirjautuminen palveluun","Käyttäjänimi","Salasana","Kirjaudu"]
    return render_template("login.html",
      message=localized[0],
      username=localized[1],
      password=localized[2],
      submit=localized[3])

@application.route("/handle_login", methods=["POST"])
def handle_login():
    login_data = {"un":request.form["uname"]}
    sql = f"SELECT id, uname, pw_hash FROM Users WHERE uname=:un"
    result = DB.session.execute(sql, login_data)
    data = result.fetchone()
    validation_result = validate_password_on_login(request.form["password"], data[2])
    return redirect("/") if validation_result else redirect("/login")

@application.route("/password")
def password():
    localized = ["Salasanan vaihtaminen","Käyttäjänimi","Salasana","Uusi salasana","Toista uusi salasana","Vaihda salasana"]
    return render_template("password_change.html",
      message=localized[0],
      username=localized[1],
      password=localized[2],
      new_password=localized[3],
      repeat_new_password=localized[4],
      submit=localized[3])

@application.route("/handle_password_change", methods=["POST"])
def handle_password_change():
    __user_data_request = f"SELECT id, uname, pw_hash FROM Users WHERE uname=:un"
    __user_data_update = f"UPDATE Users SET pw_hash=:hash WHERE uname=:un"
    login_data = {"un":request.form["uname"]}
    user_result = DB.session.execute(__user_data_request, login_data)
    user_data = user_result.fetchone()
    validation_result = validate_passwords_on_change(
      login_data["password"],
      user_data[2],
      request.form["new_password"],
      request.form["new_password_repeat"])
    if validation_result != None:
        new_data = {"un": user_data[1], "hash": validation_result}
        try:
            DB.session.execute(__user_data_update, new_data)
            return redirect("/login")
        except:
            return redirect("/password")
    else:
        return redirect("/password")

@application.route("/register")
def register():
    localized = ["Rekisteröityminen palveluun","Käyttäjänimi","Salasana","Toista salasana","Rekisteröitymistunnus","Rekisteröidy"]
    return render_template("registration.html",
      message=localized[0],
      username=localized[1],
      password=localized[2],
      repeat_password=localized[3],
      registration_code=localized[4],
      submit=localized[5])

@application.route("/handle_registration", methods=["POST"])
def handle_registration():
    form_data = [
      request.form["new_username"],
      request.form["new_password"],
      request.form["new_password_repeat"],
      request.form["registration_code"]
    ]
    validation = validate_password_on_register(form_data[1], form_data[2])
    __user_data_insert = "INSERT INTO Users (uname, pw_hash) VALUES (:un, :hash)"
    __user_data_request = "SELECT id, uname FROM Users WHERE uname=:un"
    if form_data[3] == REG_CODE:
        insert_data = {"un": form_data[0], "hash": validation}
        try:
            DB.session.execute(__user_data_insert, insert_data)
            DB.session.commit()
        except:
            return redirect("/register")
    request_data = {"un": form_data[0]}
    user_result = DB.session.execute(__user_data_request, request_data)
    user_data = user_result.fetchone()
    if user_data[0] == 1:
        admin_data = {"uid": user_data[0]}
        __set_admin_sql = f"INSERT INTO Admins (user_id, superuser) VALUES (:uid, True)"
        DB.session.execute(__set_admin_sql, admin_data)
        DB.session.commit()
    return redirect("/login")

@application.route("/management")
def show():
    return "Management will be here"

@application.route("/management/groups")
def manage_groups():
    return "Group management"

@application.route("/management/groups/<int:id>")
def manage_group(id:int):
    return f"Managing group with id {id}"

@application.route("/management/chats")
def manage_chats():
    return "Chat management"

@application.route("/management/chats/<int:id>")
def manage_chat(id:int):
    return f"Managing chat with id {id}"

@application.route("/management/admins")
def manage_admins():
    return "Admin management"