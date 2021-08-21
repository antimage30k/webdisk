from models.base import db, User
from sqlalchemy import create_engine

from models.utils import UserRole
from settings import MYSQL_USER, MYSQL_PASSWORD, DATABASE_NAME
from app import create_app
from models.utils import salted_password


def reset_db():
    uri = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@localhost/?charset=utf8mb4'
    engine = create_engine(uri,
                           encoding='utf-8',
                           pool_recycle=3600,
                           pool_pre_ping=True,
                           echo=True,
                           )
    with engine.connect() as e:
        e.execute(f'DROP DATABASE IF EXISTS {DATABASE_NAME}')
        e.execute(f'CREATE DATABASE {DATABASE_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')
        e.execute(f'USE {DATABASE_NAME}')

    # 不知为何，不能使用db.create_all
    db.metadata.create_all(bind=engine)


def generate_fake_data():
    form = dict(
        name='admin',
        password=salted_password('admin'),
        role=UserRole.ADMIN,
    )
    User.create(form)


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        reset_db()
        generate_fake_data()
