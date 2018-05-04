from flask import Blueprint
# __INIT__可以导入上级包

# 选取一样的名字
api_blueprint = Blueprint('api', __name__)

from . import errors, testapi



