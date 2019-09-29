import os

import pytest
from flask import current_app

from app.main.config import basedir
from app.main.config import DevelopmentConfig
from app.main.config import ProductionConfig
from app.main.config import TestingConfig


def test_config_should_create_development_app_when_used_development_config(create_app_for_test):
    app = create_app_for_test(DevelopmentConfig)

    assert app.config['SECRET_KEY'] != 'my_precious'
    assert app.config['DEBUG'] is True
    assert current_app is not None


def test_config_should_create_test_app_when_used_test_config(create_app_for_test):
    app = create_app_for_test(TestingConfig)

    assert app.config['SECRET_KEY'] != 'my_precious'
    assert app.config['DEBUG'] is True
    assert app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///' + os.path.join(basedir, 'flask_boilerplate_test.db')


def test_config_should_create_production_app_when_used_production_config(create_app_for_test):
    app = create_app_for_test(ProductionConfig)

    assert app.config['DEBUG'] is False


if __name__ == '__main__':
    pytest.main(['app/integrationtest/{}.py'.format(__file__)])
