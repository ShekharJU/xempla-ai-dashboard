"""
Feedback Store for Xempla AI Systems Intern Prototype

Stores and retrieves feedback data in JSONL format.
"""
import json
import os
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
import uuid


class FeedbackStore:
    """Stores feedback data in JSONL format"""
    
    def __init__(self, file_path: str = "feedback.jsonl"):
        """Initialize feedback store
        
        Args:
            file_path: Path to the JSONL file for storing feedback
        """
        self.file_path = file_path
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """Ensure the feedback file exists"""
        # Create directory if it doesn't exist and path has directory component
        dir_path = os.path.dirname(self.file_path)
        if dir_path:  # Only create directory if there is a directory component
            os.makedirs(dir_path, exist_ok=True)
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w", encoding="utf-8") as f:
                pass  # Create empty file
    
    def store_feedback(self, feedback: Dict[str, Any]) -> str:
        """Store feedback data
        
        Args:
            feedback: Feedback data dictionary
            
        Returns:
            Feedback ID
        """
        # Generate feedback ID if not present
        if "id" not in feedback:
            feedback["id"] = str(uuid.uuid4())
        
        # Add timestamp if not present
        if "timestamp" not in feedback:
            feedback["timestamp"] = datetime.now(timezone.utc).isoformat()
        
        # Save feedback to file
        with open(self.file_path, "a", encoding="utf-8") as f:
            json.dump(feedback, f)
            f.write("\n")
        return feedback["id"]

    def load_feedback(self):
        if not os.path.exists(self.file_path):
            return []
        with open(self.file_path, "r", encoding="utf-8") as f:
            return [json.loads(line) for line in f] 