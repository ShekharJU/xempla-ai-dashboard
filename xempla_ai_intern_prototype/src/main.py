"""
Main Demonstration Script for Xempla AI Systems Intern Prototype

This script demonstrates a closed-loop AI system that integrates LLMs with feedback
mechanisms for energy efficiency, fault diagnostics, and predictive maintenance.
"""

import os
import sys
import logging
import time
from datetime import datetime
from typing import Dict, List, Any

# Add src to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agents.ai_agent import AIAgent
from src.simulation.data_simulator import DataSimulator
from src.feedback.feedback_loop import FeedbackLoop

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('results/ai_system.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class ClosedLoopAIDemo:
    """
    Demonstration of closed-loop AI system for Xempla AI Systems Intern role
    """
    
    def __init__(self):
        self.data_simulator = DataSimulator()
        self.agents = {
            'maintenance': AIAgent('maintenance', learning_rate=0.15),
            'energy': AIAgent('energy', learning_rate=0.12),
            'fault': AIAgent('fault', learning_rate=0.18)
        }
        self.simulation_results = []
        
        logger.info("Initialized Closed-Loop AI Demo System")
    
    def run_predictive_maintenance_demo(self, iterations: int = 10) -> None:
        """
        Demonstrate predictive maintenance with LLM decision-making and feedback
        """
        logger.info("Starting Predictive Maintenance Demo")
        print("\n" + "="*60)
        print("PREDICTIVE MAINTENANCE DEMONSTRATION")
        print("="*60)
        
        # Generate manufacturing equipment data
        equipment_data = self.data_simulator.generate_manufacturing_data(hours=24)
        agent = self.agents['maintenance']
        
        for i in range(iterations):
            print(f"\n--- Iteration {i+1}/{iterations} ---")
            
            # Get current operational data
            current_data = equipment_data.iloc[i].to_dict()
            operational_context = {
                'motor_vibration': current_data['motor_vibration'],
                'bearing_temperature': current_data['bearing_temperature'],
                'oil_pressure': current_data['oil_pressure'],
                'efficiency': current_data['efficiency'],
                'operating_hours': current_data['operating_hours']
            }
            
            # Make maintenance decision
            decision_result = agent.make_decision(operational_context, 'maintenance')
            
            print(f"Decision ID: {decision_result['decision_id']}")
            print(f"Confidence: {decision_result['confidence']:.2f}")
            print(f"Decision: {decision_result['decision'][:200]}...")
            print(f"Recommendations: {decision_result['recommendations'][:2]}")
            
            # Simulate feedback (in real system, this would come from actual outcomes)
            feedback_outcome = self._simulate_maintenance_outcome(operational_context, decision_result)
            
            # Provide feedback to agent
            agent.receive_feedback(
                decision_id=decision_result['decision_id'],
                outcome=feedback_outcome['outcome'],
                metrics=feedback_outcome['metrics'],
                actual_result=feedback_outcome['actual_result']
            )
            
            print(f"Feedback: {feedback_outcome['outcome']} (Score: {feedback_outcome['metrics'].get('accuracy', 0):.2f})")
            
            time.sleep(1)  # Simulate processing time
        
        # Show learning insights
        insights = agent.get_performance_insights()
        print(f"\n--- Learning Insights ---")
        print(f"Success Rate: {insights['success_rate']:.1f}%")
        print(f"Total Decisions: {insights['total_decisions']}")
        print(f"Performance Trends: {insights['performance_trends']}")
    
    def run_energy_optimization_demo(self, iterations: int = 8) -> None:
        """
        Demonstrate energy optimization with LLM decision-making and feedback
        """
        logger.info("Starting Energy Optimization Demo")
        print("\n" + "="*60)
        print("ENERGY OPTIMIZATION DEMONSTRATION")
        print("="*60)
        
        # Generate HVAC system data
        hvac_data = self.data_simulator.generate_hvac_data(days=7)
        agent = self.agents['energy']
        
        for i in range(iterations):
            print(f"\n--- Iteration {i+1}/{iterations} ---")
            
            # Get current operational data
            current_data = hvac_data.iloc[i*4].to_dict()  # Sample every 4th data point
            operational_context = {
                'temperature_setpoint': current_data['temperature_setpoint'],
                'actual_temperature': current_data['actual_temperature'],
                'humidity': current_data['humidity'],
                'energy_consumption': current_data['energy_consumption'],
                'efficiency': current_data['efficiency'],
                'compressor_runtime': current_data['compressor_runtime']
            }
            
            # Make energy optimization decision
            decision_result = agent.make_decision(operational_context, 'energy_optimization')
            
            print(f"Decision ID: {decision_result['decision_id']}")
            print(f"Current Energy Consumption: {operational_context['energy_consumption']:.1f} kWh")
            print(f"System Efficiency: {operational_context['efficiency']:.1f}%")
            print(f"Decision: {decision_result['decision'][:200]}...")
            
            # Simulate feedback
            feedback_outcome = self._simulate_energy_outcome(operational_context, decision_result)
            
            # Provide feedback to agent
            agent.receive_feedback(
                decision_id=decision_result['decision_id'],
                outcome=feedback_outcome['outcome'],
                metrics=feedback_outcome['metrics'],
                actual_result=feedback_outcome['actual_result']
            )
            
            print(f"Energy Savings: {feedback_outcome['metrics'].get('cost_savings', 0):.1f}%")
            print(f"Feedback: {feedback_outcome['outcome']}")
            
            time.sleep(1)
        
        # Show learning insights
        insights = agent.get_performance_insights()
        print(f"\n--- Learning Insights ---")
        print(f"Success Rate: {insights['success_rate']:.1f}%")
        print(f"Efficiency Improvement: {insights['performance_trends'].get('efficiency', 0):.1f}%")
    
    def run_fault_diagnosis_demo(self, iterations: int = 6) -> None:
        """
        Demonstrate fault diagnosis with LLM decision-making and feedback
        """
        logger.info("Starting Fault Diagnosis Demo")
        print("\n" + "="*60)
        print("FAULT DIAGNOSIS DEMONSTRATION")
        print("="*60)
        
        # Generate fault scenarios
        fault_scenarios = self.data_simulator.generate_fault_scenarios(n_scenarios=iterations)
        agent = self.agents['fault']
        
        for i, scenario in enumerate(fault_scenarios):
            print(f"\n--- Fault Scenario {i+1}/{iterations} ---")
            
            # Create operational context from fault scenario
            operational_context = {
                'fault_type': scenario['fault_type'],
                'severity': scenario['severity'],
                'detection_delay_hours': scenario['detection_delay_hours'],
                'cost_impact': scenario['cost_impact'],
                'safety_risk': scenario['safety_risk'],
                'operational_impact': scenario['operational_impact']
            }
            
            # Make fault diagnosis decision
            decision_result = agent.make_decision(operational_context, 'fault_diagnosis')
            
            print(f"Fault Type: {scenario['fault_type']}")
            print(f"Severity: {scenario['severity']}")
            print(f"Safety Risk: {scenario['safety_risk']}")
            print(f"Decision: {decision_result['decision'][:200]}...")
            print(f"Next Actions: {decision_result['next_actions'][:2]}")
            
            # Simulate feedback
            feedback_outcome = self._simulate_fault_outcome(scenario, decision_result)
            
            # Provide feedback to agent
            agent.receive_feedback(
                decision_id=decision_result['decision_id'],
                outcome=feedback_outcome['outcome'],
                metrics=feedback_outcome['metrics'],
                actual_result=feedback_outcome['actual_result']
            )
            
            print(f"Diagnosis Accuracy: {feedback_outcome['metrics'].get('accuracy', 0):.1f}%")
            print(f"Response Time: {feedback_outcome['metrics'].get('response_time', 0):.1f} hours")
            
            time.sleep(1)
        
        # Show learning insights
        insights = agent.get_performance_insights()
        print(f"\n--- Learning Insights ---")
        print(f"Success Rate: {insights['success_rate']:.1f}%")
        print(f"Accuracy Improvement: {insights['performance_trends'].get('accuracy', 0):.1f}%")
    
    def _simulate_maintenance_outcome(self, operational_data: Dict, decision_result: Dict) -> Dict:
        """Simulate maintenance decision outcome"""
        # Simple simulation based on operational parameters
        vibration = operational_data['motor_vibration']
        temperature = operational_data['bearing_temperature']
        efficiency = operational_data['efficiency']
        
        # Determine outcome based on decision quality and operational conditions
        if vibration > 4.0 or temperature > 80:
            outcome = 'success' if 'maintenance' in decision_result['decision'].lower() else 'failure'
        elif efficiency < 85:
            outcome = 'success' if 'inspection' in decision_result['decision'].lower() else 'partial'
        else:
            outcome = 'success' if 'monitor' in decision_result['decision'].lower() else 'partial'
        
        return {
            'outcome': outcome,
            'metrics': {
                'accuracy': 0.85 if outcome == 'success' else 0.45,
                'efficiency': efficiency + (5 if outcome == 'success' else -2),
                'cost_savings': 15.0 if outcome == 'success' else 2.0
            },
            'actual_result': {
                'maintenance_performed': outcome == 'success',
                'downtime_hours': 0 if outcome == 'success' else 4,
                'cost_impact': -500 if outcome == 'success' else 2000
            }
        }
    
    def _simulate_energy_outcome(self, operational_data: Dict, decision_result: Dict) -> Dict:
        """Simulate energy optimization outcome"""
        current_consumption = operational_data['energy_consumption']
        current_efficiency = operational_data['efficiency']
        
        # Determine outcome based on decision quality
        if 'optimize' in decision_result['decision'].lower() or 'adjust' in decision_result['decision'].lower():
            outcome = 'success'
            savings = 12.0
            efficiency_gain = 8.0
        elif 'monitor' in decision_result['decision'].lower():
            outcome = 'partial'
            savings = 5.0
            efficiency_gain = 3.0
        else:
            outcome = 'failure'
            savings = 0.0
            efficiency_gain = 0.0
        
        return {
            'outcome': outcome,
            'metrics': {
                'accuracy': 0.90 if outcome == 'success' else 0.60,
                'efficiency': current_efficiency + efficiency_gain,
                'cost_savings': savings
            },
            'actual_result': {
                'energy_saved_kwh': current_consumption * savings / 100,
                'efficiency_improvement': efficiency_gain,
                'cost_savings_usd': current_consumption * savings / 100 * 0.12  # $0.12/kWh
            }
        }
    
    def _simulate_fault_outcome(self, scenario: Dict, decision_result: Dict) -> Dict:
        """Simulate fault diagnosis outcome"""
        fault_type = scenario['fault_type']
        severity = scenario['severity']
        
        # Determine outcome based on diagnosis accuracy
        if fault_type in decision_result['decision'].lower():
            outcome = 'success'
            accuracy = 95.0
            response_time = scenario['detection_delay_hours'] * 0.5
        elif any(word in decision_result['decision'].lower() for word in ['fault', 'issue', 'problem']):
            outcome = 'partial'
            accuracy = 70.0
            response_time = scenario['detection_delay_hours'] * 0.8
        else:
            outcome = 'failure'
            accuracy = 30.0
            response_time = scenario['detection_delay_hours'] * 1.5
        
        return {
            'outcome': outcome,
            'metrics': {
                'accuracy': accuracy,
                'response_time': response_time,
                'cost_savings': scenario['cost_impact'] * (0.8 if outcome == 'success' else 0.3)
            },
            'actual_result': {
                'fault_correctly_identified': outcome == 'success',
                'repair_time_hours': scenario['repair_time_hours'] * (0.7 if outcome == 'success' else 1.2),
                'total_cost': scenario['cost_impact'] * (0.6 if outcome == 'success' else 1.1)
            }
        }
    
    def generate_final_report(self) -> None:
        """Generate comprehensive final report"""
        print("\n" + "="*60)
        print("FINAL SYSTEM PERFORMANCE REPORT")
        print("="*60)
        
        for agent_type, agent in self.agents.items():
            insights = agent.get_performance_insights()
            print(f"\n{agent_type.upper()} AGENT:")
            print(f"  Success Rate: {insights['success_rate']:.1f}%")
            print(f"  Total Decisions: {insights['total_decisions']}")
            print(f"  Learning Rate: {insights['learning_rate']:.3f}")
            print(f"  Performance Trends:")
            for metric, trend in insights['performance_trends'].items():
                print(f"    {metric}: {trend:+.1f}%")
            
            # Export agent data
            agent.export_agent_data(f'results/{agent_type}_agent_data.json')
        
        print(f"\nAll data exported to 'results/' directory")
        print("Check 'ai_system.log' for detailed system logs")

def main():
    """Main demonstration function"""
    print("Xempla AI Systems Intern - Closed-Loop AI Prototype")
    print("Demonstrating LLM Integration with Feedback Mechanisms")
    print("="*60)
    
    # Create results directory if it doesn't exist
    os.makedirs('results', exist_ok=True)
    
    # Initialize demo system
    demo = ClosedLoopAIDemo()
    
    try:
        # Run demonstrations
        demo.run_predictive_maintenance_demo(iterations=8)
        demo.run_energy_optimization_demo(iterations=6)
        demo.run_fault_diagnosis_demo(iterations=5)
        
        # Generate final report
        demo.generate_final_report()
        
        print("\n" + "="*60)
        print("DEMONSTRATION COMPLETED SUCCESSFULLY")
        print("="*60)
        print("\nKey Features Demonstrated:")
        print("✓ LLM Integration for Decision Making")
        print("✓ Feedback Loop Mechanisms")
        print("✓ Continuous Learning and Improvement")
        print("✓ Multi-Domain Applications (Maintenance, Energy, Fault Diagnosis)")
        print("✓ Performance Tracking and Analytics")
        print("✓ Realistic Operational Data Simulation")
        
    except Exception as e:
        logger.error(f"Demo failed: {e}")
        print(f"Demo failed: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 