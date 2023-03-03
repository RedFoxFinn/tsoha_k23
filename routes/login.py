"""
    routes/login.py

    module for routing to applications login page, logout & login handling
"""
import secrets
from flask import redirect, render_template, request, session, flash

from app import application
from tools import user_module as users,\
    admin_module as admins,\
    validate_input as validators,\
    password_tools as passwords
from tools.config_module import PW_RESET


@application.route("/login", methods=["GET"])
def login():
    """
        module function responsible for routing to
        applications login page
    """
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
    """
        module function responsible for routing the
        applications login on submitting login form
    """
    _input = {
        "uname": request.form['uname'],
        "pw": request.form['password']
    }
    __field_validations = [
        1 if validators.validate_reg_or_log(
            _input["uname"], "USERNAME") else 0,
        1 if validators.validate_reg_or_log(_input["pw"], "PASSWORD") else 0
    ]
    __input_validations = [
        1 if validators.input_validation(_input["uname"]) else 0,
        1 if validators.input_validation(_input["pw"]) else 0
    ]
    if sum(__field_validations) < 2 and sum(__input_validations) < 2:
        flash("Virheellinen syöte yhdessä tai useammassa kentistä. \
        Tarkista tiedot.", "error")
        return redirect("/login")
    _user_data = users.user_by_uname(_input["uname"], full_mode=True)
    if _user_data[3] == PW_RESET or \
            (_input["pw"] == "RESET_MY_PASSWORD" and _user_data[3] == PW_RESET):
        session["reset_for"] = _input["uname"]
        flash("Salasana nollattu, aseta uusi", "info")
        return redirect("/reset")
    validation_result = passwords.validate_password_on_login(
        _input["pw"], _user_data[3])
    _admin_data = admins.check_admin(_user_data[0])
    if validation_result:
        session["username"] = _user_data[1]
        session["csrf_token"] = secrets.token_hex(16)
        session["user_status"] = "ADMIN" if _admin_data else "USER"
        flash("Kirjautuminen onnistui!", "success")
        return redirect("/")
    flash("Tarkista tunnuksesi kirjoitusasu", "warning")
    return redirect("/login")


@application.route("/logout")
def logout():
    """
        module function responsible for logging out user on logout
    """
    del session["username"]
    del session["user_status"]
    del session["csrf_token"]
    flash("Kirjauduit ulos palvelusta onnistuneesti", "success")
    return redirect('/')
