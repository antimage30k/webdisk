from flask import Flask
from flask_cors import CORS

from models.base import db
from routes.main import main as main_bp
from routes.disk import disk as disk_bp
import settings


def create_app():
    app = Flask(__name__)
    CORS(app, supports_credentials=True)
    app.secret_key = settings.FLASK_SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@localhost:{}/webdisk?charset=utf8mb4'.format(
        settings.MYSQL_USER, settings.MYSQL_PASSWORD, settings.DB_PORT
    )
    db.init_app(app)
    app.register_blueprint(main_bp)
    app.register_blueprint(disk_bp, url_prefix='/disk')
    return app


if __name__ == "__main__":
    app = create_app()
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.jinja_env.auto_reload = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    config = dict(
        debug=True,
        host='127.0.0.1',
        port=4000,
    )
    app.run(**config)
