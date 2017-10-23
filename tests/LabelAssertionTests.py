import unittest
import json
from PullRequest import PullRequest

NO_LABELS = ''
ONE_LABEL = ['label_1']
TWO_LABELS = ['label_2, label_3']


# To run (from parent directory): $ python -m unittest tests.LabelAssertionTests
class LabelAssertionTests(unittest.TestCase):

    def test_pr_with_no_labels_no_requirements(self):
        pr = init_pr_with_event_json('./tests/pr_event_no_labels.json')
        self.assertTrue(pr.validate_labels(NO_LABELS, NO_LABELS, NO_LABELS))

    def test_pr_with_no_labels_some_requirements(self):
        pr = init_pr_with_event_json('./tests/pr_event_no_labels.json')
        self.assertFalse(pr.validate_labels(required_any=TWO_LABELS, required_all=ONE_LABEL, banned=NO_LABELS))


def init_pr_with_event_json(filename):
    with open(filename) as json_file:
        return PullRequest(json.load(json_file))


def init_pr_with_issue_url(url):
    pr = PullRequest()
    pr.set_issue_url(url)
    return pr


if __name__ == '__main__':
    unittest.main()