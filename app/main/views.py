from . import main_blueprint
from flask import render_template


# print('main/views imported')


@main_blueprint.route('/')
def index():
    return render_template('base.html')


@main_blueprint.route('/DeadBlue')
def dead_blue():
    return render_template('base1.html')

