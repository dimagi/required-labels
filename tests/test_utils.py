from unittest.mock import patch, MagicMock

from exceptions import NoGitHubTokenException
from utils import PullRequest


class TestPullRequest():
    @patch('utils.Session', MagicMock())
    @patch('utils.get_credentials')
    @patch('utils.get_token')
    def test_it_use_login_token_authentication(self,
                                               get_token,
                                               get_credentials):
        get_credentials.return_value = ('myuser', 'mypass')
        PullRequest({'pull_request': {'issue_url': 'https/github/orga/url/issueurl'}})
        get_token.assert_called_once()
        get_credentials.assert_not_called()

    @patch('utils.Session', MagicMock())
    @patch('utils.get_credentials')
    @patch('utils.get_token')
    def test_it_fallback_to_login_password_authentication_with_no_token(self,
                                                                        get_token,
                                                                        get_credentials):
        get_token.side_effect = NoGitHubTokenException
        PullRequest({'pull_request': {'issue_url': 'https/github/orga/url/issueurl'}})
        get_token.assert_called_once()
        get_credentials.assert_called_once()
