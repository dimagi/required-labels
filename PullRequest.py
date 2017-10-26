import requests
from config import GITHUB_USER, GITHUB_PW

class PullRequest(object):
    def __init__(self, event=None):
        self.event = event
        if event is not None:
            self.issue_url = event['pull_request']['issue_url']

    @property
    def label_url(self):
        return "{}/labels".format(self.issue_url)

    @property
    def full_repo_name(self):
        return self.event['pull_request']['head']['repo']['full_name']

    @property
    def head_commit(self):
        return self.event['pull_request']['head']['sha']

    def request_labels_json(self):
        return requests.get(self.label_url, auth=(GITHUB_USER, GITHUB_PW)).json()

    def validate_labels(self, required_any, required_all, banned):
        self_labels_list = [l['name'] for l in self.request_labels_json()]
        if required_any != [''] and not any(l in required_any for l in self_labels_list):
            return False
        if required_all != [''] and any(l not in self_labels_list for l in required_all):
            return False
        if banned != [''] and any(l in self_labels_list for l in banned):
            return False
        return True

    def post_status(self, status_json):
        url = 'https://api.github.com/repos/{full_repo_name}/statuses/{sha}'.format(
            full_repo_name=self.full_repo_name,
            sha=self.head_commit)
        print(url)
        r = requests.post(url, data=status_json)
        return r.status_code

    # for testing
    def set_issue_url(self, url):
        self.issue_url = url