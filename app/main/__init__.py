from flask import Blueprint


# __INIT__可以导入上级包

main_blueprint = Blueprint('main', __name__)


__all__ = ['errors', 'forms', 'views']


from . import views, errors
