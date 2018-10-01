import os
import sys
from configparser import ConfigParser, NoSectionError
from pathlib import Path


APP_BASEDIR = Path(os.path.abspath(__file__)).parent
APP_NAME = "dimagi/required-labels"

CONFIG_FILENAME = "custom.conf"

class ConfigException(Exception):
    pass


def generate_config():
    config = {}
    conf = ConfigParser()
    conf.read(_get_config_file())
    try:
        config['required_any'] = conf.get('Labels', 'required-labels-any')
        config['required_all'] = conf.get('Labels', 'required-labels-all')
        config['banned'] = conf.get('Labels', 'banned-labels')
        config['github_user'] = conf.get('GitHub', 'user')
        config['github_pw'] = conf.get('GitHub', 'password')
    except NoSectionError:
        config['required_any'] = os.environ.get('REQUIRED_LABELS_ANY', None)
        config['required_all'] = os.environ.get('REQUIRED_LABELS_ALL', None)
        config['banned'] = os.environ.get('BANNED_LABELS', None)
        config['github_user'] = os.environ.get('GITHUB_USER', None)
        config['github_pw'] = os.environ.get('GITHUB_PW', None)

    for label in ['required_any', 'required_all', 'banned']:
        config[label] = config[label].split(',') if config[label] else None
    return config


def _get_config_file():
    if 'CONFIG_FILE' in os.environ:
        return os.environ['CONFIG_FILE']
    return os.path.join(APP_BASEDIR, CONFIG_FILENAME)


CONFIG = generate_config()


def get_credentials():
    if CONFIG['github_user'] == '' or CONFIG['github_pw'] == '':
        return None
    else:
        return CONFIG['github_user'], CONFIG['github_pw']


UNIT_TESTING = any([arg for arg in sys.argv if 'test' in arg])


if not UNIT_TESTING:
    labels_configured = any([CONFIG['required_any'], CONFIG['required_all'],
                             CONFIG['banned']])
    credentials_configured = all([CONFIG['github_pw'], CONFIG['github_user']])
    if not labels_configured or not credentials_configured:
        raise ConfigException(
            "Please ensure your config file has a [Labels] and [Github] section.\n"
            "Did you forget to create a configuration file?\n"
            "You can do this by running\033[1m cp {0}.template {0} \033[0m\n"
            "You can also add REQUIRED_LABELS_ALL, REQUIRED_LABELS_ANY, or BANNED_LABELS along with "
            "GITHUB_USER and GITHUB_PW as environment variables"
            "".format(CONFIG_FILENAME)
        )

