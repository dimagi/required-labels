import json
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

    def compute_and_post_status(self, required_any, required_all, banned):
        return self.post_status(self.create_status_json(required_any, required_all, banned))

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

    def create_status_json(self, required_any, required_all, banned):
        passes_label_requirements = self.validate_labels(required_any, required_all, banned)
        if passes_label_requirements:
            description = "PR has the necessary labels"
        else:
            description = "PR does not pass the label requirements for this repo --> {}".format(
                construct_detailed_failure_message(required_any, required_all, banned))
        response_json = {
            "state": "success" if passes_label_requirements else "failure",
            "target_url": "",
            "description": description,
            "context": "Required-Labels Status Checker"
        }
        return json.dumps(response_json)

    def validate_labels(self, required_any, required_all, banned):
        labels_list = [l['name'] for l in self.labels]
        if required_any is not None and not any(l in required_any for l in labels_list):
            return False
        if required_all is not None and any(l not in labels_list for l in required_all):
            return False
        if banned is not None and any(l in labels_list for l in banned):
            return False
        return True


def construct_detailed_failure_message(required_any, required_all, banned):
    requirement_details = []
    if required_any is not None:
        requirement_details.append('[1 of the following labels: {}]'.format(', '.join(required_any)))
    if required_all is not None:
        requirement_details.append('[all of the following labels: {}]'.format(', '.join(required_all)))
    if banned is not None:
        requirement_details.append('[none of the following labels: {}]'.format(', '.join(banned)))
    return 'Your PR must have: {}'.format(' and '.join(requirement_details))