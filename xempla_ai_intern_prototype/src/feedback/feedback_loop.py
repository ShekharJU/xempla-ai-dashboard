"""
Feedback Loop Implementation for Closed-Loop AI Systems

This module implements the core feedback mechanism that enables AI systems
to learn from their decisions and improve over time.
"""

import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import json
from .feedback_store import FeedbackStore

logger = logging.getLogger(__name__)

@dataclass
class Decision:
    """Represents a decision made by the AI system"""
    timestamp: datetime
    decision_type: str
    input_data: Dict[str, Any]
    decision: str
    reasoning: str
    confidence: float

@dataclass
class Feedback:
    """Represents feedback on a decision"""
    decision_id: str
    timestamp: datetime
    outcome: str  # success, failure, partial
    metrics: Dict[str, float]
    actual_result: Dict[str, Any]
    feedback_score: float

class FeedbackLoop:
    """
    Implements the feedback loop mechanism for closed-loop AI systems
    """
    
    def __init__(self, learning_rate: float = 0.1):
        self.learning_rate = learning_rate
        self.decisions: List[Decision] = []
        self.feedback_history: List[Feedback] = []
        self.performance_metrics: Dict[str, List[float]] = {
            'accuracy': [],
            'efficiency': [],
            'cost_savings': []
        }
    
    def record_decision(self, decision: Decision) -> str:
        """
        Record a decision made by the AI system
        
        Args:
            decision: The decision object to record
            
        Returns:
            Decision ID for future reference
        """
        decision_id = f"decision_{len(self.decisions)}_{decision.timestamp.strftime('%Y%m%d_%H%M%S')}"
        self.decisions.append(decision)
        logger.info(f"Recorded decision {decision_id}: {decision.decision_type}")
        return decision_id
    
    def record_feedback(self, decision_id: str, feedback: Feedback) -> None:
        """
        Record feedback on a previous decision
        
        Args:
            decision_id: ID of the decision being evaluated
            feedback: Feedback object with outcome and metrics
        """
        feedback.decision_id = decision_id
        self.feedback_history.append(feedback)
        
        # Update performance metrics
        self._update_performance_metrics(feedback)
        
        logger.info(f"Recorded feedback for {decision_id}: {feedback.outcome}")
    
    def _update_performance_metrics(self, feedback: Feedback) -> None:
        """Update performance metrics based on feedback"""
        if 'accuracy' in feedback.metrics:
            self.performance_metrics['accuracy'].append(feedback.metrics['accuracy'])
        
        if 'efficiency' in feedback.metrics:
            self.performance_metrics['efficiency'].append(feedback.metrics['efficiency'])
        
        if 'cost_savings' in feedback.metrics:
            self.performance_metrics['cost_savings'].append(feedback.metrics['cost_savings'])
    
    def calculate_improvement(self, metric: str, window: int = 10) -> float:
        """
        Calculate improvement in a specific metric over time
        
        Args:
            metric: Metric to analyze (accuracy, efficiency, cost_savings)
            window: Number of recent data points to consider
            
        Returns:
            Improvement percentage
        """
        if metric not in self.performance_metrics:
            return 0.0
        
        values = self.performance_metrics[metric]
        if len(values) < window:
            return 0.0
        
        recent_values = values[-window:]
        if len(recent_values) < 2:
            return 0.0
        
        # Calculate improvement from first to last value in window
        improvement = (recent_values[-1] - recent_values[0]) / recent_values[0] * 100
        return improvement
    
    def get_learning_insights(self) -> Dict[str, Any]:
        """
        Generate insights for improving the AI system
        
        Returns:
            Dictionary with learning insights and recommendations
        """
        insights = {
            'total_decisions': len(self.decisions),
            'total_feedback': len(self.feedback_history),
            'success_rate': self._calculate_success_rate(),
            'performance_trends': self._calculate_performance_trends(),
            'recommendations': self._generate_recommendations()
        }
        
        return insights
    
    def _calculate_success_rate(self) -> float:
        """Calculate overall success rate of decisions"""
        if not self.feedback_history:
            return 0.0
        
        successful = sum(1 for f in self.feedback_history if f.outcome == 'success')
        return successful / len(self.feedback_history) * 100
    
    def _calculate_performance_trends(self) -> Dict[str, float]:
        """Calculate trends for different performance metrics"""
        trends = {}
        for metric in self.performance_metrics:
            trends[metric] = self.calculate_improvement(metric)
        return trends
    
    def _generate_recommendations(self) -> List[str]:
        """Generate recommendations for system improvement"""
        recommendations = []
        
        success_rate = self._calculate_success_rate()
        if success_rate < 70:
            recommendations.append("Consider improving decision criteria and input data quality")
        
        accuracy_improvement = self.calculate_improvement('accuracy')
        if accuracy_improvement < 5:
            recommendations.append("Review and refine the decision-making algorithms")
        
        efficiency_improvement = self.calculate_improvement('efficiency')
        if efficiency_improvement < 10:
            recommendations.append("Optimize operational parameters and response times")
        
        return recommendations
    
    def export_data(self, filename: str) -> None:
        """Export feedback loop data to JSON file"""
        data = {
            'decisions': [
                {
                    'timestamp': d.timestamp.isoformat(),
                    'decision_type': d.decision_type,
                    'input_data': d.input_data,
                    'decision': d.decision,
                    'reasoning': d.reasoning,
                    'confidence': d.confidence
                }
                for d in self.decisions
            ],
            'feedback': [
                {
                    'decision_id': f.decision_id,
                    'timestamp': f.timestamp.isoformat(),
                    'outcome': f.outcome,
                    'metrics': f.metrics,
                    'actual_result': f.actual_result,
                    'feedback_score': f.feedback_score
                }
                for f in self.feedback_history
            ],
            'performance_metrics': self.performance_metrics
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        logger.info(f"Exported feedback loop data to {filename}")

class FeedbackCollector:
    def __init__(self, store=None):
        self.store = store or FeedbackStore()

    def collect(self, decision, context, outcome, metrics):
        feedback = {
            "decision": decision,
            "context": context,
            "outcome": outcome,
            "metrics": metrics
        }
        self.store.store_feedback(feedback)
        return feedback 