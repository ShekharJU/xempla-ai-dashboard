"""
Energy Optimization Agent for Xempla AI Systems Intern Prototype

This agent specializes in energy efficiency optimization using real building
energy consumption data and weather information.
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import pandas as pd
import numpy as np

from src.agents.ai_agent import AIAgent
from src.simulation.building_data_loader import BuildingEnergyDataLoader

logger = logging.getLogger(__name__)

class EnergyOptimizationAgent(AIAgent):
    """
    Specialized agent for energy efficiency optimization using real building data
    """
    
    def __init__(self, learning_rate: float = 0.12):
        super().__init__('energy_optimization', learning_rate=learning_rate)
        self.data_loader = BuildingEnergyDataLoader()
        self.optimization_history = []
        
        logger.info("Initialized Energy Optimization Agent")
    
    def analyze_building_efficiency(self, building_id: str) -> Dict[str, Any]:
        """
        Analyze energy efficiency of a specific building
        
        Args:
            building_id: Building identifier
            
        Returns:
            Dictionary with efficiency analysis and recommendations
        """
        # Get building data and features
        features = self.data_loader.get_energy_efficiency_features(building_id)
        if features is None:
            return {'error': f'Unable to load data for building {building_id}'}
        
        # Get optimization scenarios
        scenarios = self.data_loader.get_optimization_scenarios(building_id)
        
        # Create operational context for LLM
        operational_context = {
            'building_id': building_id,
            'total_energy_consumption': features['total_energy_consumption'],
            'avg_daily_consumption': features['avg_daily_consumption'],
            'peak_consumption': features['peak_consumption'],
            'energy_intensity': features['energy_intensity'],
            'avg_temperature': features['avg_temperature'],
            'heating_degree_days': features['heating_degree_days'],
            'cooling_degree_days': features['cooling_degree_days'],
            'optimization_scenarios': scenarios
        }
        
        # Make optimization decision
        decision_result = self.make_decision(operational_context, 'energy_optimization')
        
        # Add analysis results
        analysis_result = {
            'building_id': building_id,
            'analysis_timestamp': datetime.now().isoformat(),
            'efficiency_features': features,
            'optimization_scenarios': scenarios,
            'ai_recommendations': decision_result,
            'priority_actions': self._extract_priority_actions(decision_result, scenarios)
        }
        
        self.optimization_history.append(analysis_result)
        
        return analysis_result
    
    def detect_energy_anomalies(self, building_id: str) -> Dict[str, Any]:
        """
        Detect anomalies in energy consumption patterns
        
        Args:
            building_id: Building identifier
            
        Returns:
            Dictionary with anomaly detection results
        """
        # Get anomaly detection data
        anomaly_data = self.data_loader.get_anomaly_detection_data(building_id)
        if anomaly_data is None:
            return {'error': f'Unable to load anomaly data for building {building_id}'}
        
        # Calculate anomaly scores using statistical methods
        energy_consumption = anomaly_data['energy_consumption']
        mean_consumption = energy_consumption.mean()
        std_consumption = energy_consumption.std()
        
        # Identify anomalies (values beyond 2 standard deviations)
        anomaly_threshold = mean_consumption + 2 * std_consumption
        anomalies = energy_consumption[energy_consumption > anomaly_threshold]
        
        # Create operational context for LLM
        operational_context = {
            'building_id': building_id,
            'total_data_points': len(anomaly_data),
            'anomaly_count': len(anomalies),
            'anomaly_percentage': (len(anomalies) / len(anomaly_data)) * 100,
            'max_anomaly_value': anomalies.max() if len(anomalies) > 0 else 0,
            'avg_consumption': mean_consumption,
            'consumption_std': std_consumption
        }
        
        # Make anomaly diagnosis decision
        decision_result = self.make_decision(operational_context, 'fault_diagnosis')
        
        return {
            'building_id': building_id,
            'analysis_timestamp': datetime.now().isoformat(),
            'anomaly_statistics': {
                'total_points': len(anomaly_data),
                'anomaly_count': len(anomalies),
                'anomaly_percentage': (len(anomalies) / len(anomaly_data)) * 100,
                'max_anomaly': anomalies.max() if len(anomalies) > 0 else 0,
                'anomaly_threshold': anomaly_threshold
            },
            'ai_diagnosis': decision_result,
            'anomaly_timestamps': anomalies.index.tolist() if len(anomalies) > 0 else []
        }
    
    def generate_optimization_report(self, building_ids: List[str]) -> Dict[str, Any]:
        """
        Generate comprehensive optimization report for multiple buildings
        
        Args:
            building_ids: List of building identifiers
            
        Returns:
            Dictionary with comprehensive optimization report
        """
        report = {
            'report_timestamp': datetime.now().isoformat(),
            'buildings_analyzed': len(building_ids),
            'building_analyses': [],
            'overall_statistics': {},
            'cross_building_recommendations': []
        }
        
        total_potential_savings = 0
        total_implementation_cost = 0
        
        for building_id in building_ids:
            try:
                analysis = self.analyze_building_efficiency(building_id)
                if 'error' not in analysis:
                    report['building_analyses'].append(analysis)
                    
                    # Calculate potential savings
                    scenarios = analysis.get('optimization_scenarios', [])
                    for scenario in scenarios:
                        total_potential_savings += scenario.get('potential_savings', 0) * 100  # Convert to percentage
                        total_implementation_cost += scenario.get('implementation_cost', 0)
                        
            except Exception as e:
                logger.error(f"Error analyzing building {building_id}: {e}")
                report['building_analyses'].append({
                    'building_id': building_id,
                    'error': str(e)
                })
        
        # Calculate overall statistics
        if report['building_analyses']:
            successful_analyses = [a for a in report['building_analyses'] if 'error' not in a]
            if successful_analyses:
                report['overall_statistics'] = {
                    'successful_analyses': len(successful_analyses),
                    'avg_energy_intensity': np.mean([a['efficiency_features']['energy_intensity'] for a in successful_analyses]),
                    'total_potential_savings_percent': total_potential_savings,
                    'total_implementation_cost': total_implementation_cost,
                    'avg_payback_period': self._calculate_avg_payback_period(successful_analyses)
                }
        
        # Generate cross-building recommendations
        report['cross_building_recommendations'] = self._generate_cross_building_recommendations(report['building_analyses'])
        
        return report
    
    def _extract_priority_actions(self, decision_result: Dict, scenarios: List[Dict]) -> List[Dict]:
        """Extract priority actions from AI decision and scenarios"""
        priority_actions = []
        
        # Add AI recommendations
        if 'recommendations' in decision_result:
            for i, rec in enumerate(decision_result['recommendations'][:3]):
                priority_actions.append({
                    'action_id': f'ai_recommendation_{i+1}',
                    'type': 'ai_recommendation',
                    'description': rec,
                    'priority': 'high' if i == 0 else 'medium',
                    'estimated_impact': 'significant'
                })
        
        # Add scenario-based actions
        for scenario in scenarios:
            priority_actions.append({
                'action_id': scenario['scenario_id'],
                'type': scenario['type'],
                'description': f"Implement {scenario['type'].replace('_', ' ')} optimization",
                'priority': 'high' if scenario['potential_savings'] > 0.15 else 'medium',
                'estimated_impact': f"{scenario['potential_savings']*100:.1f}% energy savings",
                'implementation_cost': scenario['implementation_cost'],
                'payback_period': scenario['payback_period_months']
            })
        
        # Sort by priority
        priority_order = {'high': 1, 'medium': 2, 'low': 3}
        priority_actions.sort(key=lambda x: priority_order.get(x['priority'], 4))
        
        return priority_actions[:5]  # Return top 5 actions
    
    def _calculate_avg_payback_period(self, analyses: List[Dict]) -> float:
        """Calculate average payback period across analyses"""
        payback_periods = []
        
        for analysis in analyses:
            scenarios = analysis.get('optimization_scenarios', [])
            for scenario in scenarios:
                if 'payback_period_months' in scenario:
                    payback_periods.append(scenario['payback_period_months'])
        
        return np.mean(payback_periods) if payback_periods else 0
    
    def _generate_cross_building_recommendations(self, analyses: List[Dict]) -> List[str]:
        """Generate recommendations that apply across multiple buildings"""
        recommendations = []
        
        # Find common patterns
        energy_intensities = []
        common_issues = []
        
        for analysis in analyses:
            if 'error' not in analysis:
                features = analysis.get('efficiency_features', {})
                energy_intensities.append(features.get('energy_intensity', 0))
                
                # Identify common issues
                if features.get('energy_intensity', 0) > 100:  # High energy intensity
                    common_issues.append('high_energy_intensity')
                if features.get('heating_degree_days', 0) > 2000:  # High heating needs
                    common_issues.append('high_heating_needs')
                if features.get('cooling_degree_days', 0) > 1500:  # High cooling needs
                    common_issues.append('high_cooling_needs')
        
        # Generate recommendations based on patterns
        if len(energy_intensities) > 0:
            avg_intensity = np.mean(energy_intensities)
            if avg_intensity > 80:
                recommendations.append("Implement building-wide energy monitoring and control systems")
            
            if common_issues.count('high_energy_intensity') > len(analyses) * 0.5:
                recommendations.append("Conduct energy audits and implement building envelope improvements")
            
            if common_issues.count('high_heating_needs') > len(analyses) * 0.3:
                recommendations.append("Upgrade HVAC systems and implement smart thermostats")
            
            if common_issues.count('high_cooling_needs') > len(analyses) * 0.3:
                recommendations.append("Optimize cooling systems and implement demand-based control")
        
        # Add general recommendations
        recommendations.extend([
            "Establish energy efficiency training programs for building operators",
            "Implement real-time energy monitoring dashboards",
            "Set up automated alerts for energy consumption anomalies"
        ])
        
        return recommendations[:5]  # Return top 5 recommendations
    
    def get_optimization_performance_metrics(self) -> Dict[str, Any]:
        """Get performance metrics for the energy optimization agent"""
        base_metrics = self.get_performance_insights()
        
        # Add energy-specific metrics
        energy_metrics = {
            'total_buildings_analyzed': len(self.optimization_history),
            'avg_optimization_scenarios_per_building': np.mean([
                len(analysis.get('optimization_scenarios', [])) 
                for analysis in self.optimization_history
            ]) if self.optimization_history else 0,
            'total_potential_savings_identified': sum([
                sum([scenario.get('potential_savings', 0) * 100 for scenario in analysis.get('optimization_scenarios', [])])
                for analysis in self.optimization_history
            ]),
            'most_common_optimization_type': self._get_most_common_optimization_type()
        }
        
        base_metrics.update(energy_metrics)
        return base_metrics
    
    def _get_most_common_optimization_type(self) -> str:
        """Get the most common optimization type across all analyses"""
        optimization_types = []
        
        for analysis in self.optimization_history:
            scenarios = analysis.get('optimization_scenarios', [])
            for scenario in scenarios:
                optimization_types.append(scenario.get('type', 'unknown'))
        
        if optimization_types:
            from collections import Counter
            return Counter(optimization_types).most_common(1)[0][0]
        
        return 'none' 