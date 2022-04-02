from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from sqlalchemy import create_engine

import settings
from models.base import db, User
from models.utils import salted_password, UserRole
from wsgi import application

manager = Manager(application)
migrate = Migrate(application, db)

manager.add_command('db', MigrateCommand)


@manager.command
def create_db():
    uri = f'mysql+pymysql://{settings.MYSQL_USER}:{settings.MYSQL_PASSWORD}@' \
          f'{settings.DB_HOST}:{settings.DB_PORT}/?charset=utf8mb4'
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


if __name__ == '__main__':
    manager.run()
