from flask_restplus import fields
from .restplus import api

user = api.model('User Model', {
    'id': fields.Integer(readOnly=True, description='id'),
    'email': fields.String(required=True, description='email'),
    'is_admin': fields.Boolean(description='is_admin', default=False),
    'password': fields.String(required=True, description='password')
})
