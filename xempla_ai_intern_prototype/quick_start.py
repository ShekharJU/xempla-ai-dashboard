"""
Quick Start Demo for Xempla AI Systems Intern Prototype

This script provides a quick demonstration of the closed-loop AI system
without requiring API keys, using mocked LLM responses.
"""

import sys
import os
import time
from datetime import datetime

# Add src to path
sys.path.append('src')

from src.simulation.data_simulator import DataSimulator
from src.feedback.feedback_loop import FeedbackLoop, Decision, Feedback

def mock_llm_response(operational_data, decision_type):
    """Mock LLM response for demonstration purposes"""
    responses = {
        'maintenance': {
            'content': 'Based on the operational data, I recommend scheduling preventive maintenance within 48 hours. The motor vibration levels are approaching critical thresholds.',
            'confidence': 0.85
        },
        'energy_optimization': {
            'content': 'Energy consumption can be optimized by adjusting temperature setpoints and implementing demand-based control strategies.',
            'confidence': 0.78
        },
        'fault_diagnosis': {
            'content': 'Analysis indicates potential bearing wear. Recommend immediate inspection and vibration analysis.',
            'confidence': 0.92
        }
    }
    
    return responses.get(decision_type, {
        'content': 'Standard operational recommendation based on current parameters.',
        'confidence': 0.7
    })

def quick_demo():
    """Run quick demonstration"""
    print("🚀 Xempla AI Systems Intern - Quick Start Demo")
    print("=" * 50)
    print("Demonstrating Closed-Loop AI System with Mock LLM")
    print()
    
    # 1. Initialize components
    print("📊 Initializing system components...")
    simulator = DataSimulator(seed=42)
    feedback_loop = FeedbackLoop(learning_rate=0.1)
    
    # 2. Generate sample data
    print("📈 Generating operational data...")
    hvac_data = simulator.generate_hvac_data(days=1, frequency_minutes=60)
    manufacturing_data = simulator.generate_manufacturing_data(hours=24)
    
    print(f"   ✅ Generated {len(hvac_data)} HVAC records")
    print(f"   ✅ Generated {len(manufacturing_data)} manufacturing records")
    
    # 3. Simulate decision-making process
    print("\n🤖 Simulating AI decision-making process...")
    
    decision_types = ['maintenance', 'energy_optimization', 'fault_diagnosis']
    total_decisions = 0
    successful_decisions = 0
    
    for i, decision_type in enumerate(decision_types):
        print(f"\n--- Decision {i+1}: {decision_type.replace('_', ' ').title()} ---")
        
        # Get sample data
        if decision_type == 'energy_optimization':
            sample_data = hvac_data.iloc[i % len(hvac_data)].to_dict()
        else:
            sample_data = manufacturing_data.iloc[i % len(manufacturing_data)].to_dict()
        
        # Mock LLM decision
        llm_response = mock_llm_response(sample_data, decision_type)
        
        # Create decision object
        decision = Decision(
            timestamp=datetime.now(),
            decision_type=decision_type,
            input_data=sample_data,
            decision=llm_response['content'],
            reasoning=f"Analysis based on {decision_type} parameters",
            confidence=llm_response['confidence']
        )
        
        # Record decision
        decision_id = feedback_loop.record_decision(decision)
        total_decisions += 1
        
        print(f"   Decision ID: {decision_id}")
        print(f"   Confidence: {decision.confidence:.2f}")
        print(f"   Decision: {decision.decision[:100]}...")
        
        # Simulate feedback
        feedback_quality = 0.8 if decision.confidence > 0.8 else 0.6
        outcome = 'success' if feedback_quality > 0.7 else 'partial'
        
        if outcome == 'success':
            successful_decisions += 1
        
        feedback = Feedback(
            decision_id=decision_id,
            timestamp=datetime.now(),
            outcome=outcome,
            metrics={
                'accuracy': feedback_quality,
                'efficiency': feedback_quality * 0.9,
                'cost_savings': 15.0 if outcome == 'success' else 5.0
            },
            actual_result={'result': outcome, 'impact': 'positive'},
            feedback_score=feedback_quality
        )
        
        feedback_loop.record_feedback(decision_id, feedback)
        
        print(f"   Feedback: {outcome} (Quality: {feedback_quality:.2f})")
        
        time.sleep(1)  # Simulate processing time
    
    # 4. Generate insights
    print("\n📊 Generating system insights...")
    insights = feedback_loop.get_learning_insights()
    
    print(f"\n🎯 SYSTEM PERFORMANCE SUMMARY:")
    print(f"   Total Decisions: {insights['total_decisions']}")
    print(f"   Success Rate: {insights['success_rate']:.1f}%")
    print(f"   Performance Trends:")
    for metric, trend in insights['performance_trends'].items():
        print(f"     • {metric}: {trend:+.1f}%")
    
    if insights['recommendations']:
        print(f"   Recommendations:")
        for rec in insights['recommendations'][:3]:
            print(f"     • {rec}")
    
    # 5. Export results
    print("\n📁 Exporting results...")
    os.makedirs('results', exist_ok=True)
    
    feedback_loop.export_data('results/quick_demo_results.json')
    
    print("✅ Results exported to 'results/quick_demo_results.json'")
    
    # 6. Summary
    print("\n" + "=" * 50)
    print("🎉 QUICK DEMO COMPLETED SUCCESSFULLY!")
    print("=" * 50)
    print("\nKey Features Demonstrated:")
    print("✓ Operational Data Generation")
    print("✓ AI Decision Making (Mocked)")
    print("✓ Feedback Loop Mechanisms")
    print("✓ Performance Tracking")
    print("✓ Learning Insights")
    print("✓ Data Export")
    
    print(f"\n📈 Demo Statistics:")
    print(f"   Decisions Made: {total_decisions}")
    print(f"   Success Rate: {(successful_decisions/total_decisions)*100:.1f}%")
    print(f"   System Status: {'🟢 Excellent' if insights['success_rate'] > 80 else '🟡 Good' if insights['success_rate'] > 60 else '🔴 Needs Improvement'}")
    
    print("\n💡 Next Steps:")
    print("   1. Add your API keys to config.env.example")
    print("   2. Run 'python src/main.py' for full demonstration")
    print("   3. Explore 'notebooks/analysis_demo.py' for detailed analysis")
    print("   4. Run 'python tests/test_basic_functionality.py' for testing")

if __name__ == "__main__":
    try:
        quick_demo()
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        sys.exit(1) 