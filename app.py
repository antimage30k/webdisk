from flask import Flask

import settings
from exception_handler import handle
from models.base import db
from routes.disk import disk as disk_bp
from routes.main import main as main_bp


class AppConfig:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@localhost:{}/webdisk?charset=utf8mb4'.format(
        settings.MYSQL_USER, settings.MYSQL_PASSWORD, settings.DB_PORT)
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_TEARDOWN = True


def create_app():
    app = Flask(__name__)
    app.secret_key = settings.FLASK_SECRET_KEY
    app.config.from_object(AppConfig)
    db.init_app(app)
    app.register_blueprint(main_bp, url_prefix='/api')
    app.register_blueprint(disk_bp, url_prefix='/api/disk')
    app.errorhandler(Exception)(handle)
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
