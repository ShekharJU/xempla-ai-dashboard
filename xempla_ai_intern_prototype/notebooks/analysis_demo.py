"""
Analysis Demo Script for Xempla AI Systems Intern Prototype

This script provides comprehensive analysis of the closed-loop AI system
performance and learning patterns.
"""

import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Add src to path
sys.path.append('../src')

# Import our modules
from simulation.data_simulator import DataSimulator
from agents.ai_agent import AIAgent
from feedback.feedback_loop import FeedbackLoop

# Set up plotting style
plt.style.use('default')
sns.set_palette("husl")

def main():
    print("🔍 Xempla AI Systems Intern - Analysis Demo")
    print("=" * 50)
    
    # 1. Data Generation
    print("\n📊 Generating operational data...")
    simulator = DataSimulator(seed=42)
    
    hvac_data = simulator.generate_hvac_data(days=30, frequency_minutes=30)
    manufacturing_data = simulator.generate_manufacturing_data(hours=168)
    energy_grid_data = simulator.generate_energy_grid_data(days=7)
    maintenance_data = simulator.generate_predictive_maintenance_data(cycles=500)
    
    print(f"✅ Generated {len(hvac_data)} HVAC records")
    print(f"✅ Generated {len(manufacturing_data)} manufacturing records")
    print(f"✅ Generated {len(energy_grid_data)} energy grid records")
    print(f"✅ Generated {len(maintenance_data)} maintenance cycles")
    
    # 2. Initialize AI Agents
    print("\n🤖 Initializing AI agents...")
    maintenance_agent = AIAgent('maintenance', learning_rate=0.15)
    energy_agent = AIAgent('energy', learning_rate=0.12)
    fault_agent = AIAgent('fault', learning_rate=0.18)
    
    agents = {
        'Maintenance': maintenance_agent,
        'Energy': energy_agent,
        'Fault Diagnosis': fault_agent
    }
    print("✅ AI agents initialized")
    
    # 3. Simulate Learning Process
    print("\n🔄 Simulating learning process...")
    
    def simulate_agent_learning(agent, data_samples, decision_type, iterations=10):
        performance_history = []
        
        for i in range(iterations):
            if isinstance(data_samples, pd.DataFrame):
                sample_data = data_samples.iloc[i % len(data_samples)].to_dict()
            else:
                sample_data = data_samples[i % len(data_samples)]
            
            decision_result = agent.make_decision(sample_data, decision_type)
            
            feedback_quality = np.random.normal(0.7, 0.2)
            outcome = 'success' if feedback_quality > 0.6 else 'partial' if feedback_quality > 0.3 else 'failure'
            
            agent.receive_feedback(
                decision_id=decision_result['decision_id'],
                outcome=outcome,
                metrics={'accuracy': feedback_quality, 'efficiency': feedback_quality * 0.9},
                actual_result={'result': outcome}
            )
            
            insights = agent.get_performance_insights()
            performance_history.append({
                'iteration': i,
                'success_rate': insights['success_rate'],
                'learning_rate': insights['learning_rate'],
                'total_decisions': insights['total_decisions']
            })
        
        return pd.DataFrame(performance_history)
    
    maintenance_performance = simulate_agent_learning(maintenance_agent, manufacturing_data, 'maintenance')
    energy_performance = simulate_agent_learning(energy_agent, hvac_data, 'energy_optimization')
    fault_performance = simulate_agent_learning(fault_agent, simulator.generate_fault_scenarios(10), 'fault_diagnosis')
    
    print("✅ Learning simulations completed")
    
    # 4. Generate Insights
    print("\n📈 Generating performance insights...")
    
    def generate_system_insights():
        insights = {}
        for name, agent in agents.items():
            agent_insights = agent.get_performance_insights()
            insights[name] = {
                'success_rate': agent_insights['success_rate'],
                'total_decisions': agent_insights['total_decisions'],
                'performance_trends': agent_insights['performance_trends'],
                'recommendations': agent_insights.get('recommendations', [])
            }
        return insights
    
    system_insights = generate_system_insights()
    
    # Display results
    print("\n🎯 SYSTEM PERFORMANCE SUMMARY:")
    print("=" * 40)
    
    for agent_name, insights in system_insights.items():
        print(f"\n📊 {agent_name.upper()} AGENT:")
        print(f"   Success Rate: {insights['success_rate']:.1f}%")
        print(f"   Total Decisions: {insights['total_decisions']}")
        print(f"   Performance Trends:")
        for metric, trend in insights['performance_trends'].items():
            print(f"     • {metric}: {trend:+.1f}%")
    
    overall_success_rate = np.mean([insights['success_rate'] for insights in system_insights.values()])
    total_decisions = sum([insights['total_decisions'] for insights in system_insights.values()])
    
    print(f"\n🎯 OVERALL SYSTEM PERFORMANCE:")
    print(f"   Average Success Rate: {overall_success_rate:.1f}%")
    print(f"   Total Decisions Made: {total_decisions}")
    print(f"   System Status: {'🟢 Excellent' if overall_success_rate > 80 else '🟡 Good' if overall_success_rate > 60 else '🔴 Needs Improvement'}")
    
    # 5. Export Results
    print("\n📁 Exporting results...")
    os.makedirs('../results', exist_ok=True)
    
    export_data = {
        'analysis_timestamp': datetime.now().isoformat(),
        'system_performance': {
            'overall_success_rate': overall_success_rate,
            'total_decisions': total_decisions,
            'agent_performance': system_insights
        },
        'learning_analysis': {
            'maintenance_performance': maintenance_performance.to_dict('records'),
            'energy_performance': energy_performance.to_dict('records'),
            'fault_performance': fault_performance.to_dict('records')
        },
        'data_summary': {
            'hvac_records': len(hvac_data),
            'manufacturing_records': len(manufacturing_data),
            'energy_grid_records': len(energy_grid_data),
            'maintenance_cycles': len(maintenance_data)
        }
    }
    
    with open('../results/analysis_results.json', 'w') as f:
        json.dump(export_data, f, indent=2)
    
    maintenance_performance.to_csv('../results/maintenance_performance.csv', index=False)
    energy_performance.to_csv('../results/energy_performance.csv', index=False)
    fault_performance.to_csv('../results/fault_performance.csv', index=False)
    
    print("✅ Results exported to '../results/' directory")
    print("\n🎉 Analysis completed successfully!")
    
    return 0

if __name__ == "__main__":
    exit(main()) 