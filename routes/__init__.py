from functools import wraps

from flask import session, redirect

from models.base import User
from models.utils import UserRole


def current_user_id():
    return session.get('user_id', -1)


def current_user():
    user_id = session.get('user_id', -1)
    if user_id == -1:
        return None
    u = User.get(id=user_id)

    return u


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
