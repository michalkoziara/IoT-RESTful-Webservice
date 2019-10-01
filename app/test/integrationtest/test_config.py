from unittest.mock import patch

import pytest
from flask import current_app

from app.main.config import DevelopmentConfig
from app.main.config import ProductionConfig
from app.main.config import TestingConfig
from manage import app


@pytest.fixture
def create_app_for_test():
    def _create_app(config):
        app.config.from_object(config)

        return app

    yield _create_app


def test_config_should_create_development_app_when_used_development_config(create_app_for_test):
    test_app = create_app_for_test(DevelopmentConfig)

    assert test_app.config['SECRET_KEY'] != 'my_precious'
    assert test_app.config['DEBUG'] is True
    assert current_app is not None


def test_config_should_create_test_app_when_used_test_config(create_app_for_test):
    database_url = 'database_url'

    with patch.object(TestingConfig, 'SQLALCHEMY_DATABASE_URI', database_url):
        test_app = create_app_for_test(TestingConfig)

    assert test_app.config['SECRET_KEY'] != 'my_precious'
    assert test_app.config['DEBUG'] is True
    assert test_app.config['SQLALCHEMY_DATABASE_URI'] == database_url


def test_config_should_create_production_app_when_used_production_config(create_app_for_test):
    test_app = create_app_for_test(ProductionConfig)

    assert test_app.config['DEBUG'] is False


if __name__ == '__main__':
    pytest.main(['app/integrationtest/{}.py'.format(__file__)])
