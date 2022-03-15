from flask import Blueprint, redirect, render_template, request, session, jsonify

from models.base import User

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']
    u = User.login(username, password)
    if u is None:
        return jsonify(dict(message="Login Failed"))
    session['user_id'] = u.id
    session.permanent = True
    return jsonify(dict(message="Login Succeeded"))


@main.route('/register', methods=['POST', "GET"])
def register():
    if request.method == 'GET':
        return render_template('/')
    if request.method == "POST":
        form = request.form
        result = User.register(name=form['name'], password=form['password'])
        if result:
            redirect('/login')
        else:
            redirect('/register')
