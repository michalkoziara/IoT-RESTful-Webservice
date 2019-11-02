import os


class Constants:
    LOGGER_LEVEL_OFF = os.environ.get('LOGGER_LEVEL_OFF')

    CURRENT_ENV = os.environ.get('APP_ENV', 'dev')

    DATABASE_URL_PROD = os.environ.get('DATABASE_URL')
    DATABASE_URL_TEST = 'sqlite:///' + os.path.join(
        os.path.abspath(os.path.dirname(__file__)), 'flask_boilerplate_test.db')
    SECRET_KEY = os.getenv('SECRET_KEY', 'secret_key')

    RESPONSE_MESSAGE_ADMIN_NOT_DEFINED = 'Admin not defined.'
    RESPONSE_MESSAGE_BAD_MIMETYPE = (
        'The browser (or proxy) sent a request with mimetype that does not indicate JSON data.')
    RESPONSE_MESSAGE_BAD_REQUEST = 'The browser (or proxy) sent a request that this server could not understand.'
    RESPONSE_MESSAGE_CONFLICTING_DATA = 'The browser (or proxy) sent a request with conflicting data.'
    RESPONSE_MESSAGE_CREATED = 'Created'
    RESPONSE_MESSAGE_DEVICE_KEYS_NOT_LIST = 'Devices keys must be non-empty list.'
    RESPONSE_MESSAGE_DEVICE_KEY_NOT_FOUND = 'Device key was not found.'
    RESPONSE_MESSAGE_DEVICE_STATES_NOT_FOUND = 'Devices states not found'
    RESPONSE_MESSAGE_DEVICE_STATES_NOT_LIST = 'Devices states must be a list of dictionaries'
    RESPONSE_MESSAGE_DUPLICATE_FORMULA_NAME = 'Formula with given name already exists.'
    RESPONSE_MESSAGE_ERROR = 'Server encountered an unexpected condition that prevented it from fulfilling the request.'
    RESPONSE_MESSAGE_EXECUTIVE_DEVICE_NAME_ALREADY_DEFINED = 'Executive device name already defined in device group.'
    RESPONSE_MESSAGE_EXECUTIVE_DEVICE_NOT_FOUND = 'Executive device not found'
    RESPONSE_MESSAGE_EXECUTIVE_TYPE_NAME_NOT_DEFINED = 'Executive device type name not defined.'
    RESPONSE_MESSAGE_EXECUTIVE_TYPE_ALREADY_EXISTS = 'Executive type with given name already exists.'
    RESPONSE_MESSAGE_EXECUTIVE_TYPE_NOT_FOUND = 'Executive type name not found.'
    RESPONSE_MESSAGE_FORMULA_NOT_FOUND = 'Formula name not found.'
    RESPONSE_MESSAGE_INVALID_CREDENTIALS = 'User credentials are invalid.'
    RESPONSE_MESSAGE_INVALID_FORMULA = 'Formula is invalid.'
    RESPONSE_MESSAGE_INVALID_TOKEN = 'Invalid token.'
    RESPONSE_MESSAGE_LOGGER_LEVEL_OFF = 'Errors logging is disabled.'
    RESPONSE_MESSAGE_OK = 'OK'
    RESPONSE_MESSAGE_PARTIALLY_WRONG_DATA = 'Hub send partially wrong data'
    RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND = 'Product key was not found.'
    RESPONSE_MESSAGE_SENSORS_READINGS_NOT_FOUND = 'Sensors readings not found'
    RESPONSE_MESSAGE_SENSORS_READINGS_NOT_LIST = 'Sensors readings must be a list of dictionaries'
    RESPONSE_MESSAGE_SENSOR_NAME_ALREADY_DEFINED = 'Sensor name already defined in device group.'
    RESPONSE_MESSAGE_SENSOR_NOT_FOUND = 'Sensor not found'
    RESPONSE_MESSAGE_SENSOR_TYPE_ALREADY_EXISTS = 'Sensor type with given name already exists.'
    RESPONSE_MESSAGE_SENSOR_TYPES_NOT_FOUND = 'Sensor types name not found.'
    RESPONSE_MESSAGE_SENSOR_TYPE_NAME_NOT_DEFINED = 'Sensor type name not defined.'
    RESPONSE_MESSAGE_SENSOR_TYPE_NOT_FOUND = 'Sensor type name not found.'
    RESPONSE_MESSAGE_SIGNATURE_EXPIRED = 'Signature expired.'
    RESPONSE_MESSAGE_UNCONFIGURED_DEVICE_NOT_FOUND = 'Unconfigure device not found.'
    RESPONSE_MESSAGE_UPDATED_SENSORS_AND_DEVICES = 'States of devices and readings of sensors were updated'
    RESPONSE_MESSAGE_USER_ALREADY_EXISTS = 'User with given credentials already exists.'
    RESPONSE_MESSAGE_USER_DOES_NOT_HAVE_PRIVILEGES = 'User does not have necessary privileges.'
    RESPONSE_MESSAGE_USER_GROUP_ALREADY_EXISTS = 'User group with given name already exists.'
    RESPONSE_MESSAGE_USER_GROUP_NAME_NOT_FOUND = 'User group name was not found.'
    RESPONSE_MESSAGE_USER_GROUP_NOT_DEFINED = 'User group was not found.'
    RESPONSE_MESSAGE_USER_NOT_DEFINED = 'User not defined.'
    RESPONSE_MESSAGE_USER_ALREADY_IN_USER_GROUP = 'User already is a member of user group.'
    RESPONSE_MESSAGE_WRONG_DATA = 'Hub send wrong data'
    RESPONSE_MESSAGE_WRONG_PASSWORD = 'Wrong password.'
