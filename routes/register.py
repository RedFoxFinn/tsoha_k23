
from flask import redirect, render_template, request, session, flash

from app import application
from tools import config_module as config, admin_module as admins, user_module as users
from tools.validate_input import input_validation, validate_reg_or_log
from tools.password_tools import validate_password_on_register


@application.route("/register")
def register():
    _user = session.get("username")
    if _user is not None:
        return redirect("/")
    localized = {
        "text":"Rekisteröityminen palveluun",
        "username":"Käyttäjänimi",
        "password":"Salasana",
        "dm_link":"Linkki yksityiskeskusteluun",
        "repeat_password":"Toista salasana",
        "registration_code":"Rekisteröitymistunnus",
        "submit":"Rekisteröidy",
        "tip_header":"Ohjeet rekisteröitymiseen",
        "tip_username":"Käyttäjätunnuksen pituus 5-32 merkkiä",
        "tip_password":"Salasanan pituus 8-32 merkkiä",
        "tip_dmlink": "Linkin muoto: https://t.me/*käyttäjätunnus*",
        "tip_characters":"Sallittuja merkkejä",
        "tip_letters":"Kirjaimet a-z sekä A-Z",
        "tip_numbers":"Numerot 0-9",
        "tip_forbidden":"Sallitut erikoismerkit . $ € £ _ - + @",
        "tip_uname":"5-32 merkkiä",
        "tip_pw":"8-32 merkkiä",
        "tip_dm_link": "https://t.me/..."
    }
    return render_template("registration.html",locals=localized)


@application.route("/handle_registration", methods=["POST"])
def handle_registration():
    _input = {
        "uname": request.form["new_username"],
        "pw1": request.form["new_password"],
        "pw2": request.form["new_password_repeat"],
        "dm_link": request.form["new_dm_link"],
        "reg_code": request.form["registration_code"]
    }
    __field_validations = [
        1 if validate_reg_or_log(_input["uname"], "USERNAME") else 0,
        1 if validate_reg_or_log(_input["pw1"], "PASSWORD") else 0,
        1 if validate_reg_or_log(_input["pw2"], "PASSWORD") else 0
    ]
    __input_validations = [
        1 if input_validation(_input["uname"]) else 0,
        1 if input_validation(_input["uname"]) else 0,
        1 if input_validation(_input["uname"]) else 0,
        1 if input_validation(_input["uname"]) else 0,
        1 if input_validation(_input["uname"]) else 0
    ]
    if _input["reg_code"] != config.REG_CODE:
        session["retry_form_values"] = _input
        flash("Väärä rekisteröitymistunnus. Tarkista tietojesi oikeellisuus.","warning")
        return redirect("/register")
    _pw_validation = validate_password_on_register(_input["pw1"], _input["pw2"])
    if _pw_validation is None:
        session["retry_form_values"] = _input
        flash("Salasanasi eivät vastaa toisiaan. Tarkista tietojesi oikeellisuus.","warning")
        return redirect("/register")
    if sum(__input_validations) == 5 and sum(__field_validations) == 3:
        _result = users.register(_input["uname"], _pw_validation, _input["dm_link"])
        if _result is not None:
            _retry_values = session.get("retry_form_values")
            if _retry_values is not None:
                del session["retry_form_values"]
            flash("Rekisteröityminen onnistui!", "success")
            if (_result[0] == 1 or users.count() == 1) and admins.register_admin(_result[0]):
                flash("Tunnus rekisteröity pääkäyttäjäksi", "success")
            return redirect("/login")
        session["retry_form_values"] = _input
        flash("Käyttäjätunnus on jo käytössä", "info")
        return redirect("/register")
    session["retry_form_values"] = _input
    flash("Virheellinen syöte yhdessä tai useammassa kentistä. \
        Tarkista antamasi rekisteröitymistunnus tai salasanakentät.", "warning")
    return redirect("/register")
