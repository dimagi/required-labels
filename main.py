from flask import Flask, request
from utils import PullRequest
from config import REQUIRED_LABELS_ALL, REQUIRED_LABELS_ANY, BANNED_LABELS

app = Flask(__name__)


@app.route('/', methods=["POST"])
def main():
    event_json = request.get_json()
    if event_warrants_label_check(event_json):
        pull_request = PullRequest(event_json)
        status_code = pull_request.compute_and_post_status(REQUIRED_LABELS_ANY, REQUIRED_LABELS_ALL, BANNED_LABELS)
        return str(status_code)
    else:
        return 'No label check needed'


def event_warrants_label_check(pr_event_json):
    return pr_event_json['action'] in ['opened', 'reopened', 'labeled', 'unlabeled']

