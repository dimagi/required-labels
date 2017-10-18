import requests
import json
from flask import Flask
app = Flask(__name__)

REQUIRED_LABELS = ['ready for review']

@app.route('/')
def main():
    pr_number = '1858' # will come from PR event listener
    labels_json = get_labels_for_pr(pr_number)
    return create_status_json(pr_number, any(l['name'] in REQUIRED_LABELS for l in labels_json))


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


def get_labels_for_pr(pr_number):
    # https://api.github.com/repos/dimagi/commcare-android/issues/{PR#}/labels
    url = 'https://api.github.com/repos/dimagi/commcare-android/issues/{}/labels'.format(pr_number)
    response = requests.get(url)
    return response.json()