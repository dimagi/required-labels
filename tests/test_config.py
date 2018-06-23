import os
import unittest
from unittest.mock import patch

from config import generate_config, APP_BASEDIR


class TestGenerateConfig(unittest.TestCase):
    @patch('config.ConfigParser')
    def test_it_reads_default_config_file(self, configparser):
        generate_config()
        configparser.return_value.read.assert_called_once_with(
            os.path.join(APP_BASEDIR, 'custom.conf'))

    @patch('config.ConfigParser')
    def test_it_reads_given_config_file_from_environment_var(self,
                                                             configparser):
        with patch.dict(os.environ, {'CONFIG_FILE': '/someconf'}):
            generate_config()
            configparser.return_value.read.assert_called_once_with('/someconf')

    def test_it_source_config_from_environment_with_missing_conf(self):
        with patch.dict(os.environ, {'CONFIG_FILE': '/conf/notexist',
                                     'GITHUB_USER': 'ghuser'}):
            config = generate_config()
            assert config['github_user'] == 'ghuser'

    def test_it_source_config_from_given_config_file(self):
        fixture_config = os.path.join(APP_BASEDIR, 'tests', 'fixtures',
                                      'custom.conf.test')
        with patch.dict(os.environ, {'CONFIG_FILE': fixture_config}):
            config = generate_config()
            assert config['github_user'] == 'someuser'
