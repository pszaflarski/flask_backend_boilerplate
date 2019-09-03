from flask import render_template, current_app, request, redirect, url_for, \
    flash

from . import auth
from ..models import User


# from flask_login import login_user


@auth.route('/', methods=['GET', 'POST'])
def login():
    # this is a lot of repetition from the method at the API level
    # it's intentional and only for the boilerplate

    if not current_app.config['DEBUG'] and not current_app.config['TESTING'] \
            and not request.is_secure:
        return redirect(url_for('.login', _external=True, _scheme='https'))

    if request.method == 'POST':
        data = request.form
        email = data.get('email')
        password = data.get('password')

        user = User.query.filter_by(email=email).first()
        if not user:
            flash("auth failed")
            return render_template('auth/login.html')

        if not user.verify_password(password):
            flash("auth failed")
            return render_template('auth/login.html')

        token = user.get_api_token()

        flash(f"your token is: {token}")

    return render_template('auth/login.html')
