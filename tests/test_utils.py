from unittest.mock import patch, MagicMock

from utils import PullRequest


class TestPullRequest:
    @patch('utils.Session', MagicMock())
    @patch('utils.get_credentials')
    def test_it_use_login_password_authentication(self, get_credentials):
        get_credentials.return_value = ('myuser', 'mypass')
        pull_request = PullRequest({
            'pull_request': {
                'issue_url': 'https/github/orga/url/issueurl'
            }
        })
        get_credentials.assert_called_once()
