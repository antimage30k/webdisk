import logging
import os

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from sqlalchemy import create_engine

import settings
from models.base import db, User
from models.utils import salted_password, UserRole
from utils.logger import init_logging
from utils.util import escape
from wsgi import application

init_logging()
logger = logging.getLogger(__name__)

manager = Manager(application)
migrate = Migrate(application, db)

manager.add_command('db', MigrateCommand)


@manager.command
def create_db():
    uri = f"mysql+pymysql://{escape(settings.MYSQL_USER)}:{escape(settings.MYSQL_PASSWORD)}@" \
          f"{settings.DB_HOST}:{settings.DB_PORT}/?charset=utf8mb4"
    engine = create_engine(uri,
                           encoding='utf-8',
                           pool_recycle=3600,
                           pool_pre_ping=True,
                           echo=True,
                           )
    with engine.connect() as e:
        e.execute(
            f'CREATE DATABASE if not exists {settings.DATABASE_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')


@manager.command
def add_admin():
    if User.get(id=1) is not None:
        return
    form = dict(
        name='admin',
        password=salted_password(settings.ADMIN_PASS),
        role=UserRole.ADMIN,
    )
    User.create(form)


@manager.command
def set_environ():
    """
    supervisor 有自己的环境变量，读不到docker 容器的environment
    """
    envs = []
    for key, val in os.environ.items():
        envs.append(f'{key}="{val}",')
    if envs:
        supervisor_env = 'environment=' + ''.join(envs)
        with open('/etc/supervisor/conf.d/webdisk.conf', 'a') as f:
            f.write('\n')
            f.write(supervisor_env)


if __name__ == '__main__':
    manager.run()
