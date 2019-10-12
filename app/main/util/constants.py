import os


class Constants:
    LOGGER_LEVEL_OFF = os.environ.get('LOGGER_LEVEL_OFF')

    CURRENT_ENV = os.environ.get('APP_ENV', 'dev')

    DATABASE_URL_PROD = os.environ.get('DATABASE_URL')
    DATABASE_URL_TEST = 'sqlite:///' + \
        os.path.join(os.path.abspath(os.path.dirname(__file__)), 'flask_boilerplate_test.db')
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious_secret_key')

    RESPONSE_MESSAGE_BAD_REQUEST = 'The browser (or proxy) sent a request that this server could not understand.'
    RESPONSE_MESSAGE_CONFLICTING_DATA = 'The browser (or proxy) sent a request with conflicting data.'
    RESPONSE_MESSAGE_BAD_MIMETYPE =\
        'The browser (or proxy) sent a request with mimetype that does not indicate JSON data.'

    RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND = 'Product key was not found'
    RESPONSE_MESSAGE_DEVICE_KEY_NOT_FOUND = 'Device key was not found'
    RESPONSE_MESSAGE_USER_DOES_NOT_HAVE_PRIVILEGES = 'User does not have necessary privileges'
    RESPONSE_MESSAGE_USER_NOT_DEFINED = 'User not defined'
    RESPONSE_MESSAGE_OK = 'OK'

