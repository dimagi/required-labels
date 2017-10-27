from utils import PullRequest
import json

class MockPullRequest(PullRequest):
    def __init__(self, labels_json_file):
        super(MockPullRequest, self).__init__()
        with open(labels_json_file) as f:
            self.labels_json = json.load(f)

    @property
    def labels(self):
        return self.labels_json

    def post_status(self, status_json):
        pass
