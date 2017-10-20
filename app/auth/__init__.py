from flask import Blueprint
# __INIT__可以导入上级包

auth_blueprint = Blueprint('login', __name__)

from . import views, errors
