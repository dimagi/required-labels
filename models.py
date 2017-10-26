import requests
from config import get_credentials


class PullRequest(object):
    def __init__(self, event=None):
        self.event = event
        if event is not None:
            self.issue_url = event['pull_request']['issue_url']

    @property
    def labels(self):
        return self.request_labels_json()

    def request_labels_json(self):
        return requests.get(self.label_url, auth=get_credentials()).json()

    @property
    def label_url(self):
        return "{}/labels".format(self.issue_url)

    def post_status(self, status_json):
        url = 'https://api.github.com/repos/{full_repo_name}/statuses/{sha}'.format(
            full_repo_name=self.full_repo_name,
            sha=self.head_commit)
        r = requests.post(url, data=status_json, auth=get_credentials())
        return r.status_code

    @property
    def full_repo_name(self):
        return self.event['pull_request']['head']['repo']['full_name']

    @property
    def head_commit(self):
        return self.event['pull_request']['head']['sha']

    def validate_labels(self, required_any, required_all, banned):
        labels_list = [l['name'] for l in self.labels]
        if required_any != '' and not any(l in required_any for l in labels_list):
            return False
        if required_all != '' and any(l not in labels_list for l in required_all):
            return False
        if banned != '' and any(l in labels_list for l in banned):
            return False
        return True
