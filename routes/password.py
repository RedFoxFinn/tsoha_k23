
from flask import abort, redirect, render_template, request, session, flash

from app import application
from tools.database_module import DB
from tools.validate_input import input_validation, validate_reg_or_log
from tools.password_tools import validate_passwords_on_change, validate_password_on_register
import tools.user_module as users
import tools.validate_input as validators


@application.route("/reset")
def reset_user_password():
    _user = session.get("username")
    if _user is not None:
        del session["username"]
    if session.get("reset_for") is None:
        flash("Siirrytään kirjautumiseen.", "info")
        return redirect("/login")
    localized = {
        "text": "Salasanan asettaminen",
        "new_pw1": "Uusi salasana",
        "new_pw2": "Toista uusi salasana",
        "submit": "Aseta salasana",
        "tip_header": "Ohjeet salasanan asettamiseen",
        "tip_password": "Salasanan pituus 8-32 merkkiä",
        "tip_characters": "Sallittuja merkkejä",
        "tip_letters": "Kirjaimet a-z sekä A-Z",
        "tip_numbers": "Numerot 0-9",
        "tip_special": "Sallitut erikoismerkit . $ € £ _ - + @",
        "tip_pw": "8-32 merkkiä"
    }
    return render_template(
        "password_reset.html",
        local=localized
    )


@application.route("/handle_password_set", methods=["POST"])
def handle_password_set():
    _user = session.get("username")
    if _user is not None:
        flash("Siirrytään etusivulle.", "info")
        return redirect("/")
    if session.get("reset_for") is None:
        flash("Siirrytään kirjautumiseen.", "info")
        return redirect("/login")
    _fields = {
        "password1": request.form["new_password"],
        "password2": request.form["new_password_repeat"],
        "uname": request.form["username"]
    }
    __field_validations = [
        1 if validators.validate_reg_or_log(
            _fields["uname"], "USERNAME") else 0,
        1 if validators.validate_reg_or_log(
            _fields["password1"], "PASSWORD") else 0,
        1 if validators.validate_reg_or_log(
            _fields["password2"], "PASSWORD") else 0
    ]
    __input_validations = [
        1 if validators.input_validation(_fields["uname"]) else 0,
        1 if validators.input_validation(_fields["password1"]) else 0,
        1 if validators.input_validation(_fields["password2"]) else 0
    ]
    if sum(__field_validations) < 2 and sum(__input_validations) < 2:
        session["retry_form_values"] = _fields
        flash("Virheellinen syöte yhdessä tai useammassa kentistä. \
        Tarkista tiedot.", "error")
        return redirect("/reset")
    _pw_validation = validate_password_on_register(
        _fields["password1"], _fields["password2"])
    if _pw_validation is None:
        session["retry_form_values"] = _fields
        flash("Salasanasi eivät vastaa toisiaan. \
            Tarkista tietojesi oikeellisuus.", "warning")
        return redirect("/reset")
    _user_data = users.user_by_uname(_fields["uname"])
    _result = users.set_new_password(_user_data[0], _pw_validation)
    if _result:
        _retry_values = session.get("retry_form_values")
        if _retry_values is not None:
            del session["retry_form_values"]
        del session["reset_for"]
        flash("Salasanan asettaminen onnistui!", "success")
        return redirect("/login")
    session["retry_form_values"] = _fields
    flash("Virheellinen syöte yhdessä tai useammassa kentistä. \
        Tarkista tiedot.", "error")
    return redirect("/reset")


@application.route("/password")
def password():
    _user = session.get("username")
    if _user is None:
        flash("Toiminto vaatii kirjautumisen", "info")
        return redirect("/login")
    data = users.count()
    if data == 0:
        return redirect("/init_site")
    localized = ["Salasanan vaihtaminen", "Käyttäjänimi", "Salasana",
                 "Uusi salasana", "Toista uusi salasana", "Vaihda salasana"]
    return render_template("password_change.html",
                           text=localized[0],
                           username=localized[1],
                           password=localized[2],
                           new_password=localized[3],
                           repeat_new_password=localized[4],
                           submit=localized[3])


@application.route("/handle_password_change", methods=["POST"])
def handle_password_change():
    if request.form["csrf_token"] != session.get("csrf_token"):
        return abort(403)
    __fields = [request.form['username'], request.form['password'],
                request.form['new_password'], request.form['new_password_repeat']]
    __field_validations = [
        1 if validate_reg_or_log(__fields[0], "USERNAME") else 0,
        1 if validate_reg_or_log(__fields[1], "PASSWORD") else 0,
        1 if validate_reg_or_log(__fields[2], "PASSWORD") else 0,
        1 if validate_reg_or_log(__fields[3], "PASSWORD") else 0
    ]
    __user_data_request = "SELECT id, uname, pw_hash FROM Users WHERE uname=:un"
    __user_data_update = "UPDATE Users SET pw_hash=:hash WHERE uname=:un"
    _input_validations = [
        1 if input_validation(f) else 0 for f in __fields
    ]
    if sum(__field_validations) == 4 and sum(_input_validations) == 4:
        login_data = {"un": __fields[0]}
        user_result = DB.session.execute(
            __user_data_request, login_data)   # pylint: disable=no-member
        user_data = user_result.fetchone()
        validation_result = validate_passwords_on_change(
            __fields[1],
            user_data[2],
            __fields[2],
            __fields[3])
        if validation_result is not None:
            new_data = {"un": user_data[1], "hash": validation_result}
            try:
                DB.session.execute(
                    __user_data_update,
                    new_data)    # pylint: disable=no-member
                DB.session.commit()  # pylint: disable=no-member
                del session["username"]
                del session["user_status"]
                del session["csrf_token"]
                flash("Salasanan vaihto onnistui", "success")
                return redirect("/login")
            except:   # pylint: disable=bare-except
                flash("Salasanan vaohto epäonnistui. Yritä uudelleen.", "warning")
                return redirect("/password")
        flash("Tarkista kirjoittamasi kentät", "warning")
        return redirect("/password")
    flash("Virheellinen syöte yhdessä tai useammassa kentistä", "error")
    return redirect("/password")
