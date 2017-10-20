from . import main_blueprint
from flask import render_template


print('main/errors imported')


@main_blueprint.app_errorhandler(404)
def error404(e):
    print('404 was found')
    return render_template('404.html'), 404
