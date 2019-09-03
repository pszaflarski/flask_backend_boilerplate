import logging

from flask import request
from flask_restplus import Resource
from flask_restplus import fields

from .restplus import api, token_required
from .serializers import user
from .. import db
from ..models import User

log = logging.getLogger(__name__)

ns_user = api.namespace('user', description='Operations related to User Management')


def create_user(data):
    username = data.get('username')
    email = data.get('email')
    is_admin = data.get('is_admin', False)
    password = data.get('password')
    user = User(email=email, username=username, password=password, is_admin=is_admin)

    db.session.add(user)
    db.session.commit()


@ns_user.route('/')
class UserResource(Resource):

    @api.doc(security='apiKey')
    @token_required
    def get(self):
        """
        Returns list of Users.
        """

        @api.marshal_with(user, as_list=True)
        def _get_users():
            return User.query.all()

        users = _get_users()
        return users

    @api.doc(security='apiKey')
    @token_required
    @api.response(201, 'User successfully created.')
    @api.expect(user)
    def post(self):
        """
        Creates a new User.
        """
        data = request.json
        create_user(data)
        return None, 201


@ns_user.route('/token')
class TokenResource(Resource):
    model = api.model('Model', {
        'email': fields.String(required=True, description='email'),
        'password': fields.String(required=True, description='password')
    })

    @api.doc(security=None)
    @api.expect(model)
    def post(self):
        """
        Gets a token from and email and password.
        """
        data = request.json
        email = data.get('email')
        password = data.get('password')

        user = User.query.filter_by(email=email).first()
        if not user:
            return None, 401

        if not user.verify_password(password):
            return None, 401

        token = user.get_api_token()

        return {'X-API-KEY': token}, 200
