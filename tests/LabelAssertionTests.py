import unittest
import json
from PullRequest import PullRequest

NO_LABELS = ['']
MOBILE_PRODUCT_LABELS = ['product/all-users', 'product/custom', 'product/invisible', 'product/internal-or-flagged']
MULTIPLE_LABELS = ['cross requested', 'product/internal-or-flagged', 'ready for review']

# labels on this PR are: product/invisible
PR_1857_URL = 'https://api.github.com/repos/dimagi/commcare-android/issues/1857'
# labels on this PR are: cross requested, minor (quick review), product/internal-or-flagged, ready for review
PR_1858_URL = 'https://api.github.com/repos/dimagi/commcare-android/issues/1858'
# labels on this PR are: bug, ready for review
PR_1783_URL = 'https://api.github.com/repos/dimagi/commcare-android/issues/1783'
# labels on this PR are: cross requested, ready for review
PR_1830_URL = 'https://api.github.com/repos/dimagi/commcare-android/issues/1830'

# To run (from parent directory): $ python -m unittest tests.LabelAssertionTests
class LabelAssertionTests(unittest.TestCase):

    def test_pr_with_no_labels_no_requirements(self):
        pr = init_pr_with_event_json('./tests/pr_event_no_labels.json')
        self.assertTrue(pr.validate_labels(NO_LABELS, NO_LABELS, NO_LABELS))

    def test_required_any_passes(self):
        pr = init_pr_with_issue_url(PR_1857_URL)
        self.assertTrue(pr.validate_labels(required_any=MOBILE_PRODUCT_LABELS, required_all=NO_LABELS, banned=NO_LABELS))

    def test_required_any_fails(self):
        pr = init_pr_with_issue_url(PR_1783_URL)
        self.assertFalse(pr.validate_labels(required_any=MOBILE_PRODUCT_LABELS, required_all=NO_LABELS, banned=NO_LABELS))

    def test_banned_passes(self):
        pr = init_pr_with_issue_url(PR_1783_URL)
        self.assertTrue(pr.validate_labels(required_any=NO_LABELS, required_all=NO_LABELS, banned=MOBILE_PRODUCT_LABELS))

    def test_banned_fails(self):
        pr = init_pr_with_issue_url(PR_1858_URL)
        self.assertFalse(pr.validate_labels(required_any=NO_LABELS, required_all=NO_LABELS, banned=MOBILE_PRODUCT_LABELS))

    # This test is currently failing
    def test_all_passes(self):
        pr = init_pr_with_issue_url(PR_1858_URL)
        self.assertTrue(pr.validate_labels(required_any=NO_LABELS, required_all=MULTIPLE_LABELS, banned=NO_LABELS))

    def test_all_fails(self):
        pr = init_pr_with_issue_url(PR_1830_URL)
        self.assertFalse(pr.validate_labels(required_any=NO_LABELS, required_all=MULTIPLE_LABELS, banned=NO_LABELS))


def init_pr_with_event_json(filename):
    with open(filename) as json_file:
        return PullRequest(json.load(json_file))


def init_pr_with_issue_url(url):
    pr = PullRequest()
    pr.set_issue_url(url)
    return pr


if __name__ == '__main__':
    unittest.main()