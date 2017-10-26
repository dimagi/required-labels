from configparser import ConfigParser

config = ConfigParser()
config.read("custom.conf")

required_any = config.get('Labels', 'required-labels-any')
required_all = config.get('Labels', 'required-labels-all')
banned = config.get('Labels', 'banned-labels')

REQUIRED_LABELS_ANY = '' if required_any == '' else required_any.split(',')
REQUIRED_LABELS_ALL = '' if required_all == '' else required_all.split(',')
BANNED_LABELS = '' if banned == '' else banned.split(',')
GITHUB_USER = config.get('GitHub', 'user')
GITHUB_PW = config.get('GitHub', 'password')


def get_credentials():
    if GITHUB_USER == '' or GITHUB_PW == '':
        return None
    else:
        return GITHUB_USER, GITHUB_PW
