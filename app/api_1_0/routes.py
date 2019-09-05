import logging

from flask import request
from flask_restplus import Resource
from flask_restplus import fields

from .restplus import api, token_required, admin_token_required
from .serializers import user
from .. import db
from ..models import User

log = logging.getLogger(__name__)

ns_user = api.namespace('user', description='Operations related to User Management')

@ns_user.route('/')
class UserCollection(Resource):

    @api.doc(security='apiKey')
    @admin_token_required
    def get(self):
        """
        Returns list of Users.
        """

        users = User.query.all()
        return api.marshal(
            users,
            api.model('List Users Model', {
                'id': fields.Integer(description='id'),
                'email': fields.String(description='email'),
                'is_admin': fields.Boolean(description='user is admin')
            }))

    @api.doc(security='apiKey')
    @api.response(201, 'User successfully created.')
    @api.expect(api.model('Create User Model', {
        'email': fields.String(required=True, description='email'),
        'password': fields.String(required=True, description='password'),
        'is_admin': fields.Boolean(default=False, description='user is admin')
    }))
    @admin_token_required
    def post(self):
        """
        Creates a new User.
        """
        data = request.json
        email = data.get('email')
        is_admin = data.get('is_admin', False)
        password = data.get('password')
        user = User(email=email, password=password, is_admin=is_admin)

        db.session.add(user)
        db.session.commit()
        return None, 201


@ns_user.route('/<int:id>')
@api.response(404, 'User not found.')
class UserItem(Resource):

    @api.doc(security='apiKey')
    @token_required
    def get(self, id):
        """
        Returns a User by id.
        """
        user = User.query.get(id)

        if not user:
            return {'message': 'user not found'}, 404

        return api.marshal(
            user,
            api.model('List Users Model', {
                'id': fields.Integer(description='id'),
                'email': fields.String(description='email'),
                'is_admin': fields.Boolean(description='user is admin')
            }))

    # @api.expect(user)
    @api.response(204, 'User successfully updated.')
    def put(self, id):
        """
        Update a user
        """
        # data = request.json
        # update_user(id, data)
        return None, 204

    @api.response(204, 'Category successfully deleted.')
    def delete(self, id):
        """
        Deletes a user.
        """
        # delete_user(id)
        return None, 204


@ns_user.route('/token')
class TokenResource(Resource):
    model = api.model('Login User Model', {
        'email': fields.String(required=True, description='email'),
        'password': fields.String(required=True, description='password'),
        'ttl': fields.Integer(description='time token will be valid in seconds', default=300)
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
        ttl = data.get('ttl', 300)

        user = User.query.filter_by(email=email).first()
        if not user:
            return None, 401

        if not user.verify_password(password):
            return None, 401

        token = user.get_api_token(expiration=ttl)

        return {'X-API-KEY': token}, 200