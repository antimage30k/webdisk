from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

import settings
from models.base import db, User
from models.utils import salted_password, UserRole
from wsgi import application

manager = Manager(application)
migrate = Migrate(application, db)

manager.add_command('db', MigrateCommand)


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
