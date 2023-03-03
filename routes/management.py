
from flask import abort, redirect, render_template, request, session, flash

from app import application
from tools import admin_module as admins,\
    chat_module as chats,\
    group_module as groups,\
    topics_module as topics,\
    user_module as users
from tools.validate_input import input_validation, link_input_validation


@application.route("/management")
def management():
    _user = session.get("username")
    if _user is None:
        flash("Toiminto vaatii kirjautumisen", "warning")
        return redirect("/login")
    localized = {
        "text": "Hallintapaneeli",
        "groups": "Ryhmien hallinta",
        "chats": "Keskusteluryhmien hallinta",
        "users": "Käyttäjien hallinta"
    }
    return render_template("management.html", local=localized)


@application.route("/management/chats")
def chat_management():
    _user = session.get("username")
    if _user is None:
        flash("Toiminto vaatii kirjautumisen", "warning")
        return redirect("/login")
    _status = session.get("user_status")
    localized = {
        "text": "Hallintapaneeli",
        "current_mode": "Keskusteluryhmien hallinta",
        "add_new": "Keskusteluryhmän lisäys",
        "listing": "Keskusteluryhmälista",
        "groups": "Ryhmien hallinta",
        "chats": "Keskusteluryhmien hallinta",
        "users": "Käyttäjien hallinta",
        "chat_name": "Keskusteluryhmän nimi",
        "topic": "Aihe",
        "group": "Ryhmä",
        "link": "Linkki",
        "submit": "Lisää keskusteluryhmä",
        "update": "Päivitä",
        "tip_characters": "Sallittuja merkkejä",
        "tip_letters": "Kirjaimet a-z sekä A-Z",
        "tip_numbers": "Numerot 0-9"
    }
    _topic_data = topics.get_topics()
    _group_data = groups.get_groups()

    _chats = []
    _chats += chats.get_public_chats()
    _chats += chats.get_login_restricted_chats()
    _chats += chats.get_age_restricted_chats()
    if _status is not None and _status == "ADMIN":
        _chats += chats.get_security_restricted_chats()

    return render_template("chat_management.html",
                           local=localized,
                           topic_options=_topic_data if len(
                               _topic_data) > 0 else [],
                           group_options=_group_data if len(
                               _group_data) > 0 else [],
                           showable=_chats,
                           management="True")


@application.route("/management/chats/<int:id_value>")
def manage_single_chat(id_value: int):
    _user = session.get("username")
    if _user is None:
        flash("Toiminto vaatii kirjautumisen", "warning")
        return redirect("/login")
    localized = {
        "text": "Hallintapaneeli",
        "current_mode": "Keskusteluryhmien hallinta",
        "update": "Keskusteluryhmän muokkaus",
        "groups": "Ryhmien hallinta",
        "chats": "Keskusteluryhmien hallinta",
        "users": "Käyttäjien hallinta",
        "chat_name": "Keskusteluryhmän nimi",
        "topic": "Aihe",
        "group": "Ryhmä",
        "link": "Linkki",
        "mod": "Ylläpitäjä",
        "submit": "Päivitä keskusteluryhmä",
        "tip_characters": "Sallittuja merkkejä",
        "tip_letters": "Kirjaimet a-z sekä A-Z",
        "tip_numbers": "Numerot 0-9"
    }

    _topic_data = topics.get_topics()
    _group_data = groups.get_groups()
    _moderator_data = chats.get_chat_moderators()

    _chat_data = chats.get_chat_by_id(id_value)
    if _chat_data is None:
        flash("Keskusteluryhmää ei löydy.", "warning")
        return redirect("/management/chats")
    _admin_data = admins.check_admin_by_uname(_user)
    if _chat_data[6] != _user:
        if _admin_data is None:
            flash("Et voi muokata tätä keskusteluryhmää: puuttuvat oikeudet.", "error")
            return redirect("/management/chats")
    return render_template("single_chat_management.html",
                           local=localized,
                           chat={
                               "id": _chat_data[0],
                               "cname": _chat_data[1],
                               "link": _chat_data[2],
                               "topic": _chat_data[3],
                               "group": _chat_data[4],
                               "restriction": _chat_data[5],
                               "moderator": _chat_data[6]
                           },
                           topic_options=_topic_data if len(
                               _topic_data) > 0 else [],
                           group_options=_group_data if len(
                               _group_data) > 0 else [],
                           moderator_options=_moderator_data if len(
                               _moderator_data) > 0 else []
                           )


@application.route("/handle_chat_adding", methods=["POST"])
def handle_chat_adding():
    if request.form["csrf_token"] != session.get("csrf_token"):
        return abort(403)
    _uname = session.get("username")
    if _uname is None:
        flash("Toiminto vaatii kirjautumisen.", "warning")
        return redirect("/login")
    _user_data = users.user_by_uname(_uname)
    _fields = {
        "cname": request.form["cname"],
        "topic": request.form["topic"],
        "group": request.form["group"],
        "link": request.form["link"]
    }
    _input_validations = []
    _input_validations.append(1 if input_validation(_fields["cname"]) else 0)
    if _fields["topic"].isnumeric():
        _input_validations.append(1 if input_validation(
            _fields["topic"], short_mode=True) else 0)
    else:
        _input_validations.append(
            1 if input_validation(_fields["topic"]) else 0)
    _input_validations.append(1 if _fields["group"].isnumeric() else 0)
    _input_validations.append(
        1 if link_input_validation(_fields["link"]) else 0)
    if sum(_input_validations) < 4:
        session["retry_form_values"] = _fields
        flash("Virheellinen syöte yhdessä tai useammassa kentistä.", "error")
        return redirect("/management/chats")
    _fields["topic"] = topics.add_topic(_fields["topic"])
    _input_data = {
        "cname": _fields["cname"],
        "topic": int(_fields["topic"]),
        "group": int(_fields["group"]),
        "link": _fields["link"],
        "moderator": int(_user_data[0])
    }
    if chats.add_chat(_input_data):
        _retry_values = session.get("retry_form_values")
        if _retry_values is not None:
            del session["retry_form_values"]
        flash("Keskusteluryhmän lisääminen onnistui.", "success")
        return redirect("/management/chats")
    session["retry_form_values"] = _input_data
    flash("Virheellinen syöte yhdessä tai useammassa kentistä. Tarkista antamasi syöte.", "warning")
    return redirect("/management/chats")


@application.route("/handle_chat_update", methods=["POST"])
def handle_chat_update():
    if request.form["csrf_token"] != session.get("csrf_token"):
        return abort(403)
    _uname = session.get("username")
    if _uname is None:
        flash("Toiminto vaatii kirjautumisen.", "warning")
        return redirect("/login")
    _fields = {
        "id": request.form["id"],
        "cname": request.form["cname"],
        "topic": request.form["topic"],
        "group": request.form["group"],
        "link": request.form["link"],
        "moderator": request.form["moderator"]
    }
    _input_validations = []
    _input_validations.append(1 if input_validation(_fields["cname"]) else 0)
    if _fields["topic"].isnumeric():
        _input_validations.append(1 if input_validation(
            _fields["topic"], short_mode=True) else 0)
    else:
        _input_validations.append(
            1 if input_validation(_fields["topic"]) else 0)
    _input_validations.append(1 if _fields["group"].isnumeric() else 0)
    _input_validations.append(
        1 if link_input_validation(_fields["link"]) else 0)
    if sum(_input_validations) < 4:
        session["retry_form_values"] = _fields
        flash("Virheellinen syöte yhdessä tai useammassa kentistä.", "error")
        return redirect("/management/chats")
    _fields["topic"] = topics.add_topic(_fields["topic"])
    _input_data = {
        "cname": _fields["cname"],
        "topic": int(_fields["topic"]),
        "group": int(_fields["group"]),
        "link": _fields["link"],
        "moderator": int(_fields["moderator"]),
        "id": int(_fields["id"])
    }
    if chats.update_chat(_input_data):
        _retry_values = session.get("retry_form_values")
        if _retry_values is not None:
            del session["retry_form_values"]
        flash("Keskusteluryhmän päivittäminen onnistui.", "success")
        return redirect("/management/chats")
    session["retry_form_values"] = _input_data
    flash("Virheellinen syöte yhdessä tai useammassa kentistä. \
        Tarkista antamasi syöte.", "warning")
    return redirect("/management/chats")


@application.route("/handle_chat_removal", methods=["POST"])
def handle_chat_removal():
    _user = session.get("username")
    if _user is None:
        flash("Toiminto vaatii kirjautumisen", "warning")
        return redirect("/login")
    _id_value = request.form["id"]
    _chat = chats.get_chat_by_id(_id_value)
    _admin_data = None
    if _chat[6] != _user:
        _admin_data = admins.check_admin_by_uname(_user)
        if _admin_data is None:
            flash("Sinulla ei ole tarvittavia oikeuksia tähän toimintoon.", "error")
            return redirect("/management/chats")
    if chats.remove_chat(_id_value):
        flash("Keskusteluryhmä poistettu onnistuneesti.", "success")
        return redirect("/management/chats")
    flash("Keskusteluryhmää ei poistettu: tietoja ei löytynyt.", "error")
    return redirect(f"/management/chats/{_id_value}")


@application.route("/management/groups")
def group_management():
    localized = {
        "text": "Hallintapaneeli",
        "current_mode": "Ryhmien hallinta",
        "add_new": "Ryhmän lisäys",
        "listing": "Ryhmälista",
        "groups": "Ryhmien hallinta",
        "chats": "Keskusteluryhmien hallinta",
        "users": "Käyttäjien hallinta",
        "group_name": "Ryhmän nimi",
        "restriction_level": "Rajoitustaso",
        "submit": "Lisää ryhmä",
        "update": "Päivitä",
        "tip_header": "Ohjeet ryhmien lisäämiseen",
        "tip_groupname": "Ryhmän nimen pituus 3-32 merkkiä",
        "tip_characters": "Sallittuja merkkejä",
        "tip_letters": "Kirjaimet a-z sekä A-Z",
        "tip_numbers": "Numerot 0-9",
        "tip_forbidden": "Erikoismerkit eivät ole salittuja"
    }
    _restriction_opts = [("NONE", "Rajoittamaton"), ("LOGIN", "Kirjautuminen"),
                         ("AGE", "Ikärajoitettu"), ("SEC", "Turvaluokitettu")]
    _user = session.get("username")
    if _user is not None:
        data = groups.get_groups()
        return render_template(
            "group_management.html",
            local=localized,
            restriction_options=_restriction_opts,
            groups=data)
    flash("Toiminto vaatii kirjautumisen.", "warning")
    return redirect("/login")


@application.route("/management/groups/<int:id_value>")
def manage_single_group(id_value: int):
    _user = session.get("username")
    if _user is None:
        flash("Toiminto vaatii kirjautumisen", "warning")
        return redirect("/login")
    _admin_data = admins.check_admin_by_uname(_user)
    if _admin_data is None:
        flash("Toiminto vaatii käyttäjältä ylläpitäjän oikeudet.", "error")
        return redirect("/")
    _group = groups.get_group_by_id(id_value)
    old_data = {
        "old_name": _group[1],
        "old_restriction": _group[2],
        "id": _group[0]
    }
    localized = {
        "text": "Hallintapaneeli",
        "current_mode": "Ryhmän hallinta",
        "groups": "Ryhmien hallinta",
        "chats": "Keskusteluryhmien hallinta",
        "users": "Käyttäjien hallinta",
        "group_name": "Ryhmän nimi",
        "restriction_level": "Rajoitustaso",
        "submit": "Päivitä ryhmä"
    }
    _restriction_opts = [
        ("NONE", "Rajoittamaton"),
        ("LOGIN", "Kirjautuminen"),
        ("AGE", "Ikärajoitettu"),
        ("SEC", "Turvaluokitettu")
    ]
    return render_template(
        "single_group_management.html",
        local=localized,
        restriction_options=_restriction_opts,
        group=old_data)


@application.route("/handle_group_adding", methods=["POST"])
def handle_group_adding():
    if request.form["csrf_token"] != session.get("csrf_token"):
        return abort(403)
    _uname = session.get("username")
    if _uname is None:
        flash("Toiminto vaatii kirjautumisen", "warning")
        return redirect("/login")
    _input = {
        "gname": request.form["gname"],
        "restriction": request.form["restriction"]
    }
    _input_validations = [
        1 if input_validation(_input["gname"]) else 0,
        1 if input_validation(_input["restriction"]) else 0
    ]
    if sum(_input_validations) < 2:
        flash("Virheellinen syöte yhdessä tai useammassa kentistä. \
            Tarkista antamasi syöte.", "error")
        return redirect("/management/groups")
    _admin_data = admins.check_admin_by_uname(_uname)
    if _admin_data is None:
        flash("Toiminto vaatii käyttäjältä ylläpitäjän oikeudet.", "error")
        return redirect("/")
    if groups.add_group(_input["gname"], _input["restriction"], _admin_data[0]):
        _retry_values = session.get("retry_form_values")
        if _retry_values is not None:
            del session["retry_form_values"]
        flash("Ryhmän lisääminen onnistui", "success")
        return redirect("/management/groups")
    session["retry_form_values"] = _input
    flash("Ryhmä on jo olemassa. \
        Valitse toinen nimi tai käytä olemassaolevaa ryhmää.", "warning")
    return redirect("/management/groups")


@application.route("/handle_group_update", methods=["POST"])
def handle_group_update():
    if request.form["csrf_token"] != session.get("csrf_token"):
        return abort(403)
    _uname = session.get("username")
    if _uname is None:
        flash("Toiminto vaatii kirjautumisen", "warning")
        return redirect("/login")
    _input = {
        "gname": request.form["gname"],
        "restriction": request.form["restriction"],
        "id": request.form["id"]
    }
    _input_validations = [
        1 if input_validation(_input["gname"]) else 0,
        1 if input_validation(_input["restriction"]) else 0
    ]
    if sum(_input_validations) < 2:
        flash("Virheellinen syöte yhdessä tai useammassa kentistä. \
            Tarkista antamasi syöte.", "error")
        return redirect("/management/groups")
    if groups.update_group(int(_input["id"]), _input["gname"], _input["restriction"]):
        _retry_values = session.get("retry_form_values")
        if _retry_values is not None:
            del session["retry_form_values"]
        flash("Ryhmän päivittämimnen onnistui", "success")
        return redirect("/management/groups")
    session["retry_form_values"] = _input
    flash("Virheellinen syöte yhdessä tai useammassa kentistä. \
        Tarkista antamasi syöte.", "warning")
    return redirect(f"/management/groups/{_input['id']}")


@application.route("/management/users")
def user_management():
    _user = session.get("username")
    if _user is None:
        flash("Toiminto vaatii kirjautumisen.","warning")
        return redirect("/login")
    _admin_data = admins.check_admin_by_uname(_user)
    if _admin_data is None:
        flash("Toiminto vaatii pääkäyttäjän oikeudet.","error")
        return redirect("/management")
    localized = {
        "text": "Hallintapaneeli",
        "current_mode": "Käyttäjien hallinta",
        "groups": "Ryhmien hallinta",
        "chats": "Keskusteluryhmien hallinta",
        "users": "Käyttäjien hallinta",
        "listing": "Käyttäjät",
        "name": "käyttäjänimi",
        "link": "Keskustelulinkki",
        "is_admin": "Pääkäyttäjä?",
        "restriction_level": "Rajoitustaso",
        "change": "Muuta",
        "reset_pw": "Nollaa salasana",
        "reset": "Nollaa"
    }
    _user_data = users.users_with_admin_status()
    if _user_data:
        return render_template(
            "user_management.html",
            local=localized,
            users=_user_data
        )
    return "user management will eventually be here. Soon<sup>TM</sup>"

@application.route("/handle_admin_change", methods=["POST"])
def handle_admin_change():
    if request.form["csrf_token"] != session.get("csrf_token"):
        return abort(403)
    _user = session.get("username")
    if _user is None:
        flash("Toiminto vaatii kirjautumisen.","warning")
        return redirect("/login")
    _admin_data = admins.check_admin_by_uname(_user)
    if _admin_data is None:
        flash("Toiminto vaatii pääkäyttäjän oikeudet.","error")
        return redirect("/management")
    _fields = {
        "id": int(request.form["id"]),
        "uname": request.form["uname"]
    }
    if _admin_data[1] == _fields["id"]:
        flash("Et voi muuttaa omaa statustasi","error")
        return redirect("/management/users")
    _result = admins.change_admin_status(_fields["id"],_admin_data[0])
    if _result[0] == 'REGISTER':
        if _result[1]:
            flash(f"Käyttäjä {_fields['uname']} asetettu pääkäyttäjäksi","success")
        else:
            flash("Virhe: muutettavia tietoja ei löydetty.","error")
    if _result[0] == 'CANCEL':
        if _result[1]:
            flash(f"Käyttäjän {_fields['uname']} pääkäyttäjäoikeudet peruttu","success")
        else:
            flash("Virhe: muutettavia tietoja ei löydetty.","error")
    return redirect("/management/users")

@application.route("/reset_password", methods=["POST"])
def reset_password():
    if request.form["csrf_token"] != session.get("csrf_token"):
        return abort(403)
    _user = session.get("username")
    if _user is None:
        flash("Toiminto vaatii kirjautumisen.","warning")
        return redirect("/login")
    _admin_data = admins.check_admin_by_uname(_user)
    if _admin_data is None:
        flash("Toiminto vaatii pääkäyttäjän oikeudet.","error")
        return redirect("/management")
    _fields = {
        "id": int(request.form["id"]),
        "uname": request.form["uname"]
    }
    if _fields["uname"] == _user:
        del session["username"]
        del session["user_status"]
    _outcome = users.reset_user_password(_fields["id"], _admin_data[0])
    if _outcome:
        flash(f"Käyttäjän {_fields['uname']} salasana nollattu.","info")
        return redirect("/management/users")
    flash("Virhe: muutettavia tietoja ei löydetty.","error")
    return redirect("/management/users")