import os

from flask_restplus import Api, Namespace, Resource, fields
from flask import Blueprint, url_for

from .main.controller.user_controller import api as user_ns

blueprint = Blueprint('api', __name__)

class MyApi(Api):
    @property
    def specs_url(self):
        """Monkey patch for HTTPS"""
        scheme = 'https' if os.environ.get('APP_ENV', 'dev') == 'prod' else 'http'
        return url_for(self.endpoint('specs'), _external=True, _scheme=scheme)

api = MyApi(blueprint,
          doc='/doc/',
          title='API',
          version='0.1',
          description='a web service API'
          )

api.add_namespace(user_ns, path='/user')
