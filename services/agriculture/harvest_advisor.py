"""
Harvest Advisor for Weather GPT
Provides harvesting timing recommendations based on weather conditions
"""

from typing import Dict, List
from datetime import datetime, timedelta
import logging
from .crop_database import CropDatabase

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class HarvestAdvisor:
    """Provides harvesting timing recommendations based on weather conditions"""
    
    def __init__(self):
        self.crop_db = CropDatabase()
    
    def get_harvest_recommendations(self, weather_data: Dict, crop_name: str, 
                                   growth_stage: str = 'mature') -> Dict:
        """
        Get harvest recommendations for a specific crop
        
        Args:
            weather_data: Current weather data
            crop_name: Name of the crop
            growth_stage: Current growth stage of the crop
            
        Returns:
            Harvest recommendations with timing and conditions
        """
        crop_info = self.crop_db.get_crop_info(crop_name)
        if not crop_info:
            return {'error': 'Crop not found in database'}
        
        temp = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        wind_speed = weather_data.get('wind', {}).get('speed', 0) * 3.6
        weather_condition = weather_data.get('weather', [{}])[0].get('description', '').lower()
        
        # Assess current harvest conditions
        harvest_assessment = self._assess_harvest_conditions(
            crop_info, weather_data, growth_stage
        )
        
        # Get optimal harvest window
        harvest_window = self._calculate_harvest_window(
            crop_info, weather_data, harvest_assessment
        )
        
        # Get harvest precautions
        precautions = self._get_harvest_precautions(
            crop_info, weather_data, harvest_assessment
        )
        
        # Get post-harvest recommendations
        post_harvest = self._get_post_harvest_recommendations(
            crop_info, weather_data
        )
        
        return {
            'crop': crop_info['name'],
            'growth_stage': growth_stage,
            'current_conditions': {
                'temperature': temp,
                'humidity': humidity,
                'wind_speed': wind_speed,
                'weather_condition': weather_condition
            },
            'harvest_assessment': harvest_assessment,
            'harvest_window': harvest_window,
            'precautions': precautions,
            'post_harvest_recommendations': post_harvest,
            'overall_recommendation': self._generate_overall_recommendation(harvest_assessment)
        }
    
    def _assess_harvest_conditions(self, crop: Dict, weather_data: Dict, 
                                  growth_stage: str) -> Dict:
        """Assess if current conditions are suitable for harvesting"""
        temp = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        wind_speed = weather_data.get('wind', {}).get('speed', 0) * 3.6
        weather_condition = weather_data.get('weather', [{}])[0].get('description', '').lower()
        
        # Get harvest conditions from crop data
        harvest_conditions = crop.get('harvest_conditions', {})
        optimal_temp_range = harvest_conditions.get('temp_range', (20, 30))
        optimal_humidity_range = harvest_conditions.get('humidity_range', (40, 60))
        
        # Assess each condition
        temp_suitable = optimal_temp_range[0] <= temp <= optimal_temp_range[1]
        humidity_suitable = optimal_humidity_range[0] <= humidity <= optimal_humidity_range[1]
        wind_suitable = wind_speed < 20  # Generally avoid harvesting in high winds
        weather_suitable = not any adverse in weather_condition for adverse in 
                         ['storm', 'thunder', 'heavy rain', 'strong wind'])
        
        # Calculate overall suitability
        conditions_met = sum([temp_suitable, humidity_suitable, wind_suitable, weather_suitable])
        overall_suitable = conditions_met >= 3
        
        # Determine suitability level
        if overall_suitable and conditions_met == 4:
            suitability = 'EXCELLENT'
        elif overall_suitable:
            suitability = 'GOOD'
        elif conditions_met >= 2:
            suitability = 'MODERATE'
        else:
            suitability = 'POOR'
        
        return {
            'overall_suitable': overall_suitable,
            'suitability_level': suitability,
            'temperature': {
                'current': temp,
                'optimal_range': optimal_temp_range,
                'suitable': temp_suitable,
                'impact': self._get_temp_harvest_impact(temp, optimal_temp_range)
            },
            'humidity': {
                'current': humidity,
                'optimal_range': optimal_humidity_range,
                'suitable': humidity_suitable,
                'impact': self._get_humidity_harvest_impact(humidity, optimal_humidity_range)
            },
            'wind': {
                'current_speed': wind_speed,
                'suitable': wind_suitable,
                'impact': self._get_wind_harvest_impact(wind_speed)
            },
            'weather': {
                'current_condition': weather_condition,
                'suitable': weather_suitable,
                'impact': self._get_weather_harvest_impact(weather_condition)
            },
            'growth_stage_readiness': self._assess_growth_stage_readiness(growth_stage, crop)
        }
    
    def _get_temp_harvest_impact(self, temp: float, optimal_range: tuple) -> str:
        """Get temperature impact on harvest quality"""
        if optimal_range[0] <= temp <= optimal_range[1]:
            return "Optimal temperature for harvest quality"
        elif temp > optimal_range[1] + 5:
            return "High temperature - risk of quality loss and increased respiration"
        elif temp > optimal_range[1]:
            return "Slightly high temperature - may affect shelf life"
        elif temp < optimal_range[0] - 5:
            return "Low temperature - risk of chilling damage"
        elif temp < optimal_range[0]:
            return "Slightly low temperature - handle with care"
        else:
            return "Temperature conditions acceptable"
    
    def _get_humidity_harvest_impact(self, humidity: float, optimal_range: tuple) -> str:
        """Get humidity impact on harvest quality"""
        if optimal_range[0] <= humidity <= optimal_range[1]:
            return "Optimal humidity for harvest"
        elif humidity > optimal_range[1] + 15:
            return "High humidity - risk of fungal growth and post-harvest diseases"
        elif humidity > optimal_range[1]:
            return "Slightly high humidity - monitor for disease development"
        elif humidity < optimal_range[0] - 10:
            return "Low humidity - risk of desiccation and quality loss"
        elif humidity < optimal_range[0]:
            return "Slightly low humidity - may affect freshness"
        else:
            return "Humidity conditions acceptable"
    
    def _get_wind_harvest_impact(self, wind_speed: float) -> str:
        """Get wind impact on harvest operations"""
        if wind_speed < 10:
            return "Calm conditions - ideal for harvest"
        elif wind_speed < 20:
            return "Light wind - acceptable for harvest"
        elif wind_speed < 30:
            return "Moderate wind - exercise caution during harvest"
        elif wind_speed < 40:
            return "Strong wind - not ideal for harvest, consider delaying"
        else:
            return "Very strong wind - avoid harvest operations"
    
    def _get_weather_harvest_impact(self, weather_condition: str) -> str:
        """Get weather condition impact on harvest"""
        if 'clear' in weather_condition:
            return "Clear skies - excellent harvest conditions"
        elif 'cloud' in weather_condition:
            return "Cloudy conditions - good for harvest, reduces heat stress"
        elif 'rain' in weather_condition or 'drizzle' in weather_condition:
            return "Rain expected - not suitable for harvest, delay until dry"
        elif 'storm' in weather_condition or 'thunder' in weather_condition:
            return "Storm conditions - dangerous for harvest, avoid completely"
        elif 'fog' in weather_condition or 'mist' in weather_condition:
            return "Foggy conditions - may affect visibility and quality"
        else:
            return "Weather conditions should be assessed for harvest suitability"
    
    def _assess_growth_stage_readiness(self, growth_stage: str, crop: Dict) -> Dict:
        """Assess if growth stage is ready for harvest"""
        ready_stages = ['mature', 'ripe', 'ready', 'harvest_ready', 'fully_mature']
        not_ready_stages = ['seedling', 'vegetative', 'flowering', 'fruit_set', 'developing']
        
        if any(stage in growth_stage.lower() for stage in ready_stages):
            return {
                'ready': True,
                'message': 'Crop is at appropriate growth stage for harvest'
            }
        elif any(stage in growth_stage.lower() for stage in not_ready_stages):
            return {
                'ready': False,
                'message': f'Crop is at {growth_stage} stage - not ready for harvest'
            }
        else:
            return {
                'ready': True,  # Assume ready if stage is unknown
                'message': f'Growth stage "{growth_stage}" - assess readiness manually'
            }
    
    def _calculate_harvest_window(self, crop: Dict, weather_data: Dict, 
                                assessment: Dict) -> Dict:
        """Calculate optimal harvest window"""
        if assessment['overall_suitable']:
            return {
                'can_harvest_now': True,
                'optimal_time': 'Immediate - current conditions are excellent',
                'time_window': 'Next 4-6 hours',
                'best_time_of_day': self._get_best_harvest_time(weather_data),
                'next_good_window': self._predict_next_good_window(weather_data, assessment)
            }
        elif assessment['suitability_level'] == 'MODERATE':
            return {
                'can_harvest_now': True,
                'optimal_time': 'With caution - conditions are acceptable',
                'time_window': 'Next 2-3 hours if conditions remain stable',
                'best_time_of_day': self._get_best_harvest_time(weather_data),
                'next_good_window': self._predict_next_good_window(weather_data, assessment)
            }
        else:
            return {
                'can_harvest_now': False,
                'optimal_time': 'Delay harvest until conditions improve',
                'time_window': 'Not suitable currently',
                'best_time_of_day': self._get_best_harvest_time(weather_data),
                'next_good_window': self._predict_next_good_window(weather_data, assessment)
            }
    
    def _get_best_harvest_time(self, weather_data: Dict) -> str:
        """Get best time of day for harvest based on conditions"""
        temp = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        
        if temp > 30:
            return "Early morning (6-8 AM) or late evening (5-7 PM) to avoid heat"
        elif temp < 15:
            return "Late morning (10 AM - 12 PM) when temperatures are warmer"
        elif humidity > 80:
            return "Mid-morning (9-11 AM) when humidity decreases"
        else:
            return "Early morning (6-8 AM) for optimal quality and worker comfort"
    
    def _predict_next_good_window(self, weather_data: Dict, assessment: Dict) -> str:
        """Predict when next good harvest window will be"""
        current_condition = weather_data.get('weather', [{}])[0].get('description', '').lower()
        
        if 'rain' in current_condition or 'storm' in current_condition:
            return "Wait 12-24 hours after rain stops for fields to dry"
        elif 'high' in assessment['wind']['impact'] or 'strong' in assessment['wind']['impact']:
            return "Wait for wind speeds to drop below 20 km/h"
        elif not assessment['temperature']['suitable']:
            return "Wait for temperatures to enter optimal range"
        elif not assessment['humidity']['suitable']:
            return "Wait for humidity to improve (usually mid-morning)"
        else:
            return "Current conditions should improve within 6-12 hours"
    
    def _get_harvest_precautions(self, crop: Dict, weather_data: Dict, 
                                assessment: Dict) -> List[str]:
        """Get harvest precautions based on conditions"""
        precautions = []
        temp = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        wind_speed = weather_data.get('wind', {}).get('speed', 0) * 3.6
        weather_condition = weather_data.get('weather', [{}])[0].get('description', '').lower()
        
        # General precautions
        precautions.append("🧤 Clean all harvest equipment before use")
        precautions.append("👷 Ensure workers have appropriate safety equipment")
        precautions.append("📦 Use clean, ventilated containers for harvested produce")
        
        # Temperature-based precautions
        if temp > 30:
            precautions.append("🌡️ Harvest early morning or late evening to avoid heat stress")
            precautions.append("❄️ Have cooling facilities ready for immediate post-harvest cooling")
            precautions.append("💧 Provide workers with water and shade")
        elif temp < 15:
            precautions.append("🧥 Ensure workers have warm clothing")
            precautions.append("🏠 Store produce in appropriate temperature conditions")
        
        # Humidity-based precautions
        if humidity > 80:
            precautions.append("🍄 Monitor for fungal diseases during harvest")
            precautions.append("🌿 Handle produce gently to avoid damage in humid conditions")
            precautions.append("📦 Ensure proper ventilation in storage areas")
        elif humidity < 40:
            precautions.append("💧 Minimize time between harvest and cooling")
            precautions.append("🌿 Avoid excessive handling to prevent moisture loss")
        
        # Wind-based precautions
        if wind_speed > 20:
            precautions.append("💨 Secure loose materials and equipment")
            precautions.append("🛡️ Use windbreaks if possible")
            precautions.append("⚠️ Exercise caution with tall crops or equipment")
        
        # Weather-based precautions
        if 'rain' in weather_condition:
            precautions.append("🌧️ Ensure fields have adequate drainage")
            precautions.append("🚧 Avoid harvesting in wet conditions")
            precautions.append("🏠 Have indoor storage ready")
        
        # Crop-specific precautions
        if crop['storm_impact_risk'] == 'high':
            precautions.append("⚠️ Monitor weather forecasts for storm warnings")
            precautions.append("🛡️ Consider提前 harvesting if storms are predicted")
        
        precautions.append("📱 Monitor weather conditions during harvest")
        precautions.append("🚑 Have emergency plan for sudden weather changes")
        
        return precautions
    
    def _get_post_harvest_recommendations(self, crop: Dict, weather_data: Dict) -> List[str]:
        """Get post-harvest recommendations"""
        recommendations = []
        temp = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        
        # Immediate post-harvest
        recommendations.append("❄️ Cool produce immediately after harvest to maintain quality")
        recommendations.append("🧹 Clean and sanitize all post-harvest equipment")
        recommendations.append("📦 Sort produce to remove damaged items")
        
        # Storage recommendations
        if temp > 25:
            recommendations.append("❄️ Use refrigerated storage if available")
            recommendations.append("💨 Ensure adequate air circulation in storage")
        elif temp < 15:
            recommendations.append("🏠 Maintain appropriate storage temperature")
            recommendations.append("🛡️ Protect from cold drafts if necessary")
        
        if humidity > 70:
            recommendations.append("🌿 Monitor for fungal growth in storage")
            recommendations.append("💨 Use dehumidifiers if necessary")
        elif humidity < 40:
            recommendations.append("💧 Maintain appropriate humidity levels in storage")
            recommendations.append("🌿 Use humidification if needed")
        
        # Quality maintenance
        recommendations.append("📊 Monitor storage conditions regularly")
        recommendations.append("🔄 Implement first-in-first-out inventory system")
        recommendations.append("🔍 Regular quality inspections")
        
        # Crop-specific recommendations
        if crop['category'] == 'Fruit':
            recommendations.append("🍎 Handle fruits gently to avoid bruising")
            recommendations.append("📦 Use appropriate packaging for fruit types")
        elif crop['category'] == 'Vegetable':
            recommendations.append("🥬 Remove field heat quickly")
            recommendations.append("💧 Maintain appropriate humidity for leafy vegetables")
        elif crop['category'] == 'Cereal':
            recommendations.append("🌾 Ensure proper drying before storage")
            recommendations.append("🐛 Monitor for pest activity in stored grains")
        
        return recommendations
    
    def _generate_overall_recommendation(self, assessment: Dict) -> str:
        """Generate overall harvest recommendation"""
        if assessment['overall_suitable']:
            if assessment['suitability_level'] == 'EXCELLENT':
                return "✅ EXCELLENT conditions for harvest. Proceed with harvest operations immediately."
            else:
                return "✅ GOOD conditions for harvest. Proceed with standard precautions."
        elif assessment['suitability_level'] == 'MODERATE':
            return "⚠️ MODERATE conditions. Can harvest with extra precautions, but monitor conditions closely."
        else:
            return "❌ POOR conditions for harvest. Delay harvest until conditions improve. Monitor weather forecasts."
    
    def get_multi_crop_harvest_plan(self, weather_data: Dict, 
                                  crops_with_stages: List[Dict]) -> Dict:
        """
        Generate harvest plan for multiple crops
        
        Args:
            weather_data: Current weather data
            crops_with_stages: List of dicts with crop name and growth stage
            
        Returns:
            Multi-crop harvest plan
        """
        plans = []
        
        for crop_data in crops_with_stages:
            crop_name = crop_data['crop']
            growth_stage = crop_data.get('growth_stage', 'mature')
            
            plan = self.get_harvest_recommendations(weather_data, crop_name, growth_stage)
            plans.append(plan)
        
        # Sort by harvest suitability
        suitability_order = {'EXCELLENT': 0, 'GOOD': 1, 'MODERATE': 2, 'POOR': 3}
        plans.sort(key=lambda x: suitability_order.get(x['harvest_assessment']['suitability_level'], 4))
        
        # Get ready-to-harvest crops
        ready_crops = [p for p in plans if p['harvest_assessment']['growth_stage_readiness']['ready']]
        
        return {
            'timestamp': datetime.now().isoformat(),
            'weather_summary': {
                'temperature': weather_data['main']['temp'],
                'humidity': weather_data['main']['humidity'],
                'condition': weather_data.get('weather', [{}])[0].get('description', '')
            },
            'harvest_plans': plans,
            'ready_to_harvest': len(ready_crops),
            'recommended_priority': self._get_harvest_priority(plans),
            'overall_conditions': self._assess_overall_harvest_conditions(plans)
        }
    
    def _get_harvest_priority(self, plans: List[Dict]) -> List[str]:
        """Get harvest priority recommendations"""
        priority = []
        
        # Get crops that can be harvested now
        harvestable = [p for p in plans if p['harvest_window']['can_harvest_now']]
        if harvestable:
            crop_names = [c['crop'] for c in harvestable]
            priority.append(f"🌾 Priority: Harvest {', '.join(crop_names)} while conditions are favorable")
        
        # Get crops with excellent conditions
        excellent = [p for p in plans if p['harvest_assessment']['suitability_level'] == 'EXCELLENT']
        if excellent:
            crop_names = [c['crop'] for c in excellent]
            priority.append(f"⭐ Excellent conditions for: {', '.join(crop_names)}")
        
        # Get crops that should be delayed
        delay = [p for p in plans if not p['harvest_window']['can_harvest_now']]
        if delay:
            crop_names = [c['crop'] for c in delay]
            priority.append(f"⏸️ Delay harvest for: {', '.join(crop_names)} until conditions improve")
        
        return priority if priority else ["Monitor all crops and conditions"]
    
    def _assess_overall_harvest_conditions(self, plans: List[Dict]) -> str:
        """Assess overall conditions for multi-crop harvest"""
        if not plans:
            return "No crops specified for harvest planning"
        
        harvestable = sum(1 for p in plans if p['harvest_window']['can_harvest_now'])
        total = len(plans)
        
        if harvestable == total:
            return f"Excellent conditions - all {total} crops can be harvested"
        elif harvestable >= total * 0.7:
            return f"Good conditions - {harvestable}/{total} crops can be harvested"
        elif harvestable >= total * 0.5:
            return f"Moderate conditions - {harvestable}/{total} crops can be harvested with caution"
        else:
            return f"Poor conditions - only {harvestable}/{total} crops suitable for harvest"