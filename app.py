from datetime import date, datetime
from flask import Flask
from flask import abort, redirect, render_template, request, session, flash, make_response
from flask_sqlalchemy import SQLAlchemy

from modules.config_module import DB_URL, REG_CODE, SECRET_KEY, APP_NAME

from tools.validate_input import input_validation, validate_reg_or_log
from tools.password_tools import validate_password_on_login, validate_passwords_on_change, validate_password_on_register

application = Flask(__name__, template_folder="templates", static_folder='static')
application.config["SECRET_KEY"] = SECRET_KEY
application.config["SQLALCHEMY_DATABASE_URI"] = DB_URL
DB = SQLAlchemy(application)

@application.context_processor
def set_global_html_variables():
    template_config = {'app_name': APP_NAME}
    return template_config

@application.route("/", methods=["GET"])
def frontpage():
    sql = "SELECT count(*) FROM Users"
    result = DB.session.execute(sql)
    data = result.fetchall()[0]
    if data[0] == 0:
        flash("Aloitetaan sovelluksen alustaminen...","warning")
        return redirect("/init_site")
    else:
        localized = f"Tervetuloa sovellukseen {APP_NAME}"
        return render_template("index.html", text=localized)

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

@application.route("/login", methods=["GET"])
def login():
    sql = "SELECT count(*) FROM Users"
    result = DB.session.execute(sql)
    data = result.fetchall()[0]
    _user = session.get("username")
    if data[0] == 0:
        return redirect('/init_site')
    if _user != None:
        return redirect("/")
    else:
        localized = ["Kirjautuminen palveluun","Käyttäjänimi","Salasana","Kirjaudu"]
        return render_template("login.html",
          text=localized[0],
          username=localized[1],
          password=localized[2],
          submit=localized[3])

@application.route("/handle_login", methods=["POST"])
def handle_login():
    __fields = [request.form['uname'], request.form['password']]
    __field_validations = [
      1 if validate_reg_or_log(__fields[0], "USERNAME") else 0,
      1 if validate_reg_or_log(__fields[1], "PASSWORD") else 0
    ]
    if sum(__field_validations) == 2 and sum([1 if input_validation(f) else 0 for f in __fields]) == 0:
        login_data = {"un":__fields[0]}
        sql = f"SELECT id, uname, pw_hash FROM Users WHERE uname=:un"
        result = DB.session.execute(sql, login_data)
        data = result.fetchone()
        validation_result = validate_password_on_login(__fields[1], data[2])
        if validation_result:
            session["username"] = __fields[0]
            flash("Kirjautuminen onnistui!", "info")
            return redirect("/")
        else:
            flash("Tarkista tunnuksesi kirjoitusasu", "warning")
            return redirect("/login")
    else:
        flash("Virheellinen syöte yhdessä tai useammassa kentistä","error")
        return redirect("/login")

@application.route("/logout")
def logout():
    del session["username"]
    flash("Kirjauduit ulos palvelusta onnistuneesti")
    return redirect('/')

@application.route("/password")
def password():
    sql = "SELECT count(*) FROM Users"
    result = DB.session.execute(sql)
    data = result.fetchall()[0]
    if data[0] == 0:
        return redirect("/init_site")
    else:
        localized = ["Salasanan vaihtaminen","Käyttäjänimi","Salasana","Uusi salasana","Toista uusi salasana","Vaihda salasana"]
        return render_template("password_change.html",
          text=localized[0],
          username=localized[1],
          password=localized[2],
          new_password=localized[3],
          repeat_new_password=localized[4],
          submit=localized[3])

@application.route("/handle_password_change", methods=["POST"])
def handle_password_change():
    __fields = [request.form['uname'], request.form['password'], request.form['new_password'], request.form['new_password_repeat']]
    __field_validations = [
      1 if validate_reg_or_log(__fields[0], "USERNAME") else 0,
      1 if validate_reg_or_log(__fields[1], "PASSWORD") else 0,
      1 if validate_reg_or_log(__fields[2], "PASSWORD") else 0,
      1 if validate_reg_or_log(__fields[3], "PASSWORD") else 0
    ]
    __user_data_request = f"SELECT id, uname, pw_hash FROM Users WHERE uname=:un"
    __user_data_update = f"UPDATE Users SET pw_hash=:hash WHERE uname=:un"
    if sum(__field_validations) == 4 and sum([1 if input_validation(f) else 0 for f in __fields]) == 0:
        login_data = {"un":__fields[0]}
        user_result = DB.session.execute(__user_data_request, login_data)
        user_data = user_result.fetchone()
        validation_result = validate_passwords_on_change(
          __fields[1],
          user_data[2],
          __fields[2],
          __fields[3])
        if validation_result != None:
            new_data = {"un": user_data[1], "hash": validation_result}
            try:
                DB.session.execute(__user_data_update, new_data)
                DB.session.commit()
                flash("Salasanan vaihto onnistui", "info")
                return redirect("/login")
            except:
                return redirect("/password")
        else:
            flash("Tarkista kirjoittamasi kentät", "warning")
            return redirect("/password")
    else:
        flash("Virheellinen syöte yhdessä tai useammassa kentistä","error")
        return redirect("/password")

@application.route("/register")
def register():
    _user = session.get("username")
    if _user != None:
        return redirect("/")
    else:
        localized = ["Rekisteröityminen palveluun","Käyttäjänimi","Salasana","Toista salasana","Rekisteröitymistunnus","Rekisteröidy"]
        return render_template("registration.html",
          text=localized[0],
          username=localized[1],
          password=localized[2],
          repeat_password=localized[3],
          registration_code=localized[4],
          submit=localized[5])

@application.route("/handle_registration", methods=["POST"])
def handle_registration():
    __fields = [
      request.form["new_username"],
      request.form["new_password"],
      request.form["new_password_repeat"],
      request.form["registration_code"]
    ]
    __field_validations = [
      1 if validate_reg_or_log(__fields[0], "USERNAME") else 0,
      1 if validate_reg_or_log(__fields[1], "PASSWORD") else 0,
      1 if validate_reg_or_log(__fields[2], "PASSWORD") else 0
    ]
    if sum([1 if input_validation(f) else 0 for f in __fields]) == 0 and sum(__field_validations) == 3:
        validation = validate_password_on_register(__fields[1], __fields[2])
        __user_data_insert = "INSERT INTO Users (uname, pw_hash) VALUES (:un, :hash)"
        __user_data_request = "SELECT id, uname FROM Users WHERE uname=:un"
        if __fields[3] == REG_CODE:
            insert_data = {"un": __fields[0], "hash": validation}
            try:
                DB.session.execute(__user_data_insert, insert_data)
                DB.session.commit()
                flash("Rekisteröityminen onnistui", "info")
            except:
                flash("Käyttäjätunnus on jo käytössä", "warning")
                return redirect("/register")
        request_data = {"un": __fields[0]}
        user_result = DB.session.execute(__user_data_request, request_data)
        user_data = user_result.fetchone()
        if user_data[0] == 1:
            admin_data = {"uid": user_data[0]}
            __set_admin_sql = f"INSERT INTO Admins (user_id, superuser) VALUES (:uid, True)"
            DB.session.execute(__set_admin_sql, admin_data)
            DB.session.commit()
        return redirect("/login")
    else:
        flash("Virheellinen syöte yhdessä tai useammassa kentistä","error")
        return redirect("/register")

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