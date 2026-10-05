"""
Storm Impact Analyzer for Weather GPT
Analyzes storm impact on crops and provides protection/recovery recommendations
"""

from typing import Dict, List
from datetime import datetime, timedelta
import logging
from .crop_database import CropDatabase

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class StormImpactAnalyzer:
    """Analyzes storm impact on crops and provides protection/recovery recommendations"""
    
    def __init__(self):
        self.crop_db = CropDatabase()
    
    def analyze_storm_impact(self, weather_data: Dict, crop_name: str, 
                           current_growth_stage: str = 'mature') -> Dict:
        """
        Analyze storm impact on a specific crop
        
        Args:
            weather_data: Current weather data
            crop_name: Name of the crop
            current_growth_stage: Current growth stage of the crop
            
        Returns:
            Storm impact analysis with recommendations
        """
        crop_info = self.crop_db.get_crop_info(crop_name)
        if not crop_info:
            return {'error': 'Crop not found in database'}
        
        temp = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        wind_speed = weather_data.get('wind', {}).get('speed', 0) * 3.6
        weather_condition = weather_data.get('weather', [{}])[0].get('description', '').lower()
        weather_id = weather_data.get('weather', [{}])[0].get('id', 0)
        
        # Determine storm severity
        storm_severity = self._determine_storm_severity(weather_data, weather_id)
        
        # Analyze impact on crop
        impact_analysis = self._analyze_crop_impact(
            crop_info, storm_severity, current_growth_stage, weather_data
        )
        
        # Get protection measures
        protection_measures = self._get_protection_measures(
            crop_info, storm_severity, current_growth_stage
        )
        
        # Get recovery recommendations
        recovery_recommendations = self._get_recovery_recommendations(
            crop_info, storm_severity, impact_analysis
        )
        
        # Get damage assessment
        damage_assessment = self._assess_potential_damage(
            crop_info, storm_severity, current_growth_stage
        )
        
        return {
            'crop': crop_info['name'],
            'growth_stage': current_growth_stage,
            'storm_severity': storm_severity,
            'current_conditions': {
                'temperature': temp,
                'humidity': humidity,
                'wind_speed': wind_speed,
                'weather_condition': weather_condition,
                'weather_id': weather_id
            },
            'impact_analysis': impact_analysis,
            'damage_assessment': damage_assessment,
            'protection_measures': protection_measures,
            'recovery_recommendations': recovery_recommendations,
            'overall_risk_level': self._calculate_overall_risk(
                crop_info, storm_severity, current_growth_stage
            ),
            'action_priority': self._determine_action_priority(storm_severity, impact_analysis)
        }
    
    def _determine_storm_severity(self, weather_data: Dict, weather_id: int) -> Dict:
        """Determine the severity of the storm"""
        wind_speed = weather_data.get('wind', {}).get('speed', 0) * 3.6
        weather_condition = weather_data.get('weather', [{}])[0].get('description', '').lower()
        
        # Weather ID based severity (OpenWeatherMap codes)
        if weather_id in [781]:  # Tornado
            severity = 'EXTREME'
            severity_score = 10
        elif weather_id in [962, 961]:  # Hurricane
            severity = 'EXTREME'
            severity_score = 10
        elif weather_id in [230, 231, 232]:  # Thunderstorm with heavy rain
            severity = 'SEVERE'
            severity_score = 8
        elif weather_id in [200, 201, 202, 211, 212, 221]:  # Thunderstorm
            severity = 'SEVERE'
            severity_score = 7
        elif weather_id in [502, 503, 504]:  # Heavy rain
            severity = 'HIGH'
            severity_score = 6
        elif weather_id in [511, 520, 521, 522]:  # Freezing rain/showers
            severity = 'SEVERE'
            severity_score = 8
        elif wind_speed > 60:
            severity = 'SEVERE'
            severity_score = 7
        elif wind_speed > 40:
            severity = 'HIGH'
            severity_score = 5
        elif 'storm' in weather_condition or 'thunder' in weather_condition:
            severity = 'MODERATE'
            severity_score = 4
        elif 'rain' in weather_condition:
            severity = 'LOW'
            severity_score = 2
        else:
            severity = 'NONE'
            severity_score = 0
        
        return {
            'level': severity,
            'score': severity_score,
            'description': self._get_severity_description(severity)
        }
    
    def _get_severity_description(self, severity: str) -> str:
        """Get description for severity level"""
        descriptions = {
            'EXTREME': 'Life-threatening storm with catastrophic potential',
            'SEVERE': 'Dangerous storm with significant damage potential',
            'HIGH': 'Strong storm with moderate damage potential',
            'MODERATE': 'Moderate storm with some damage potential',
            'LOW': 'Light storm with minimal damage potential',
            'NONE': 'No storm conditions detected'
        }
        return descriptions.get(severity, 'Unknown severity')
    
    def _analyze_crop_impact(self, crop: Dict, storm_severity: Dict, 
                           growth_stage: str, weather_data: Dict) -> Dict:
        """Analyze the impact of storm on the crop"""
        severity_score = storm_severity['score']
        crop_storm_risk = crop.get('storm_impact_risk', 'medium')
        
        # Calculate risk multiplier based on crop characteristics
        risk_multipliers = {
            'very_high': 2.0,
            'high': 1.5,
            'medium': 1.0,
            'low': 0.5
        }
        risk_multiplier = risk_multipliers.get(crop_storm_risk, 1.0)
        
        # Calculate base impact score
        base_impact = severity_score * risk_multiplier
        
        # Growth stage sensitivity
        sensitive_stages = crop.get('sensitive_stages', {})
        stage_sensitivity = 1.0
        
        for stage, conditions in sensitive_stages.items():
            if stage in growth_stage.lower():
                stage_sensitivity = 1.5  # Sensitive stages are more vulnerable
                break
        
        final_impact_score = min(10, base_impact * stage_sensitivity)
        
        # Determine impact level
        if final_impact_score >= 8:
            impact_level = 'CATASTROPHIC'
        elif final_impact_score >= 6:
            impact_level = 'SEVERE'
        elif final_impact_score >= 4:
            impact_level = 'MODERATE'
        elif final_impact_score >= 2:
            impact_level = 'MINOR'
        else:
            impact_level = 'NEGLIGIBLE'
        
        # Specific impact types
        impact_types = self._determine_impact_types(crop, storm_severity, weather_data)
        
        return {
            'impact_score': round(final_impact_score, 2),
            'impact_level': impact_level,
            'crop_storm_risk': crop_storm_risk,
            'risk_multiplier': risk_multiplier,
            'stage_sensitivity': stage_sensitivity,
            'impact_types': impact_types,
            'expected_damage_percentage': self._estimate_damage_percentage(final_impact_score)
        }
    
    def _determine_impact_types(self, crop: Dict, storm_severity: Dict, 
                              weather_data: Dict) -> List[str]:
        """Determine specific types of storm impact"""
        impact_types = []
        wind_speed = weather_data.get('wind', {}).get('speed', 0) * 3.6
        weather_condition = weather_data.get('weather', [{}])[0].get('description', '').lower()
        weather_id = weather_data.get('weather', [{}])[0].get('id', 0)
        
        # Wind damage
        if wind_speed > 30:
            if crop['wind_tolerance'] == 'low':
                impact_types.append("Wind damage (lodging, breakage)")
            elif crop['wind_tolerance'] == 'medium':
                impact_types.append("Moderate wind damage")
            else:
                impact_types.append("Potential wind damage")
        
        # Rain/flooding damage
        if 'rain' in weather_condition or weather_id in [502, 503, 504]:
            if crop['flood_tolerance'] == 'low':
                impact_types.append("Flooding damage (waterlogging, root rot)")
            elif crop['flood_tolerance'] == 'medium':
                impact_types.append("Moderate flooding risk")
            else:
                impact_types.append("Low flooding risk")
        
        # Hail damage (if we had hail data)
        if weather_id in [903, 904, 905, 906]:  # Hail codes
            impact_types.append("Hail damage (physical damage to plants)")
        
        # Lightning damage
        if 'thunder' in weather_condition or weather_id in [200, 201, 202, 211, 212, 221]:
            impact_types.append("Lightning strike risk")
        
        # Temperature damage
        temp = weather_data['main']['temp']
        if temp < 5:
            impact_types.append("Cold damage/frost")
        elif temp > 35:
            impact_types.append("Heat stress damage")
        
        # Disease risk
        humidity = weather_data['main']['humidity']
        if humidity > 80:
            impact_types.append("Fungal disease outbreak risk")
        
        # Physical damage
        if storm_severity['level'] in ['SEVERE', 'EXTREME']:
            impact_types.append("Physical structural damage")
        
        return impact_types if impact_types else ["General storm stress"]
    
    def _estimate_damage_percentage(self, impact_score: float) -> str:
        """Estimate potential damage percentage"""
        if impact_score >= 8:
            return "70-100% damage expected"
        elif impact_score >= 6:
            return "40-70% damage expected"
        elif impact_score >= 4:
            return "20-40% damage expected"
        elif impact_score >= 2:
            return "5-20% damage expected"
        else:
            return "Minimal damage expected (<5%)"
    
    def _get_protection_measures(self, crop: Dict, storm_severity: Dict, 
                                growth_stage: str) -> Dict:
        """Get protection measures based on storm severity"""
        severity = storm_severity['level']
        measures = {
            'immediate': [],
            'short_term': [],
            'long_term': []
        }
        
        # Immediate measures (pre-storm)
        if severity in ['EXTREME', 'SEVERE']:
            measures['immediate'].extend([
                "🚨 EVACUATE: Ensure human safety first - move to secure location",
                "🚨 Secure all equipment and movable structures",
                "🚨 Install windbreaks or storm barriers if time permits",
                "🚨 Harvest mature crops if possible to minimize losses",
                "🚨 Protect sensitive growth stages with covers or shelters"
            ])
        elif severity == 'HIGH':
            measures['immediate'].extend([
                "💨 Install windbreaks or supports for vulnerable plants",
                "💨 Secure irrigation systems and equipment",
                "💨 Apply protective covers for sensitive crops",
                "💨 Ensure drainage systems are clear and functional"
            ])
        elif severity == 'MODERATE':
            measures['immediate'].extend([
                "🌿 Monitor weather conditions closely",
                "🌿 Prepare protective materials if needed",
                "🌿 Check and reinforce plant supports"
            ])
        
        # Crop-specific measures
        if crop['wind_tolerance'] == 'low':
            measures['immediate'].append("🌱 Stake or support all plants immediately")
            measures['immediate'].append("🌿 Install windbreaks around vulnerable areas")
        
        if crop['flood_tolerance'] == 'low':
            measures['immediate'].append("🌊 Ensure drainage systems are operational")
            measures['immediate'].append("🌊 Create raised beds or mounds if possible")
        
        if crop['storm_impact_risk'] == 'very_high':
            measures['immediate'].append("⚠️ Consider emergency harvest if crops are mature")
            measures['immediate'].append("🛡️ Provide maximum protection possible")
        
        # Short-term measures (during storm)
        measures['short_term'].extend([
            "📱 Stay updated with weather alerts and forecasts",
            "📊 Monitor field conditions from safe location",
            "🚑 Keep emergency contact numbers accessible",
            "📷 Document conditions for insurance purposes if applicable"
        ])
        
        # Long-term measures (post-storm preparation)
        measures['long_term'].extend([
            "🌳 Plant windbreaks for future protection",
            "💧 Improve drainage infrastructure",
            "🛡️ Invest in permanent protective structures",
            "📈 Select storm-resistant crop varieties for high-risk areas",
            "📊 Develop storm response plan for farm"
        ])
        
        return measures
    
    def _get_recovery_recommendations(self, crop: Dict, storm_severity: Dict, 
                                    impact_analysis: Dict) -> Dict:
        """Get recovery recommendations based on impact"""
        impact_level = impact_analysis['impact_level']
        recovery = {
            'immediate_actions': [],
            'short_term_recovery': [],
            'long_term_recovery': []
        }
        
        # Immediate actions (post-storm)
        recovery['immediate_actions'].extend([
            "🔍 Assess damage as soon as it's safe to enter fields",
            "📷 Document all damage with photos for records/insurance",
            "🚑 Prioritize human safety during damage assessment",
            "💧 Check drainage and address waterlogging immediately",
            "🌿 Remove debris and damaged plant material"
        ])
        
        if impact_level in ['CATASTROPHIC', 'SEVERE']:
            recovery['immediate_actions'].extend([
                "🚨 Contact agricultural extension services for guidance",
                "🚨 Report significant losses to relevant authorities if applicable",
                "🚨 Consider emergency financial assistance programs"
            ])
        
        # Short-term recovery (1-2 weeks)
        recovery['short_term_recovery'].extend([
            "🌱 Support damaged plants with staking if possible",
            "💧 Adjust irrigation based on soil moisture and damage",
            "🍄 Monitor for disease outbreaks in damaged areas",
            "🐛 Increase pest monitoring as damaged plants are more susceptible",
            "🌿 Apply appropriate fertilizers to support recovery"
        ])
        
        if impact_level in ['CATASTROPHIC', 'SEVERE']:
            recovery['short_term_recovery'].extend([
                "🔄 Consider replanting if damage is extensive",
                "🔄 Adjust planting schedule for next season",
                "💰 Assess financial impact and recovery options"
            ])
        
        # Long-term recovery (1-3 months)
        recovery['long_term_recovery'].extend([
            "📊 Evaluate crop performance and recovery progress",
            "🌱 Plan for next season with lessons learned",
            "🛡️ Implement improved protection measures",
            "📈 Update farm management practices based on storm experience",
            "💰 Review and update insurance coverage if applicable"
        ])
        
        return recovery
    
    def _assess_potential_damage(self, crop: Dict, storm_severity: Dict, 
                               growth_stage: str) -> Dict:
        """Assess potential damage to different crop components"""
        severity = storm_severity['score']
        
        damage_assessment = {
            'foliage_damage': self._assess_foliage_damage(crop, severity),
            'stem_damage': self._assess_stem_damage(crop, severity),
            'root_damage': self._assess_root_damage(crop, severity, storm_severity),
            'reproductive_damage': self._assess_reproductive_damage(crop, severity, growth_stage),
            'quality_impact': self._assess_quality_impact(crop, severity, growth_stage),
            'yield_impact': self._assess_yield_impact(crop, severity, growth_stage)
        }
        
        return damage_assessment
    
    def _assess_foliage_damage(self, crop: Dict, severity: float) -> str:
        """Assess potential foliage damage"""
        if severity >= 8:
            return "Severe leaf damage and defoliation expected"
        elif severity >= 6:
            return "Significant leaf damage and tearing expected"
        elif severity >= 4:
            return "Moderate leaf damage expected"
        elif severity >= 2:
            return "Minor leaf damage possible"
        else:
            return "Minimal foliage damage expected"
    
    def _assess_stem_damage(self, crop: Dict, severity: float) -> str:
        """Assess potential stem damage"""
        wind_tolerance = crop.get('wind_tolerance', 'medium')
        
        if wind_tolerance == 'low':
            if severity >= 6:
                return "High risk of stem breakage and lodging"
            elif severity >= 4:
                return "Moderate risk of stem damage"
            else:
                return "Low risk of stem damage"
        elif wind_tolerance == 'medium':
            if severity >= 8:
                return "Significant stem damage risk"
            elif severity >= 6:
                return "Moderate stem damage risk"
            else:
                return "Low stem damage risk"
        else:
            if severity >= 8:
                return "Some stem damage possible in extreme conditions"
            else:
                return "Minimal stem damage risk"
    
    def _assess_root_damage(self, crop: Dict, severity: float, storm_severity: Dict) -> str:
        """Assess potential root damage"""
        flood_tolerance = crop.get('flood_tolerance', 'medium')
        weather_condition = storm_severity.get('description', '').lower()
        
        if 'rain' in weather_condition or 'flood' in weather_condition:
            if flood_tolerance == 'low':
                return "High risk of root damage from waterlogging"
            elif flood_tolerance == 'medium':
                return "Moderate root damage risk from excess water"
            else:
                return "Low root damage risk"
        else:
            return "Root damage primarily from wind stress (minor)"
    
    def _assess_reproductive_damage(self, crop: Dict, severity: float, growth_stage: str) -> str:
        """Assess potential damage to reproductive structures"""
        sensitive_stages = ['flowering', 'fruit_set', 'grain_filling', 'pollination']
        
        if any(stage in growth_stage.lower() for stage in sensitive_stages):
            if severity >= 6:
                return "High risk of flower/fruit loss and reproductive failure"
            elif severity >= 4:
                return "Moderate risk of reproductive damage"
            else:
                return "Some reproductive damage possible"
        else:
            return "Reproductive structures not significantly affected at current stage"
    
    def _assess_quality_impact(self, crop: Dict, severity: float, growth_stage: str) -> str:
        """Assess impact on crop quality"""
        if severity >= 6:
            return "Significant quality reduction expected"
        elif severity >= 4:
            return "Moderate quality impact likely"
        elif severity >= 2:
            return "Minor quality impact possible"
        else:
            return "Minimal quality impact expected"
    
    def _assess_yield_impact(self, crop: Dict, severity: float, growth_stage: str) -> str:
        """Assess impact on yield"""
        if severity >= 8:
            return "Catastrophic yield loss (70-100%)"
        elif severity >= 6:
            return "Severe yield loss (40-70%)"
        elif severity >= 4:
            return "Moderate yield loss (20-40%)"
        elif severity >= 2:
            return "Minor yield loss (5-20%)"
        else:
            return "Minimal yield impact (<5%)"
    
    def _calculate_overall_risk(self, crop: Dict, storm_severity: Dict, 
                               growth_stage: str) -> str:
        """Calculate overall risk level"""
        severity_score = storm_severity['score']
        crop_risk = crop.get('storm_impact_risk', 'medium')
        
        # Calculate combined risk
        risk_values = {'very_high': 3, 'high': 2, 'medium': 1, 'low': 0}
        crop_risk_value = risk_values.get(crop_risk, 1)
        
        combined_risk = severity_score + crop_risk_value
        
        if combined_risk >= 10:
            return "EXTREME RISK"
        elif combined_risk >= 8:
            return "HIGH RISK"
        elif combined_risk >= 5:
            return "MODERATE RISK"
        elif combined_risk >= 3:
            return "LOW RISK"
        else:
            return "MINIMAL RISK"
    
    def _determine_action_priority(self, storm_severity: Dict, impact_analysis: Dict) -> str:
        """Determine action priority based on storm severity and impact"""
        severity = storm_severity['level']
        impact_level = impact_analysis['impact_level']
        
        if severity in ['EXTREME', 'SEVERE'] or impact_level in ['CATASTROPHIC', 'SEVERE']:
            return "IMMEDIATE ACTION REQUIRED"
        elif severity == 'HIGH' or impact_level == 'MODERATE':
            return "HIGH PRIORITY"
        elif severity == 'MODERATE' or impact_level == 'MINOR':
            return "MODERATE PRIORITY"
        else:
            return "MONITOR ONLY"
    
    def get_multi_crop_storm_analysis(self, weather_data: Dict, 
                                     crops_with_stages: List[Dict]) -> Dict:
        """
        Analyze storm impact on multiple crops
        
        Args:
            weather_data: Current weather data
            crops_with_stages: List of dicts with crop name and growth stage
            
        Returns:
            Multi-crop storm impact analysis
        """
        analyses = []
        
        for crop_data in crops_with_stages:
            crop_name = crop_data['crop']
            growth_stage = crop_data.get('growth_stage', 'mature')
            
            analysis = self.analyze_storm_impact(weather_data, crop_name, growth_stage)
            analyses.append(analysis)
        
        # Sort by risk level
        risk_order = {'EXTREME RISK': 0, 'HIGH RISK': 1, 'MODERATE RISK': 2, 
                     'LOW RISK': 3, 'MINIMAL RISK': 4}
        analyses.sort(key=lambda x: risk_order.get(x['overall_risk_level'], 5))
        
        # Get high-risk crops
        high_risk_crops = [a for a in analyses if a['overall_risk_level'] in ['EXTREME RISK', 'HIGH RISK']]
        
        return {
            'timestamp': datetime.now().isoformat(),
            'storm_severity': analyses[0]['storm_severity'] if analyses else {'level': 'NONE'},
            'crop_analyses': analyses,
            'high_risk_crops': len(high_risk_crops),
            'recommended_actions': self._generate_multi_crop_actions(analyses),
            'overall_assessment': self._generate_overall_storm_assessment(analyses)
        }
    
    def _generate_multi_crop_actions(self, analyses: List[Dict]) -> List[str]:
        """Generate recommended actions for multiple crops"""
        actions = []
        
        if not analyses:
            return ["No crops specified for storm analysis"]
        
        # Check for extreme risk crops
        extreme_risk = [a for a in analyses if a['overall_risk_level'] == 'EXTREME RISK']
        if extreme_risk:
            crop_names = [c['crop'] for c in extreme_risk]
            actions.append(f"🚨 EXTREME RISK: Implement maximum protection for {', '.join(crop_names)}")
        
        # Check for high risk crops
        high_risk = [a for a in analyses if a['overall_risk_level'] == 'HIGH RISK']
        if high_risk:
            crop_names = [c['crop'] for c in high_risk]
            actions.append(f"⚠️ HIGH RISK: Prioritize protection for {', '.join(crop_names)}")
        
        # General recommendations
        actions.append("📱 Monitor weather forecasts closely")
        actions.append("🛡️ Prepare protection measures for all vulnerable crops")
        actions.append("💧 Ensure drainage systems are functional")
        actions.append("📋 Document conditions for potential insurance claims")
        
        return actions
    
    def _generate_overall_storm_assessment(self, analyses: List[Dict]) -> str:
        """Generate overall storm assessment for multiple crops"""
        if not analyses:
            return "No crops specified for storm analysis"
        
        high_risk_count = sum(1 for a in analyses if a['overall_risk_level'] in ['EXTREME RISK', 'HIGH RISK'])
        total_count = len(analyses)
        
        if high_risk_count == 0:
            return f"Storm poses minimal risk to all {total_count} crops"
        elif high_risk_count <= total_count * 0.3:
            return f"Storm poses moderate risk - {high_risk_count}/{total_count} crops at high risk"
        elif high_risk_count <= total_count * 0.7:
            return f"Storm poses significant risk - {high_risk_count}/{total_count} crops at high risk"
        else:
            return f"Storm poses severe risk - {high_risk_count}/{total_count} crops at high risk"