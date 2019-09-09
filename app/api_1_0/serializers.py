from flask_restplus import fields

from .restplus import api

create_user = api.model('Create User Model', {
    'email': fields.String(required=True, description='email'),
    'password': fields.String(required=True, description='password'),
    'is_admin': fields.Boolean(default=False, description='user is admin')
})

get_user = api.model('Get User Model', {
    'id': fields.Integer(description='id'),
    'email': fields.String(description='email'),
    'is_admin': fields.Boolean(description='user is admin')
})
update_user = api.model('Update User Model', {
    'email': fields.String(description='email'),
    'is_admin': fields.Boolean(description='user is admin')
})

user_token = api.model('User Token Model', {
    'email': fields.String(required=True, description='email'),
    'password': fields.String(required=True, description='password'),
    'ttl': fields.Integer(description='time token will be valid in seconds', default=300)
})
