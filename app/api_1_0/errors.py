from flask import jsonify, make_response
from . import api_blueprint


def forbidden(message):
    resp = jsonify({'error': 'forbidden', 'message': message})
    resp.status_code = 403
    return resp


def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)
