from .feedback_store import FeedbackStore
from collections import Counter

class FeedbackAnalyzer:
    def __init__(self, store=None):
        self.store = store or FeedbackStore()

    def get_outcome_stats(self):
        feedbacks = self.store.load_feedback()
        outcomes = [fb["outcome"] for fb in feedbacks if "outcome" in fb]
        return Counter(outcomes)

    def recent_feedback(self, n=5):
        feedbacks = self.store.load_feedback()
        return feedbacks[-n:] 