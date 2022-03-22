from flask import Blueprint, render_template, request, session, jsonify

from exception_handler import APIException
from models.base import User
from routes import current_user

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/login', methods=['POST'])
def login():
    name = request.json['username']
    password = request.json['password']
    u: User = User.login(name, password)
    if u is None:
        raise APIException("invalid", 501, "001")
    session['user_id'] = u.id
    session.permanent = True
    return jsonify(dict(message="Login Succeeded", data=u.to_dict()))


@main.route('/register', methods=['POST'])
def register():
    json = request.json
    result = User.register(name=json['username'], password=json['password'])
    if result:
        return jsonify(dict(message="Register Succeeded"))
    else:
        return jsonify(dict(message=""))


@main.route('/current_user', methods=['GET'])
def get_current_user():
    u: User = current_user()
    return jsonify(u.to_dict())
