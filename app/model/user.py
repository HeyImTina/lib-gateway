from datetime import datetime
from functools import wraps

from flask import abort
from flask_login import LoginManager, UserMixin, AnonymousUserMixin
from flask_login import current_user
from werkzeug.security import generate_password_hash, check_password_hash

from app.model import db


class Permission(object):
    USER = 0x1
    ADMINISTER = 0x3


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    password_hash = db.Column(db.String(128))
    permission = db.Column(db.Integer)
    avatar = db.Column(db.String(200))
    created_time = db.Column(db.DateTime(), default=datetime.now)

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute!")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def can(self, permission):
        return (self.permission & permission) == permission

    def json(self):
        return {
            "name": self.name,
            "avatar": self.avatar,
            "is_admin": self.permission == Permission.ADMINISTER
        }


login_manager = LoginManager()
login_manager.session_protection = 'strong'


class AnonymousUser(AnonymousUserMixin):

    @staticmethod
    def can(permissions):
        return False


login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def admin_required(f):
    return permission_required(Permission.ADMINISTER)(f)