import json
from flask import Flask, request
from PullRequest import PullRequest
from config import REQUIRED_LABELS_ALL, REQUIRED_LABELS_ANY, BANNED_LABELS

app = Flask(__name__)


@app.route('/', methods=["POST", "GET"])
def main():
    #pull_request = PullRequest(request.get_json())
    pull_request = PullRequest()
    pull_request.set_issue_url('https://api.github.com/repos/dimagi/commcare-android/issues/1858')
    return str(create_status_json(pull_request, REQUIRED_LABELS_ANY, REQUIRED_LABELS_ALL, BANNED_LABELS))


def create_status_json(pull_request, required_any, required_all, banned):
    passes_label_requirements = pull_request.validate_labels(required_any, required_all, banned)
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


def construct_detailed_failure_message(required_any, required_all, banned):
    requirement_details = []
    if required_any != '':
        requirement_details.append('[1 of the following labels: {}]'.format(', '.join(required_any)))
    if required_all != '':
        requirement_details.append('[all of the following labels: {}]'.format(', '.join(required_all)))
    if banned != '':
        requirement_details.append('[none of the following labels: {}]'.format(', '.join(banned)))
    return 'Your PR must have: {}'.format(' and '.join(requirement_details))

