from flask import current_app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from sqlalchemy.exc import OperationalError
from werkzeug.security import generate_password_hash, check_password_hash

from . import db, login_manager


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), nullable=False, unique=True, index=True)
    is_admin = db.Column(db.Boolean)
    password_hash = db.Column(db.String(128))

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_api_token(self, expiration=300, secret_key=None):
        # There are other ways to create tokens that aren't so long
        # this one just uses the default serializer to get the job done
        if not secret_key:
            s = Serializer(current_app.config['SECRET_KEY'], expiration)
        else:
            s = Serializer(secret_key, expiration)
        return s.dumps({'user': self.id}).decode('utf-8')

    @staticmethod
    def validate_api_token(token, secret_key=None):
        if not secret_key:
            s = Serializer(current_app.config['SECRET_KEY'])
        else:
            s = Serializer(secret_key)
        try:
            data = s.loads(token)
        except:
            return None
        id = data.get('user')
        if id:
            return User.query.get(id)
        return None


@login_manager.user_loader
def load_user(user_id):
    try:
        return User.query.get(int(user_id))
    except OperationalError:
        # This block is probably not needed when you are going to production
        # its only meant to set up a root account so that the app is usable for
        # demo purposes
        import os
        db.create_all()
        email = os.environ.get('ROOT_USER')
        password = os.environ.get('ROOT_PASSWORD')
        user = User(id=1, email=email, password=password, is_admin=True)
        db.session.add(user)
        db.session.commit()
        return User.query.get(int(user_id))

# # Indexing
# Index('user_id_idx', User.id)
