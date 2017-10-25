from configparser import ConfigParser

config = ConfigParser()
config.read("custom.conf")

required_any = config.get('Labels', 'required-labels-any')
required_all = config.get('Labels', 'required-labels-all')
banned = config.get('Labels', 'banned-labels')

REQUIRED_LABELS_ANY = '' if required_any is '' else required_any.split(',')
REQUIRED_LABELS_ALL = '' if required_all is '' else required_all.split(',')
BANNED_LABELS = '' if banned is '' else banned.split(',')

GITHUB_USER = config.get('GitHub', 'user')
GITHUB_PW = config.get('GitHub', 'password')