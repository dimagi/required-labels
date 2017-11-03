import os
import sys
from configparser import ConfigParser, NoSectionError


class ConfigException(Exception):
    pass


config_filename = "custom.conf"
config = ConfigParser()
config.read(config_filename)

try:
    required_any = config.get('Labels', 'required-labels-any')
    required_all = config.get('Labels', 'required-labels-all')
    banned = config.get('Labels', 'banned-labels')
    GITHUB_USER = config.get('GitHub', 'user')
    GITHUB_PW = config.get('GitHub', 'password')
except NoSectionError:
    required_any = os.environ.get('REQUIRED_LABELS_ANY', None)
    required_all = os.environ.get('REQUIRED_LABELS_ALL', None)
    banned = os.environ.get('BANNED_LABELS', None)
    GITHUB_USER = os.environ.get('GITHUB_USER', None)
    GITHUB_PW = os.environ.get('GITHUB_PW', None)

REQUIRED_LABELS_ANY = required_any.split(',') if required_any else None
REQUIRED_LABELS_ALL = required_all.split(',') if required_all else None
BANNED_LABELS = banned.split(',') if banned else None


def get_credentials():
    if GITHUB_USER == '' or GITHUB_PW == '':
        return None
    else:
        return GITHUB_USER, GITHUB_PW


UNIT_TESTING = any([arg for arg in sys.argv if 'test' in arg])


if not UNIT_TESTING:
    labels_configured = any([REQUIRED_LABELS_ANY, REQUIRED_LABELS_ALL, BANNED_LABELS])
    credentials_configured = all([GITHUB_PW, GITHUB_USER])
    if not labels_configured and not credentials_configured:
        raise ConfigException(
            "Please ensure your config file has a [Labels] and [Github] section.\n"
            "Did you forget to create a configuration file?\n"
            "You can do this by running\033[1m cp {0}.template {0} \033[0m\n"
            "You can also add REQUIRED_LABELS_ALL, REQUIRED_LABELS_ANY, or BANNED_LABELS along with "
            "GITHUB_USER and GITHUB_PW as environment variables"
            "".format(config_filename)
        )
