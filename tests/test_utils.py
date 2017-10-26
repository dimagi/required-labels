from models import PullRequest
import json

class MockPullRequest(PullRequest):
    def __init__(self, labels_json_file):
        PullRequest.__init__(self)
        self.labels_json = json.load(open(labels_json_file))

    @property
    def labels(self):
        return self.labels_json

    def post_status(self, status_json):
        pass
