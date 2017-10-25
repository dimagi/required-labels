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
    def labels(self):
        return requests.get(self.label_url, auth=(GITHUB_USER, GITHUB_PW)).json()

    def validate_labels(self, required_any, required_all, banned):
        #print("labels for this pr: {}".format(str(self.labels)))
        if required_any != '' and not any(l['name'] in required_any for l in self.labels):
            return False
        if required_all != '' and any(l not in self.labels for l in required_all):
            return False
        if banned != '' and any(l in self.labels for l in banned):
            return False
        return True

    # for testing
    def set_issue_url(self, url):
        self.issue_url = url