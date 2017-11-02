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
    REQUIRED_LABELS_ANY = required_any.split(',') if required_any else None
    REQUIRED_LABELS_ALL = required_all.split(',') if required_all else None
    BANNED_LABELS = banned.split(',') if banned else None
    GITHUB_USER = config.get('GitHub', 'user')
    GITHUB_PW = config.get('GitHub', 'password')
except NoSectionError:
    raise ConfigException(
        "Please ensure your config file has a [Labels] and [Github] section.\n"
        "Did you forget to create a configuration file?\n"
        "You can do this by running\033[1m cp {0}.template {0} \033[0m".format(config_filename)
    )


def get_credentials():
    if GITHUB_USER == '' or GITHUB_PW == '':
        return None
    else:
        return GITHUB_USER, GITHUB_PW
