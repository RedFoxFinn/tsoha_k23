
from src.modules.database_module import DB

class Admin(DB.Model):
    id = DB.Column(DB.Integer,primary_key=True)
    user_id = DB.Column(DB.Integer, nullable=False)
    superuser = DB.Column(DB.Boolean, nullable=False)

    def __repr__(self):
        return '<Admin %r>' % self.user_id

def register_admin(uid: int,super:bool=False):
    _new_admin = Admin(user_id=uid,superuser=super)
    try:
        DB.session.add(_new_admin)
        DB.session.commit()
        return True
    except:
        return False


def check_admin(uid: int):
    _admin_data = Admin.query.filter_by(user_id=uid).first()
    return _admin_data
