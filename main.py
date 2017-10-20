import requests
import json
from flask import Flask, request
app = Flask(__name__)

REQUIRED_LABELS = ['ready for review']

# config = {
#     "all": ["label1", "label2"],
#     "not": ["label3"],
#     "any": ["label4", "label5"]
# }


@app.route('/', methods=["POST"])
def main():
    pull_request = PullRequest(request.get_json())
    return create_status_json(any(l['name'] in REQUIRED_LABELS for l in pull_request.labels))


def create_status_json(has_required_labels):
    if has_required_labels:
        description = "Your PR has the necessary labels"
    else:
        description = "Your PR requires 1 of the following labels: {}".format(", ".join(REQUIRED_LABELS))
    response_json = {
        "state": "success" if has_required_labels else "failure",
        "target_url": "",
        "description": description,
        "context": "Required-Labels Status Checker"
    }
    return json.dumps(response_json)


class PullRequest(object):
    def __init__(self, event):
        self.event = event

    @property
    def label_url(self):
        return "{}/labels".format(self.event['pull_request']['issue_url'])

    @property
    def labels(self):
        return requests.get(self.label_url).json()
