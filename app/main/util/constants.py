import os


class Constants:
    LOGGER_OFF = os.environ.get('LOGGER_OFF')

    CURRENT_ENV = os.environ.get('APP_ENV', 'dev')

    DATABASE_URL_PROD = os.environ.get('DATABASE_URL')
    DATABASE_URL_TEST = 'sqlite:///' + \
        os.path.join(os.path.abspath(os.path.dirname(__file__)), 'flask_boilerplate_test.db')
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious_secret_key')

    RESPONSE_MESSAGE_BAD_REQUEST = 'The browser (or proxy) sent a request that this server could not understand.'
    RESPONSE_MESSAGE_CONFLICTING_DATA = 'The browser (or proxy) sent a request with conflicting data.'
    RESPONSE_MESSAGE_BAD_MIMETYPE =\
        'The browser (or proxy) sent a request with mimetype that does not indicate JSON data.'
