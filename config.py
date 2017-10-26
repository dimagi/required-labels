from configparser import ConfigParser

config = ConfigParser()
config.read("custom.conf")

REQUIRED_LABELS_ANY = config.get('Labels', 'required-labels-any').split(',')
REQUIRED_LABELS_ALL = config.get('Labels', 'required-labels-all').split(',')
BANNED_LABELS = config.get('Labels', 'banned-labels').split(',')
GITHUB_USER = config.get('GitHub', 'user')
GITHUB_PW = config.get('GitHub', 'password')