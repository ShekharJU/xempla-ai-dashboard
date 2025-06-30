"""
Main AI Agent for Closed-Loop AI Systems

This module implements the core AI agent that makes decisions and learns
from feedback in energy efficiency, predictive maintenance, and fault diagnostics.
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from dataclasses import dataclass

from ..llm.llm_client import LLMClient, LLMResponse
from ..feedback.feedback_loop import FeedbackLoop, Decision, Feedback

logger = logging.getLogger(__name__)

@dataclass
class AgentState:
    """Represents the current state of the AI agent"""
    total_decisions: int = 0
    successful_decisions: int = 0
    learning_rate: float = 0.1
    confidence_threshold: float = 0.7
    last_decision_time: Optional[datetime] = None

class AIAgent:
    """
    Main AI agent for closed-loop decision making and learning
    """
    
    def __init__(self, agent_type: str = "general", learning_rate: float = 0.1):
        self.agent_type = agent_type
        self.llm_client = LLMClient()
        self.feedback_loop = FeedbackLoop(learning_rate=learning_rate)
        self.state = AgentState(learning_rate=learning_rate)
        self.decision_history: List[Dict[str, Any]] = []
        
        logger.info(f"Initialized AI Agent: {agent_type}")
    
    def make_decision(self, operational_data: Dict[str, Any], 
                     decision_type: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Make a decision based on operational data
        
        Args:
            operational_data: Current operational parameters
            decision_type: Type of decision to make
            context: Additional context information
            
        Returns:
            Dictionary containing the decision and metadata
        """
        try:
            # Generate decision using LLM
            llm_response = self.llm_client.generate_decision(operational_data, decision_type)
            
            # Create decision object
            decision = Decision(
                timestamp=datetime.now(),
                decision_type=decision_type,
                input_data=operational_data,
                decision=llm_response.content,
                reasoning=self._extract_reasoning(llm_response.content),
                confidence=llm_response.confidence or 0.8
            )
            
            # Record decision in feedback loop
            decision_id = self.feedback_loop.record_decision(decision)
            
            # Update agent state
            self.state.total_decisions += 1
            self.state.last_decision_time = datetime.now()
            
            # Store decision in history
            decision_record = {
                'decision_id': decision_id,
                'timestamp': decision.timestamp,
                'decision_type': decision_type,
                'operational_data': operational_data,
                'decision': decision.decision,
                'reasoning': decision.reasoning,
                'confidence': decision.confidence,
                'llm_model': llm_response.model,
                'tokens_used': llm_response.tokens_used
            }
            self.decision_history.append(decision_record)
            
            logger.info(f"Made decision {decision_id}: {decision_type}")
            
            return {
                'decision_id': decision_id,
                'decision': decision.decision,
                'reasoning': decision.reasoning,
                'confidence': decision.confidence,
                'recommendations': self._extract_recommendations(decision.decision),
                'next_actions': self._generate_next_actions(decision_type, operational_data)
            }
            
        except Exception as e:
            logger.error(f"Error making decision: {e}")
            return {
                'error': str(e),
                'decision': 'Unable to make decision due to system error',
                'recommendations': ['Check system connectivity', 'Verify data quality']
            }
    
    def receive_feedback(self, decision_id: str, outcome: str, 
                        metrics: Dict[str, float], actual_result: Dict[str, Any]) -> None:
        """
        Receive feedback on a previous decision
        
        Args:
            decision_id: ID of the decision being evaluated
            outcome: Outcome of the decision (success, failure, partial)
            metrics: Performance metrics
            actual_result: Actual results observed
        """
        try:
            feedback = Feedback(
                decision_id=decision_id,
                timestamp=datetime.now(),
                outcome=outcome,
                metrics=metrics,
                actual_result=actual_result,
                feedback_score=self._calculate_feedback_score(outcome, metrics)
            )
            
            self.feedback_loop.record_feedback(decision_id, feedback)
            
            # Update agent state
            if outcome == 'success':
                self.state.successful_decisions += 1
            
            # Adjust learning parameters based on feedback
            self._update_learning_parameters(feedback)
            
            logger.info(f"Received feedback for {decision_id}: {outcome}")
            
        except Exception as e:
            logger.error(f"Error processing feedback: {e}")
    
    def get_performance_insights(self) -> Dict[str, Any]:
        """
        Get insights about agent performance and learning progress
        
        Returns:
            Dictionary with performance insights and recommendations
        """
        insights = self.feedback_loop.get_learning_insights()
        
        # Add agent-specific insights
        insights.update({
            'agent_type': self.agent_type,
            'success_rate': (self.state.successful_decisions / max(1, self.state.total_decisions)) * 100,
            'learning_rate': self.state.learning_rate,
            'confidence_threshold': self.state.confidence_threshold,
            'recent_decisions': len(self.decision_history[-10:]) if self.decision_history else 0
        })
        
        return insights
    
    def _extract_reasoning(self, decision_content: str) -> str:
        """Extract reasoning from LLM decision content"""
        # Simple heuristic to extract reasoning
        if 'reasoning:' in decision_content.lower():
            parts = decision_content.lower().split('reasoning:')
            if len(parts) > 1:
                return parts[1].strip()
        
        # If no explicit reasoning section, use the first few sentences
        sentences = decision_content.split('.')
        return '. '.join(sentences[:3]) + '.'
    
    def _extract_recommendations(self, decision_content: str) -> List[str]:
        """Extract actionable recommendations from decision content"""
        recommendations = []
        
        # Look for recommendation patterns
        lines = decision_content.split('\n')
        for line in lines:
            line = line.strip()
            if any(keyword in line.lower() for keyword in ['recommend', 'suggest', 'should', 'action']):
                if line and not line.startswith('#'):
                    recommendations.append(line)
        
        # If no explicit recommendations found, generate generic ones
        if not recommendations:
            recommendations = [
                'Monitor system parameters closely',
                'Review operational procedures',
                'Schedule follow-up assessment'
            ]
        
        return recommendations[:5]  # Limit to top 5 recommendations
    
    def _generate_next_actions(self, decision_type: str, operational_data: Dict[str, Any]) -> List[str]:
        """Generate next actions based on decision type and data"""
        actions = []
        
        if decision_type == 'maintenance':
            actions = [
                'Schedule maintenance activities',
                'Prepare replacement parts',
                'Notify maintenance team',
                'Update maintenance schedule'
            ]
        elif decision_type == 'energy_optimization':
            actions = [
                'Implement energy-saving measures',
                'Adjust operational parameters',
                'Monitor energy consumption',
                'Track cost savings'
            ]
        elif decision_type == 'fault_diagnosis':
            actions = [
                'Investigate identified issues',
                'Implement corrective measures',
                'Monitor system recovery',
                'Document incident details'
            ]
        else:
            actions = [
                'Review decision outcomes',
                'Monitor system performance',
                'Update operational procedures'
            ]
        
        return actions
    
    def _calculate_feedback_score(self, outcome: str, metrics: Dict[str, float]) -> float:
        """Calculate a numerical feedback score"""
        base_score = {'success': 1.0, 'partial': 0.5, 'failure': 0.0}.get(outcome, 0.5)
        
        # Adjust score based on metrics
        if 'accuracy' in metrics:
            base_score *= metrics['accuracy']
        if 'efficiency' in metrics:
            base_score *= metrics['efficiency']
        if 'cost_savings' in metrics:
            base_score *= min(1.0, metrics['cost_savings'] / 1000)  # Normalize cost savings
        
        return min(1.0, max(0.0, base_score))
    
    def _update_learning_parameters(self, feedback: Feedback) -> None:
        """Update learning parameters based on feedback"""
        # Adjust learning rate based on performance
        if feedback.feedback_score > 0.8:
            # Good performance, reduce learning rate slightly
            self.state.learning_rate *= 0.95
        elif feedback.feedback_score < 0.3:
            # Poor performance, increase learning rate
            self.state.learning_rate *= 1.1
        
        # Adjust confidence threshold
        if feedback.outcome == 'success':
            self.state.confidence_threshold = min(0.9, self.state.confidence_threshold * 1.02)
        else:
            self.state.confidence_threshold = max(0.5, self.state.confidence_threshold * 0.98)
        
        # Ensure learning rate stays within reasonable bounds
        self.state.learning_rate = max(0.01, min(0.5, self.state.learning_rate))
    
    def export_agent_data(self, filename: str) -> None:
        """Export agent data and performance history"""
        data = {
            'agent_info': {
                'agent_type': self.agent_type,
                'state': {
                    'total_decisions': self.state.total_decisions,
                    'successful_decisions': self.state.successful_decisions,
                    'learning_rate': self.state.learning_rate,
                    'confidence_threshold': self.state.confidence_threshold
                }
            },
            'decision_history': self.decision_history,
            'feedback_loop_data': self.feedback_loop.export_data(filename + '_feedback.json')
        }
        
        import json
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        logger.info(f"Exported agent data to {filename}") 