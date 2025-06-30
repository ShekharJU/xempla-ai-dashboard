#!/usr/bin/env python3
"""
Building Energy Dataset Demo for Xempla AI Systems Intern Prototype

This script demonstrates the integration of real building energy consumption data
with the closed-loop AI system for energy efficiency optimization.
"""

import os
import sys
import json
import logging
from datetime import datetime
import pandas as pd
import numpy as np

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.agents.energy_optimization_agent import EnergyOptimizationAgent
from src.simulation.building_data_loader import BuildingEnergyDataLoader
from src.feedback.feedback_loop import FeedbackLoop

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def make_json_serializable(obj):
    """
    Recursively convert pandas Timestamps, datetimes, and numpy types to strings or native Python types.
    """
    if isinstance(obj, dict):
        return {k: make_json_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [make_json_serializable(v) for v in obj]
    elif isinstance(obj, (pd.Timestamp, datetime)):
        return str(obj)
    elif isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    else:
        return obj

def main():
    """Main demonstration function"""
    print("=" * 80)
    print("XEMPLA AI SYSTEMS INTERN PROTOTYPE")
    print("Building Energy Dataset Integration Demo")
    print("=" * 80)
    
    # Initialize components
    print("\n1. Initializing Building Energy Data Loader...")
    data_loader = BuildingEnergyDataLoader()
    
    # Check dataset availability
    available_buildings = data_loader.list_available_buildings()
    if not available_buildings:
        print("❌ No building data found. Please ensure the dataset is properly loaded.")
        return
    
    print(f"✅ Found {len(available_buildings)} buildings in dataset")
    
    # Get dataset statistics
    stats = data_loader.get_building_statistics()
    print(f"📊 Dataset Statistics:")
    print(f"   - Total buildings: {stats.get('total_buildings', 0)}")
    print(f"   - Building types: {list(stats.get('building_types', {}).keys())}")
    print(f"   - Average square footage: {stats.get('avg_sqft', 0):.0f} sqft")
    print(f"   - Year built range: {stats.get('year_built_range', {}).get('min', 'N/A')} - {stats.get('year_built_range', {}).get('max', 'N/A')}")
    
    # Initialize AI agent
    print("\n2. Initializing Energy Optimization Agent...")
    energy_agent = EnergyOptimizationAgent()
    
    # Initialize feedback loop
    print("\n3. Initializing Feedback Loop...")
    feedback_loop = FeedbackLoop()
    
    # Select sample buildings for analysis
    sample_buildings = available_buildings[:5]  # Analyze first 5 buildings
    print(f"\n4. Analyzing {len(sample_buildings)} sample buildings...")
    
    results = {
        'demo_timestamp': datetime.now().isoformat(),
        'buildings_analyzed': sample_buildings,
        'individual_analyses': [],
        'anomaly_detections': [],
        'optimization_report': None,
        'performance_metrics': {}
    }
    
    # Individual building analysis
    for i, building_id in enumerate(sample_buildings, 1):
        print(f"\n   📍 Analyzing Building {i}/{len(sample_buildings)}: {building_id}")
        
        try:
            # Get building info
            building_info = data_loader.get_building_info(building_id)
            if building_info:
                print(f"      - Type: {building_info.get('primaryspaceusage', 'Unknown')}")
                print(f"      - Size: {building_info.get('sqft', 0):,.0f} sqft")
                print(f"      - Year Built: {building_info.get('yearbuilt', 'Unknown')}")
            
            # Analyze efficiency
            efficiency_analysis = energy_agent.analyze_building_efficiency(building_id)
            if 'error' not in efficiency_analysis:
                results['individual_analyses'].append(efficiency_analysis)
                
                # Extract key metrics
                features = efficiency_analysis.get('efficiency_features', {})
                print(f"      - Total Energy: {features.get('total_energy_consumption', 0):,.0f} kWh")
                print(f"      - Energy Intensity: {features.get('energy_intensity', 0):.2f} kWh/sqft")
                print(f"      - Peak Consumption: {features.get('peak_consumption', 0):.2f} kWh")
                
                # Show optimization scenarios
                scenarios = efficiency_analysis.get('optimization_scenarios', [])
                if scenarios:
                    print(f"      - Optimization Scenarios: {len(scenarios)} identified")
                    for scenario in scenarios[:2]:  # Show top 2
                        savings = scenario.get('potential_savings', 0) * 100
                        print(f"        • {scenario['type']}: {savings:.1f}% potential savings")
            else:
                print(f"      ❌ Error: {efficiency_analysis['error']}")
            
            # Detect anomalies
            anomaly_result = energy_agent.detect_energy_anomalies(building_id)
            if 'error' not in anomaly_result:
                results['anomaly_detections'].append(anomaly_result)
                
                anomaly_stats = anomaly_result.get('anomaly_statistics', {})
                anomaly_count = anomaly_stats.get('anomaly_count', 0)
                anomaly_percent = anomaly_stats.get('anomaly_percentage', 0)
                
                if anomaly_count > 0:
                    print(f"      ⚠️  Anomalies: {anomaly_count} detected ({anomaly_percent:.1f}%)")
                else:
                    print(f"      ✅ No anomalies detected")
            
        except Exception as e:
            logger.error(f"Error analyzing building {building_id}: {e}")
            print(f"      ❌ Analysis failed: {str(e)}")
    
    # Generate comprehensive optimization report
    print(f"\n5. Generating Comprehensive Optimization Report...")
    optimization_report = energy_agent.generate_optimization_report(sample_buildings)
    results['optimization_report'] = optimization_report
    
    if optimization_report:
        overall_stats = optimization_report.get('overall_statistics', {})
        print(f"   📈 Overall Statistics:")
        print(f"      - Successful analyses: {overall_stats.get('successful_analyses', 0)}")
        print(f"      - Average energy intensity: {overall_stats.get('avg_energy_intensity', 0):.2f} kWh/sqft")
        print(f"      - Total potential savings: {overall_stats.get('total_potential_savings_percent', 0):.1f}%")
        print(f"      - Total implementation cost: ${overall_stats.get('total_implementation_cost', 0):,.0f}")
        print(f"      - Average payback period: {overall_stats.get('avg_payback_period', 0):.1f} months")
        
        # Show cross-building recommendations
        recommendations = optimization_report.get('cross_building_recommendations', [])
        if recommendations:
            print(f"   🎯 Cross-Building Recommendations:")
            for i, rec in enumerate(recommendations[:3], 1):
                print(f"      {i}. {rec}")
    
    # Record feedback and performance metrics
    print(f"\n6. Recording Feedback and Performance Metrics...")
    
    # Simulate feedback on optimization decisions
    for analysis in results['individual_analyses']:
        building_id = analysis['building_id']
        scenarios = analysis.get('optimization_scenarios', [])
        
        for scenario in scenarios:
            # Simulate feedback on optimization scenario
            feedback_data = {
                'decision_id': scenario['scenario_id'],
                'context': f"Energy optimization for {building_id}",
                'decision': scenario['type'],
                'outcome': 'positive' if scenario['potential_savings'] > 0.1 else 'neutral',
                'performance_score': scenario['potential_savings'] * 10,  # Scale to 0-10
                'feedback_timestamp': datetime.now().isoformat()
            }
            feedback_loop.record_feedback(feedback_data)
    
    # Get performance metrics
    performance_metrics = energy_agent.get_optimization_performance_metrics()
    results['performance_metrics'] = performance_metrics
    
    print(f"   📊 Performance Metrics:")
    print(f"      - Total buildings analyzed: {performance_metrics.get('total_buildings_analyzed', 0)}")
    print(f"      - Average scenarios per building: {performance_metrics.get('avg_optimization_scenarios_per_building', 0):.1f}")
    print(f"      - Total potential savings identified: {performance_metrics.get('total_potential_savings_identified', 0):.1f}%")
    print(f"      - Most common optimization type: {performance_metrics.get('most_common_optimization_type', 'none')}")
    
    # Export results
    print(f"\n7. Exporting Results...")
    results_file = "results/building_energy_demo_results.json"
    os.makedirs("results", exist_ok=True)
    
    try:
        # Convert all non-serializable objects to strings or native types
        serializable_results = make_json_serializable(results)
        with open(results_file, 'w') as f:
            json.dump(serializable_results, f, indent=2)
        print(f"   ✅ Results exported to: {results_file}")
        
    except Exception as e:
        logger.error(f"Error exporting results: {e}")
        print(f"   ❌ Failed to export results: {str(e)}")
    
    # Summary
    print(f"\n" + "=" * 80)
    print("DEMO SUMMARY")
    print("=" * 80)
    print(f"✅ Successfully analyzed {len(results['individual_analyses'])} buildings")
    print(f"✅ Detected anomalies in {len(results['anomaly_detections'])} buildings")
    print(f"✅ Generated comprehensive optimization report")
    print(f"✅ Recorded feedback for {len(results['individual_analyses'])} optimization scenarios")
    print(f"✅ Exported results to {results_file}")
    
    if optimization_report:
        total_savings = optimization_report.get('overall_statistics', {}).get('total_potential_savings_percent', 0)
        total_cost = optimization_report.get('overall_statistics', {}).get('total_implementation_cost', 0)
        print(f"\n💰 Potential Impact:")
        print(f"   - Total potential energy savings: {total_savings:.1f}%")
        print(f"   - Total implementation cost: ${total_cost:,.0f}")
        if total_cost > 0:
            roi = (total_savings * 100) / total_cost
            print(f"   - Estimated ROI: {roi:.2f}% per dollar invested")
    
    print(f"\n🎯 Key Insights:")
    print(f"   - Real building energy data provides valuable insights for optimization")
    print(f"   - AI agent can identify specific optimization opportunities for each building")
    print(f"   - Anomaly detection helps identify potential issues early")
    print(f"   - Cross-building analysis reveals patterns and opportunities for scale")
    print(f"   - Feedback loop enables continuous improvement of optimization strategies")
    
    print(f"\n🚀 Next Steps:")
    print(f"   - Implement real-time data streaming for live optimization")
    print(f"   - Add more sophisticated anomaly detection algorithms")
    print(f"   - Integrate with building management systems for automated control")
    print(f"   - Expand to include renewable energy and demand response optimization")
    
    print(f"\n" + "=" * 80)
    print("Demo completed successfully! 🎉")
    print("=" * 80)

if __name__ == "__main__":
    main() 