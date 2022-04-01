from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from models.base import db
from wsgi import application

manager = Manager(application)
migrate = Migrate(application, db)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
