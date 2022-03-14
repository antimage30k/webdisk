from functools import wraps

from flask import session, redirect

from models.base import User
from models.utils import UserRole
from settings import GUEST_NAME


def escape_filename(filename):
    filename = filename[:100]
    illegal = '/\:*?"<>|'
    trans = '_________'
    table = str.maketrans(illegal, trans)
    return filename.translate(table)


def current_user_id():
    u = current_user()
    return u.id


def current_user():
    user_id = session.get('user_id', -1)
    if user_id == -1:
        return guest

    u = User.get(id=user_id) or guest

    return u


def get_suffix(filename):
    parts = filename.rsplit('.', 1)
    if len(parts) == 2:
        return '.' + parts[1]
    else:
        return ''


def login_required(func):
    @wraps(func)
    def _wrapper(*args, **kwargs):
        u = current_user()
        if u is None:
            return redirect('/login')
        else:
            func(*args, **kwargs)

    return _wrapper


def admin_required(func):
    @wraps(func)
    def _wrapper(*args, **kwargs):
        u: User = current_user()
        if u.role != UserRole.ADMIN:
            return redirect('/login')
        else:
            func(*args, **kwargs)

    return _wrapper


class Guest:
    _instance = []

    def __new__(cls):
        if len(cls._instance) == 0:
            _guest = super().__new__(cls)
            cls._instance.append(_guest)
            return _guest
        else:
            return cls._instance[0]

    def __init__(self):
        self.id = -1
        self.name = GUEST_NAME
        self.role = UserRole.GUEST


guest = Guest()
