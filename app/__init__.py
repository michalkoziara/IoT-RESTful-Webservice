import os

from flask_restplus import Api, Namespace, Resource, fields
from flask import Blueprint

from .main.controller.user_controller import api as user_ns

blueprint = Blueprint('api', __name__)

if (os.environ.get('APP_ENV', 'dev') == 'prod'):
    @property
    def specs_url(self):
        return url_for(self.endpoint('specs'), _external=True, _scheme='https')

    Api.specs_url = specs_url

api = Api(blueprint,
          title='API',
          version='0.1',
          description='a web service API'
          )

api.add_namespace(user_ns, path='/user')
