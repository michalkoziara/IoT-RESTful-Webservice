import os


class Constants:
    RESPONSE_MESSAGE_WRONG_DATA = "Hub device send wrong data"
    RESPONSE_MESSAGE_PARTIALLY_WRONG_DATA = "Hub device send partially wrong data"
    LOGGER_LEVEL_OFF = os.environ.get('LOGGER_LEVEL_OFF')

    CURRENT_ENV = os.environ.get('APP_ENV', 'dev')

    DATABASE_URL_PROD = os.environ.get('DATABASE_URL')
    DATABASE_URL_TEST = 'sqlite:///' + os.path.join(
        os.path.abspath(os.path.dirname(__file__)), 'flask_boilerplate_test.db')
    SECRET_KEY = os.getenv('SECRET_KEY', 'secret_key')

    RESPONSE_MESSAGE_ERROR = 'Server encountered an unexpected condition that prevented it from fulfilling the request.'
    RESPONSE_MESSAGE_BAD_REQUEST = 'The browser (or proxy) sent a request that this server could not understand.'
    RESPONSE_MESSAGE_CONFLICTING_DATA = 'The browser (or proxy) sent a request with conflicting data.'
    RESPONSE_MESSAGE_BAD_MIMETYPE = (
        'The browser (or proxy) sent a request with mimetype that does not indicate JSON data.')
    RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND = 'Product key was not found.'
    RESPONSE_MESSAGE_DEVICE_KEY_NOT_FOUND = 'Device key was not found.'
    RESPONSE_MESSAGE_USER_GROUP_NAME_NOT_FOUND = 'User group name was not found.'
    RESPONSE_MESSAGE_USER_GROUP_NOT_DEFINED = 'User group was not found.'
    RESPONSE_MESSAGE_USER_DOES_NOT_HAVE_PRIVILEGES = 'User does not have necessary privileges.'
    RESPONSE_MESSAGE_INVALID_CREDENTIALS = 'User credentials are invalid.'
    RESPONSE_MESSAGE_USER_NOT_DEFINED = 'User not defined.'
    RESPONSE_MESSAGE_SENSOR_TYPE_NAME_NOT_DEFINED = 'Sensor type name not defined.'
    RESPONSE_MESSAGE_SENSOR_TYPE_NOT_FOUND = 'Sensor type name not found.'
    RESPONSE_MESSAGE_USER_ALREADY_EXISTS = 'User with given credentials already exists.'
    RESPONSE_MESSAGE_SIGNATURE_EXPIRED = 'Signature expired.'
    RESPONSE_MESSAGE_INVALID_TOKEN = 'Invalid token.'
    RESPONSE_MESSAGE_SENSORS_READINGS_NOT_FOUND = 'Sensors readings not found'
    RESPONSE_MESSAGE_DEVICE_STATES_NOT_FOUND = 'Devices states not found'
    RESPONSE_MESSAGE_SENSORS_READINGS_NOT_LIST = 'Sensors readings must be a list of dictionaries'
    RESPONSE_MESSAGE_DEVICE_STATES_NOT_LIST = 'Devices states must be a list of dictionaries'
    RESPONSE_MESSAGE_UPDATED_SENSORS_AND_DEVICES = "States of devices and readings of sensors were updated"
    RESPONSE_MESSAGE_OK = 'OK'
