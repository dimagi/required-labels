from configparser import ConfigParser

config = ConfigParser()
config.read("custom.conf")

required_any = config.get('Labels', 'required-labels-any')
required_all = config.get('Labels', 'required-labels-all')
banned = config.get('Labels', 'banned-labels')

REQUIRED_LABELS_ANY = required_any.split(',') if required_any else None
REQUIRED_LABELS_ALL = required_all.split(',') if required_all else None
BANNED_LABELS = banned.split(',') if banned else None
GITHUB_USER = config.get('GitHub', 'user')
GITHUB_PW = config.get('GitHub', 'password')


def get_credentials():
    if GITHUB_USER == '' or GITHUB_PW == '':
        return None
    else:
        return GITHUB_USER, GITHUB_PW
