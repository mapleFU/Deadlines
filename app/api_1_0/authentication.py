from flask import current_app, g, make_response, jsonify
from werkzeug.security import generate_password_hash
from flask_httpauth import HTTPBasicAuth
from . import api_blueprint
from ..model import User

auth = HTTPBasicAuth()


# config auth
@auth.verify_password
def verify_pw(username_or_token, password=None):
    """
    :param username_or_token: it's a user name or token of http auth
    :param password: pwd of a user
    :return: pwd
    """
    if password is None:
        token = username_or_token
        user = User.verify_token(token)
    else:
        username = username_or_token
        user = User.query.filter_by(username=username).first()
        if not user.verify_password(password=password):
            return False
    # judge
    if user is None:
        return False
    else:
        g.current_user = user
        return True


@api_blueprint.before_request
@auth.login_required
def before_request():
    print('before requests')
    if not g.current_user.is_anonymous\
            and not g.current_user.is_authenticated:
        return unauthorized()


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)


@api_blueprint.route('/token')
def get_token():
    if g.current_user.is_anonymous or \
            g.token_used:
        return unauthorized("invalid credentials")
    return jsonify({
        "token": g.current_user.generate_token(expiration=3600),
        "expiration": 3600
                    })
