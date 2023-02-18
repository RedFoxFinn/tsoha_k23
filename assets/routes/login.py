
import secrets
from flask import redirect, render_template, request, session, flash

from app import application
from modules import user_module as users,\
    admin_module as admins
from tools import validate_input as validators,\
    password_tools as passwords


@application.route("/login", methods=["GET"])
def login():
    if users.count() == 0:
        return redirect('/init_site')
    _user = session.get("username")
    if _user is not None:
        return redirect("/")
    localized = ["Kirjautuminen palveluun",
                 "Käyttäjänimi", "Salasana", "Kirjaudu"]
    return render_template("login.html",
                           text=localized[0],
                           username=localized[1],
                           password=localized[2],
                           submit=localized[3])


@application.route("/handle_login", methods=["POST"])
def handle_login():
    __fields = [request.form['uname'], request.form['password']]
    __field_validations = [
        1 if validators.validate_reg_or_log(__fields[0], "USERNAME") else 0,
        1 if validators.validate_reg_or_log(__fields[1], "PASSWORD") else 0
    ]
    if sum(__field_validations) == 2 and\
            (1 if validators.input_validation(f) else 0 for f in __fields) == 0:
        _user_data = users.user_data(__fields[0])
        validation_result = passwords.validate_password_on_login(
            __fields[1], _user_data[2])
        _admin_data = admins.check_admin(_user_data[0])
        if validation_result:
            session["username"] = _user_data[1]
            session["csrf_token"] = secrets.token_hex(16)
            session["user_status"] = "SUPER" if _admin_data[2] else\
                "ADMIN" if _admin_data is not None else "USER"
            flash("Kirjautuminen onnistui!", "success")
            return redirect("/")
        flash("Tarkista tunnuksesi kirjoitusasu", "warning")
        return redirect("/login")
    flash("Virheellinen syöte yhdessä tai useammassa kentistä", "error")
    return redirect("/login")


@application.route("/logout")
def logout():
    del session["username"]
    del session["user_status"]
    del session["csrf_token"]
    flash("Kirjauduit ulos palvelusta onnistuneesti", "success")
    return redirect('/')
