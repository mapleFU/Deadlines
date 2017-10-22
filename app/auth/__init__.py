from flask import Blueprint
# __INIT__可以导入上级包

# 选取一样的名字
auth_blueprint = Blueprint('auth', __name__)

from . import views, errors

