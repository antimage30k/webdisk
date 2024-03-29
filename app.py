from flask import Flask

import settings
from exception_handler import handle
from models.base import db
from routes.disk import disk as disk_bp
from routes.main import main as main_bp
from utils.util import escape


class AppConfig:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}:{}/webdisk?charset=utf8mb4'.format(
        escape(settings.MYSQL_USER), escape(settings.MYSQL_PASSWORD), settings.DB_HOST,
        settings.DB_PORT)
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_TEARDOWN = True
    SQLALCHEMY_POOL_RECYCLE = 400


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
    # app.config['TEMPLATES_AUTO_RELOAD'] = True
    # app.jinja_env.auto_reload = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    config = dict(
        debug=True,
        host='127.0.0.1',
        port=4000,
    )
    app.run(**config)
