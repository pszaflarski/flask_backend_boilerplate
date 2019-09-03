import os
if os.path.exists('.env'):
    print('Importing environment from .env...')
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]

from app import create_app
from flask_script import Manager
from app import db
from app.models import User

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
# print("ENVIRONMENT:{}".format(os.getenv('FLASK_CONFIG') or 'default'))
manager = Manager(app)

@manager.command
def test():
    from subprocess import call
    call(['nosetests', '-v',
          '--with-coverage', '--cover-package=app', '--cover-branches',
          '--cover-erase', '--cover-html', '--cover-html-dir=cover'])


@manager.command
def adduser(email, password=None, admin=False):
    """Register a new user."""
    if not password:
        from getpass import getpass
        password = getpass()
        password2 = getpass(prompt='Confirm: ')
        if password != password2:
            import sys
            sys.exit('Error: passwords do not match.')
    db.create_all()
    user = User(email=email, password=password, is_admin=admin)
    db.session.add(user)
    db.session.commit()
    print('User {0} was registered successfully.'.format(email))


@manager.command
def removeuser(email):
    """Remove user by email"""
    user = User.query.filter_by(email=email).first()
    eyed = int(user.id)
    db.session.delete(user)
    db.session.commit()
    print('User {0} was removed.'.format(eyed))

@manager.command
def dropall():
    db.drop_all()

@manager.command
def createall():
    db.create_all()


if __name__ == '__main__':
    manager.run()

