import os


class Constants:
    LOGGER_OFF = os.environ.get('LOGGER_OFF')
    CURRENT_ENV = os.environ.get('APP_ENV', 'dev')
    DATABASE_URL_PROD = os.environ.get('DATABASE_URL')
    DATABASE_URL_TEST = 'sqlite:///' + \
        os.path.join(os.path.abspath(os.path.dirname(__file__)), 'flask_boilerplate_test.db')
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious_secret_key')
