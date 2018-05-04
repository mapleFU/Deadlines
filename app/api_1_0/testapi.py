from . import api_blueprint
from flask import jsonify, current_app, g
from .authentication import auth


@api_blueprint.route('/test', methods=["GET"])
@auth.login_required
def test():
    # current_app.logger.log("你去死吧")
    return jsonify({
        # "yourID": g.current_user.username,
        "hello": True
    })
