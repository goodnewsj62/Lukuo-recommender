from flask_migrate import MigrateCommand
from flask_script import Manager
from flask_app import create_app

app = create_app
manager = Manager(app)
manager.app_command('db', MigrateCommand)
