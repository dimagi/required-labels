import json
from requests import Session

from config import get_credentials, APP_NAME


session = Session()
session.auth = get_credentials()
session.headers.update({"User-Agent": APP_NAME})


class PullRequest(object):
    def __init__(self, event=None):
        self.event = event
        if event is not None:
            self.issue_url = event['pull_request']['issue_url']

    @property
    def labels(self):
        return self.request_labels_json()

    def request_labels_json(self):
        r = session.get(self.label_url)
        if r.status_code >= 300:
            print("Got a non-2xx status: ", r.url, r.headers, r.content)
        return r.json()

    @property
    def label_url(self):
        return "{}/labels".format(self.issue_url)

    def compute_and_post_status(self, required_any, required_all, banned):
        return self.post_status(self.create_status_json(required_any, required_all, banned))

    def post_status(self, status_json):
        r = session.post(self.statuses_url, data=status_json)
        return r.status_code

    @property
    def statuses_url(self):
        return self.event['pull_request']['statuses_url']

    def create_status_json(self, required_any, required_all, banned):
        passes_label_requirements = self.validate_labels(required_any, required_all, banned)
        if passes_label_requirements:
            description = "Label requirements satisfied."
        else:
            description = "Label requirements not satisfied."
        response_json = {
            "state": "success" if passes_label_requirements else "failure",
            "target_url": "",
            "description": description,
            "context": APP_NAME,
        }
        return json.dumps(response_json)

    def validate_labels(self, required_any, required_all, banned):
        try:
            labels_json = self.labels
            labels_list = [l['name'] for l in labels_json]
            if required_any is not None and not any(l in required_any for l in labels_list):
                return False
            if required_all is not None and any(l not in labels_list for l in required_all):
                return False
            if banned is not None and any(l in labels_list for l in banned):
                return False
            return True
        except TypeError:
            print('self.labels was of unexpected format for PR event {}: {}'.format(self.issue_url, labels_json))
            return False
