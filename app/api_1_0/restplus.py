import logging
import traceback
from functools import wraps

from flask import current_app, request
from flask_login import login_user, current_user
from flask_restplus import Api
from sqlalchemy.orm.exc import NoResultFound

from ..models import User

log = logging.getLogger(__name__)

authorizations = {
    'apiKey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'X-API-KEY'
    }
}

api = Api(
    version='1.0',
    title='Boilerplate Flask Backend',
    description='A starting point for apps using Flask, Swagger and the App Factory Pattern',
    security='Bearer Auth',
    authorizations=authorizations
)


def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.headers.get('X-API-KEY')
        if not token:
            return {'message': 'token is missing'}, 401
        user = User.validate_api_token(token)
        if user:
            login_user(user)
            log.debug('User token validated')
        else:
            return {'message': 'invalid token'}, 401
        return func(*args, **kwargs)

    return decorated


def admin_token_required(func):
    @token_required
    @wraps(func)
    def decorated(*args, **kwargs):
        if not current_user.is_admin:
            return {'message': 'admin access required'}, 403
        return func(*args, **kwargs)

    return decorated


@api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'
    log.exception(message)

    if not current_app.config['FLASK_DEBUG']:
        return {'message': message}, 500


@api.errorhandler(NoResultFound)
def database_not_found_error_handler(e):
    log.warning(traceback.format_exc())
    return {'message': 'A database result was required but none was found.'}, 404
