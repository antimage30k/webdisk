from flask import Blueprint, request, session, jsonify

from exception_handler import Error
from models.base import User
from routes import current_user, guest, login_required

main = Blueprint('main', __name__)


@main.route('/login', methods=['POST'])
def login():
    name = request.json['username']
    password = request.json['password']
    u: User = User.login(name, password)
    if u is None:
        raise Error.login_error
    session['user_id'] = u.id
    session.permanent = True
    return jsonify(dict(message="Login Succeeded", data=u.to_dict()))


@main.route('/logout', methods=['DELETE'])
def logout():
    session.pop('user_id', None)
    return jsonify(guest.to_dict())


@main.route('/register', methods=['POST'])
def register():
    json = request.json
    result = User.register(name=json['username'], password=json['password'])
    if result:
        return jsonify(dict(message="Register Succeeded"))
    else:
        raise Error.registration_failed


@main.route('/current_user', methods=['GET'])
def get_current_user():
    u: User = current_user()
    return jsonify(u.to_dict())


@main.route('/avatar/set', methods=['PATCH'])
@login_required
def set_avatar():
    u: User = current_user()
    avatar: str = request.json['avatar']
    u.update(avatar=avatar)
    return jsonify(u.to_dict())


@main.route('/avatar/upload', methods=['POST'])
@login_required
def upload_avatar():
    return
