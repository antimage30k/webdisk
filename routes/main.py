from flask import Blueprint, redirect, render_template, request, session, jsonify

from models.base import User

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/login', methods=['POST'])
def login():
    name = request.json['username']
    password = request.json['password']
    u = User.login(name, password)
    if u is None:
        return jsonify(dict(message="Login Failed"))
    session['user_id'] = u.id
    session.permanent = True
    return jsonify(dict(message="Login Succeeded"))


@main.route('/register', methods=['POST'])
def register():
    json = request.json
    result = User.register(name=json['username'], password=json['password'])
    if result:
        return jsonify(dict(message="Register Succeeded"))
    else:
        return jsonify(dict(message=""))
