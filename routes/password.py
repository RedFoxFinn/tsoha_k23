
from flask import abort, redirect, render_template, request, session, flash

from app import application
from tools.database_module import DB
from tools.validate_input import input_validation, validate_reg_or_log
from tools.password_tools import validate_passwords_on_change

@application.route("/password")
def password():
    _user = session.get("username")
    if _user is None:
        flash("Toiminto vaatii kirjautumisen", "info")
        return redirect("/login")
    sql = "SELECT count(*) FROM Users"
    result = DB.session.execute(sql)
    data = result.fetchall()[0]
    if data[0] == 0:
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
    if request.form["csrf_token"] is not session.get("csrf_token"):
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
    if sum(__field_validations) == 4 and\
        (1 if input_validation(f) else 0 for f in __fields) == 0:
        login_data = {"un": __fields[0]}
        user_result = DB.session.execute(__user_data_request, login_data)
        user_data = user_result.fetchone()
        validation_result = validate_passwords_on_change(
            __fields[1],
            user_data[2],
            __fields[2],
            __fields[3])
        if validation_result is not None:
            new_data = {"un": user_data[1], "hash": validation_result}
            try:
                DB.session.execute(__user_data_update, new_data)
                DB.session.commit()
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
