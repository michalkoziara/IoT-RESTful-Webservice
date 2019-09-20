import os
import logging

import pytest
from flask import url_for
from flask_migrate import Migrate
from flask_migrate import MigrateCommand
from flask_script import Manager

from app import api
from app.main import create_app
from app.main import db
from app.main.model.device_group import DeviceGroup
from app.main.model.enumerator_value import EnumeratorValue
from app.main.model.executive_device import ExecutiveDevice
from app.main.model.executive_type import ExecutiveType
from app.main.model.formula import Formula
from app.main.model.log import Log
from app.main.model.sensor import Sensor
from app.main.model.sensor_reading import SensorReading
from app.main.model.sensor_type import SensorType
from app.main.model.unconfigured_device import UnconfiguredDevice
from app.main.model.user import User
from app.main.model.user_group import UserGroup
from app.main.model.user_group_member import user_group_member

current_env = os.environ.get('APP_ENV', 'dev')

app = create_app(current_env)
app.register_blueprint(api)

app.app_context().push()

manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)


@manager.command
def run():
    app.run()


@manager.command
def test():
    """Runs all tests."""
    if pytest.main(["app/test/",
                    "--cache-clear"]):
        return 0
    return 1


@manager.command
def testunit():
    """Runs the unit tests."""
    if pytest.main(["app/test/unittest"]):
        return 0
    return 1


@manager.command
def testintegration():
    """Runs the integration tests."""
    if pytest.main(["app/test/integrationtest",
                    "--cache-clear"]):
        return 0
    return 1


@manager.command
def routes():
    import urllib
    output = []
    for rule in app.url_map.iter_rules():

        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)

        methods = ','.join(rule.methods)
        url = url_for(rule.endpoint, **options)
        line = urllib.parse.unquote(
            "{:50s} {:20s} {}".format(rule.endpoint, methods, url))
        output.append(line)

    for line in sorted(output):
        print(line)


if __name__ == '__main__':
    manager.run()
