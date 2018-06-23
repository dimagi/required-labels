import os

from flask import Flask, request

from utils import PullRequest
from config import CONFIG

app = Flask(__name__)


@app.route('/', methods=["POST"])
def main():
    event_json = request.get_json()
    if event_warrants_label_check(event_json):
        pull_request = PullRequest(event_json)
        print("Checking labels for PR {}".format(pull_request.issue_url))
        status_code = pull_request.compute_and_post_status(
            CONFIG['required_any'], CONFIG['required_all'], CONFIG['banner'])
        return str(status_code)
    else:
        return 'No label check needed'


@app.route('/config', methods=["GET"])
def config():
    return """
    Any: {}<br/>
    All: {}<br/>
    Banned: {}<br/>
    """.format(CONFIG['required_any'],
               CONFIG['required_all'],
               CONFIG['banner'])


def event_warrants_label_check(pr_event_json):
    try:
        return pr_event_json['action'] in ['opened', 'reopened', 'labeled', 'unlabeled', 'synchronize']
    except KeyError:
        return False


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
