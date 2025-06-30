"""
Feedback Collector for Xempla AI Systems Intern Prototype

Collects and processes feedback from AI system decisions and outcomes.
"""
import uuid
import json
from datetime import datetime
from typing import Dict, Any, Optional
from .feedback_store import FeedbackStore


class FeedbackCollector:
    """Collects feedback from AI system decisions and outcomes"""
    
    def __init__(self, store: Optional[FeedbackStore] = None):
        """Initialize the feedback collector
        
        Args:
            store: Optional feedback store instance. If None, creates a new one.
        """
        self.store = store or FeedbackStore()
    
    def collect(
        self,
        decision: str,
        context: Dict[str, Any],
        outcome: str,
        metrics: Dict[str, Any],
        user_id: Optional[str] = None,
        confidence: Optional[float] = None,
        execution_time: Optional[float] = None
    ) -> str:
        """Collect feedback for a decision
        
        Args:
            decision: The decision or action taken
            context: Context information about the decision
            outcome: Outcome of the decision (success, failure, etc.)
            metrics: Performance metrics related to the decision
            user_id: Optional user identifier
            confidence: Optional confidence score for the decision
            execution_time: Optional execution time in seconds
            
        Returns:
            Feedback ID for the collected feedback
        """
        feedback_data = {
            'id': str(uuid.uuid4()),
            'timestamp': datetime.utcnow().isoformat(),
            'decision': decision,
            'context': context,
            'outcome': outcome,
            'metrics': metrics,
            'user_id': user_id,
            'confidence': confidence,
            'execution_time': execution_time
        }
        
        # Store the feedback
        feedback_id = self.store.store_feedback(feedback_data)
        
        return feedback_id
    
    def collect_batch(self, feedback_list: list) -> list:
        """Collect multiple feedback entries at once
        
        Args:
            feedback_list: List of feedback dictionaries
            
        Returns:
            List of feedback IDs
        """
        feedback_ids = []
        
        for feedback in feedback_list:
            feedback_id = self.collect(**feedback)
            feedback_ids.append(feedback_id)
        
        return feedback_ids
    
    def get_feedback(self, feedback_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve feedback by ID
        
        Args:
            feedback_id: The feedback ID to retrieve
            
        Returns:
            Feedback data or None if not found
        """
        return self.store.get_feedback(feedback_id)
    
    def list_feedback(self, limit: int = 100, offset: int = 0) -> list:
        """List recent feedback entries
        
        Args:
            limit: Maximum number of entries to return
            offset: Number of entries to skip
            
        Returns:
            List of feedback entries
        """
        return self.store.list_feedback(limit=limit, offset=offset) 