from flask_restplus import Api
from flask import Blueprint

from .main.controller.user_controller import api as user_ns

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='API',
          version='0.1',
          description='a web service API'
          )

api.add_namespace(user_ns, path='/user')