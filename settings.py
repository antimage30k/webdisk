import os

try:
    import config


    def _get(key, default):
        return getattr(config, key, default)
except ImportError as e:
    config = None


    def _get(key, default):
        return os.environ.get(key, default)

SALT = _get('SALT', '7LG*Pn$cQ%Cqk4')

FLASK_SECRET_KEY = _get('FLASK_SECRET_KEY', '7LG*Pn$cQ%Cqk4')

MYSQL_PASSWORD = _get('MYSQL_PASSWORD', 'test')
MYSQL_USER = _get('MYSQL_USER', 'root')
DB_HOST = _get('DB_HOST', 'localhost')
DB_PORT = _get('DB_PORT', 3306)

DATABASE_NAME = 'webdisk'
REDIS_HOST = ''
GUEST_NAME = '游客'

BASE_FILE_PATH = _get('BASE_FILE_PATH', r'/home/webdisk')
DOWNLOAD_URL_PREFIX = '/download'

ADMIN_PASS = _get('ADMIN_PASS', 'admin')
