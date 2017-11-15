from flask import Blueprint
# __INIT__可以导入上级包

# 选取一样的名字
mail_blueprint = Blueprint('mail', __name__)

from . import views, errors

