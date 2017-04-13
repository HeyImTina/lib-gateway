from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_script import Shell

from app.model import db

from app import create_app

app = create_app("dev")
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
