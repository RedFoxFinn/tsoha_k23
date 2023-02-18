
from database_module import DB

class User(DB.Model):
    id = DB.Column(DB.Integer,primary_key=True)
    uname = DB.Column(DB.String, unique=True, nullable=False)
    pw_hash = DB.Column(DB.String, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.uname

def register(new_username: str, new_password_hash: str):
    new_user = User(uname=new_username,pw_hash=new_password_hash)
    try:
        DB.session.add(new_user)
        DB.session.commit()
        _user_data = User.query.filter_by(uname=new_username).first()
        return _user_data
    except:
        return None


def count():
    _data = User.query.all()
    return len(_data)


def user_data(uname: str):
    _data = User.query.filter_by(uname=uname).first()
    return _data
