import logging

from flask import request
from flask_restplus import Resource

from .restplus import api, admin_token_required
from .serializers import get_user, create_user, get_users, update_user, user_token
from .. import db
from ..models import User

log = logging.getLogger(__name__)

ns_user = api.namespace('user', description='Operations related to User Management')


@ns_user.route('/')
class UserCollection(Resource):

    @api.doc(security='apiKey', model=get_user)
    @admin_token_required
    def get(self):
        """
        Returns list of Users.
        """
        users = User.query.all()
        return api.marshal(users, get_user)

    @api.doc(security='apiKey')
    @api.response(201, 'User successfully created.')
    @api.expect(create_user)
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
        id = user.id
        return {"message": f"User {id} created"}, 201


@ns_user.route('/<int:id>')
@api.response(404, 'User not found.')
class UserItem(Resource):

    @api.doc(security='apiKey', model=get_user)
    @admin_token_required
    def get(self, id):
        """
        Returns a User by id.
        """
        user = User.query.get(id)
        if not user:
            return {'message': 'user not found'}, 404
        return api.marshal(user, get_user)

    @api.expect(update_user)
    @api.response(200, 'User successfully updated.')
    def patch(self, id):
        """
        Update a user
        """
        user = User.query.get(id)
        if not user:
            return {'message': 'user not found'}, 404
        data = request.json
        user.email = data.get('email', user.email)
        user.is_admin = data.get('is_admin', user.is_admin)
        db.session.commit()
        return {"message": f"User {id} updated"}, 200

    @api.response(200, 'Category successfully deleted.')
    def delete(self, id):
        """
        Deletes a user.
        """
        user = User.query.get(id)
        if not user:
            return {'message': 'user not found'}, 404
        user.delete()
        db.session.commit()
        return {"message": f"User {id} deleted"}, 200


@ns_user.route('/token')
class TokenResource(Resource):

    @api.doc(security=None)
    @api.expect(user_token)
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
