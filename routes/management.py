
from flask import abort,redirect, render_template, request, session, flash

from app import application
from modules.database_module import DB
import modules.chat_module as chats
import modules.topics_module as topics
from tools.validate_input import input_validation

_admin_levels = ["ADMIN","SUPER"]

@application.route("/management")
def management():
    _user = session.get("username")
    if _user == None:
        flash("Toiminto vaatii kirjautumisen","warning")
        return redirect("/login")
    else:
        _status = session.get("user_status")
        print(_user,_status)
        if _status not in _admin_levels:
            flash("Toiminto vaatii ylläpitäjän oikeudet","error")
            return redirect("/")
        else:
            localized = {
              "text":"Hallintapaneeli",
              "groups":"Ryhmien hallinta",
              "chats":"Keskusteluryhmien hallinta",
              "admins":"Pääkäyttäjien hallinta"
            }
            return render_template("management.html", local=localized)

@application.route("/management/chats")
def chat_management():
    localized = {
      "text":"Hallintapaneeli",
      "current_mode": "Keskusteluryhmien hallinta",
      "add_moderator": "Ylläpitäjän lisäys",
      "handle": "Nimimerkki",
      "chat_link": "Keskustelulinkki",
      "mod_submit":"Lisää ylläpitäjä",
      "add_new": "Keskusteluryhmän lisäys",
      "listing": "Keskusteluryhmälista",
      "groups":"Ryhmien hallinta",
      "chats":"Keskusteluryhmien hallinta",
      "admins":"Pääkäyttäjien hallinta",
      "chat_name": "Keskusteluryhmän nimi",
      "topic": "Aihe",
      "group": "Ryhmä",
      "link": "Linkki",
      "moderators": "Ylläpitäjät",
      "submit": "Lisää keskusteluryhmä",
      "update": "Päivitä"
    }
    _topic_sql = "SELECT id,topic FROM Topics"
    _topic_result = DB.session.execute(_topic_sql)
    _topic_data = _topic_result.fetchall()

    _group_sql = "SELECT id,gname FROM Groups"
    _group_result = DB.session.execute(_group_sql)
    _group_data = _group_result.fetchall()

    _moderator_sql = "SELECT id,handle FROM Moderators"
    _moderator_result = DB.session.execute(_moderator_sql)
    _moderator_data = _moderator_result.fetchall()

    _user = session.get("username")
    _permission = session.get("user_status")

    if _user != None and _permission != None and _permission in _admin_levels:
        _chats = []
        _chats += chats.get_public_chats()
        _chats += chats.get_login_restricted_chats()
        _chats += chats.get_age_restricted_chats()
        _chats += chats.get_security_restricted_chats()
        return render_template("chat_management.html",
          local=localized,
          topic_options=_topic_data if len(_topic_data) > 0 else [],
          group_options=_group_data if len(_group_data) > 0 else [],
          moderator_options=_moderator_data if len(_moderator_data) > 0 else [],
          showable=_chats,
          management="True",
          header={"public": "Julkiset", "login": "Kirjautuneille", "admin": "Rajoitetut"}
        )
    else:
        flash("Toiminto vaatii kirjautumisen","warning")
        return redirect("/login")

@application.route("/management/chats/<int:id>")
def manage_single_chat(id:int):
    return f"I will manage chat with id {id}"

@application.route("/handle_chat_adding", methods=["POST"])
def handle_chat_adding():
    if request.form["csrf_token"] != session.get("csrf_token"):
        return abort(403)
    _fields = [
      request.form["cname"],
      request.form["topic"],
      request.form["group"],
      request.form["link"],
      request.form["moderators"]
    ]
    if sum([1 if input_validation(f) else 0 for f in _fields]) == 0:
        _fields[1] = topics.add_topic(_fields[1])
        input_data = {"cname": _fields[0],"topic":int(_fields[1]),"group":int(_fields[2]),"link":_fields[3],"moderators":[int(mod) for mod in _fields[4]]}
        if chats.add_chat(input_data):
            flash("Keskusteluryhmän lisääminen onnistui", "success")
            return redirect("/management/chats")
        else:
            flash("Virheellinen syöte yhdessä tai useammassa kentistä", "warning")
            return redirect("/management/chats")
    else:
        flash("Virheellinen syöte yhdessä tai useammassa kentistä","error")
        return redirect("/management/chats")

@application.route("/handle_moderator_adding", methods=["POST"])
def handle_moderator_adding():
    if request.form["csrf_token"] != session.get("csrf_token"):
        return abort(403)
    _fields = [request.form["handle"], request.form["chat_link"]]
    if sum([1 if input_validation(f) else 0 for f in _fields]) == 0:
        input_data = {"handle": _fields[0],"chat_link":_fields[1]}
        sql = f"INSERT INTO Moderators (handle,chat_link) VALUES (:handle,:chat_link)"
        try:
            DB.session.execute(sql, input_data)
            DB.session.commit()
            flash("Ylläpitäjän lisääminen onnistui", "success")
            return redirect("/management/chats")
        except:
            flash("Virheellinen syöte yhdessä tai useammassa kentistä", "warning")
            return redirect("/management/chats")
    else:
        flash("Virheellinen syöte yhdessä tai useammassa kentistä","error")
        return redirect("/management/chats")

@application.route("/management/groups")
def group_management():
    localized = {
      "text":"Hallintapaneeli",
      "current_mode": "Ryhmien hallinta",
      "add_new": "Ryhmän lisäys",
      "listing": "Ryhmälista",
      "groups":"Ryhmien hallinta",
      "chats":"Keskusteluryhmien hallinta",
      "admins":"Pääkäyttäjien hallinta",
      "group_name": "Ryhmän nimi",
      "restriction_level": "Rajoitustaso",
      "submit": "Lisää ryhmä",
      "update": "Päivitä"
    }
    _restriction_opts = [("NONE","Rajoittamaton"),("LOGIN","Kirjautuminen"),("AGE","Ikärajoitettu"),("SEC","Turvaluokitettu")]
    _user = session.get("username")
    if _user != None:
        sql = "SELECT id,gname,restriction FROM Groups"
        result = DB.session.execute(sql)
        data = result.fetchall()
        return render_template("group_management.html", local=localized, restriction_options=_restriction_opts, groups=data)
    else:
        flash("Toiminto vaatii kirjautumisen","warning")
        return redirect("/login")

@application.route("/management/groups/<int:id>", methods=["POST"])
def manage_single_group(id:int):
    _old_name = request.form["gname"]
    _old_restriction = request.form["restriction"]
    _user = session.get("username")
    _status = session.get("user_status")
    if _status == None or _status not in ["ADMIN","SUPER"]:
        flash("Toiminto vaatii ylläpitäjän oikeudet")
        return redirect("/management")
    elif _status in ["ADMIN","SUPER"]:
        old_data = {"old_name":_old_name,"old_restriction":_old_restriction,"id":id}
        localized = {
          "text":"Hallintapaneeli",
          "current_mode": "Ryhmän hallinta",
          "groups":"Ryhmien hallinta",
          "chats":"Keskusteluryhmien hallinta",
          "admins":"Ylläpitäjien hallinta",
          "group_name": "Ryhmän nimi",
          "restriction_level": "Rajoitustaso",
          "submit": "Päivitä ryhmä"
        }
        _restriction_opts = [("NONE","Rajoittamaton"),("LOGIN","Kirjautuminen"),("AGE","Ikärajoitettu"),("SEC","Turvaluokitettu")]
        return render_template("single_group_management.html", local=localized, restriction_options=_restriction_opts,group=old_data)

@application.route("/handle_group_adding", methods=["POST"])
def handle_group_adding():
    if request.form["csrf_token"] != session.get("csrf_token"):
        return abort(403)
    _fields = [request.form["gname"], request.form["restriction"]]
    if sum([1 if input_validation(f) else 0 for f in _fields]) == 0:
        input_data = {"gname": _fields[0],"restrict":_fields[1]}
        sql = f"INSERT INTO Groups (gname,restriction) VALUES (:gname,:restrict)"
        try:
            DB.session.execute(sql, input_data)
            DB.session.commit()
            flash("Ryhmän lisääminen onnistui", "success")
            return redirect("/management/groups")
        except:
            flash("Virheellinen syöte yhdessä tai useammassa kentistä", "warning")
            return redirect("/management/groups")
    else:
        flash("Virheellinen syöte yhdessä tai useammassa kentistä","error")
        return redirect("/management/groups")

@application.route("/handle_group_update", methods=["POST"])
def handle_group_update():
    if request.form["csrf_token"] != session.get("csrf_token"):
        return abort(403)
    _fields = [request.form["gname"], request.form["restriction"],request.form["id"]]
    if sum([1 if input_validation(f) else 0 for f in _fields]) == 0:
        sql = f"UPDATE Groups SET gname='{_fields[0]}',restriction='{_fields[1]}' WHERE id={_fields[2]}"
        try:
            DB.session.execute(sql)
            DB.session.commit()
            flash("Ryhmän päivittämimnen onnistui", "success")
            return redirect("/management/groups")
        except:
            flash("Virheellinen syöte yhdessä tai useammassa kentistä", "warning")
            return redirect("/management/groups")
    else:
        flash("Virheellinen syöte yhdessä tai useammassa kentistä","error")
        return redirect("/management/groups")

@application.route("/management/admins")
def admin_management():
    return "admin management will eventually be here. Soon<sup>TM</sup>"