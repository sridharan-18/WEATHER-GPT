"""
Crop Advisor for Weather GPT
Provides crop-specific recommendations based on weather conditions
"""

from typing import Dict, List
import logging
from .crop_database import CropDatabase

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CropAdvisor:
    """Provides crop-specific recommendations based on weather conditions"""
    
    def __init__(self):
        self.crop_db = CropDatabase()
    
    def get_crop_recommendations(self, weather_data: Dict, location: str = None) -> Dict:
        """
        Get crop recommendations based on current weather conditions
        
        Args:
            weather_data: Current weather data
            location: Location name (optional)
            
        Returns:
            Dictionary with crop recommendations and assessments
        """
        temp = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        wind_speed = weather_data.get('wind', {}).get('speed', 0) * 3.6
        rainfall = weather_data.get('rain', {}).get('1h', 0)  # 1-hour rainfall in mm
        
        all_crops = self.crop_db.get_all_crops()
        recommendations = []
        
        for crop in all_crops:
            assessment = self.crop_db.assess_weather_suitability(crop['name'], weather_data)
            
            # Calculate suitability score
            score = self._calculate_suitability_score(assessment, crop)
            
            # Get specific recommendations
            specific_recommendations = self._generate_crop_recommendations(
                crop, weather_data, assessment
            )
            
            recommendations.append({
                'crop': crop['name'],
                'category': crop['category'],
                'suitability_score': score,
                'suitable': assessment['suitable'],
                'assessment': assessment,
                'recommendations': specific_recommendations,
                'risk_factors': self._identify_risk_factors(crop, weather_data)
            })
        
        # Sort by suitability score
        recommendations.sort(key=lambda x: x['suitability_score'], reverse=True)
        
        return {
            'location': location,
            'current_conditions': {
                'temperature': temp,
                'humidity': humidity,
                'wind_speed': wind_speed,
                'rainfall': rainfall
            },
            'recommendations': recommendations[:5],  # Top 5 recommendations
            'summary': self._generate_summary(recommendations)
        }
    
    def _calculate_suitability_score(self, assessment: Dict, crop: Dict) -> int:
        """Calculate a suitability score (0-100) for a crop"""
        score = 100
        
        # Temperature deviation penalty
        temp_deviation = abs(assessment['temperature']['deviation'])
        temp_penalty = min(temp_deviation * 5, 40)  # Max 40 points penalty
        score -= temp_penalty
        
        # Humidity deviation penalty
        humidity_deviation = abs(assessment['humidity']['deviation'])
        humidity_penalty = min(humidity_deviation * 2, 30)  # Max 30 points penalty
        score -= humidity_penalty
        
        # Wind penalty
        if not assessment['wind']['suitable']:
            score -= 20
        
        # Overall suitability bonus/penalty
        if assessment['suitable']:
            score += 10  # Bonus for overall suitability
        else:
            score -= 10  # Penalty for overall unsuitability
        
        return max(0, min(100, score))
    
    def _generate_crop_recommendations(self, crop: Dict, weather_data: Dict, assessment: Dict) -> List[str]:
        """Generate specific recommendations for a crop"""
        recommendations = []
        temp = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        wind_speed = weather_data.get('wind', {}).get('speed', 0) * 3.6
        
        # Temperature-based recommendations
        if temp < crop['optimal_temp_range'][0]:
            recommendations.append(f"🌡️ Temperature is below optimal. Consider cold protection measures.")
        elif temp > crop['optimal_temp_range'][1]:
            recommendations.append(f"🌡️ Temperature is above optimal. Provide shade and increase irrigation.")
        
        # Humidity-based recommendations
        if humidity < crop['optimal_humidity_range'][0]:
            recommendations.append(f"💧 Humidity is low. Increase irrigation frequency.")
        elif humidity > crop['optimal_humidity_range'][1]:
            recommendations.append(f"💧 Humidity is high. Monitor for fungal diseases and improve ventilation.")
        
        # Wind-based recommendations
        if crop['wind_tolerance'] == 'low' and wind_speed > 20:
            recommendations.append(f"💨 High winds detected. Install windbreaks or consider staking.")
        elif crop['wind_tolerance'] == 'medium' and wind_speed > 40:
            recommendations.append(f"💨 Very high winds. Secure plants and provide support structures.")
        
        # Water requirement based recommendations
        if crop['water_requirement'] == 'high':
            recommendations.append(f"💧 This crop has high water requirements. Ensure adequate irrigation.")
        elif crop['water_requirement'] == 'low':
            recommendations.append(f"💧 This crop has low water requirements. Avoid overwatering.")
        
        # Growth stage specific recommendations
        sensitive_stages = crop.get('sensitive_stages', {})
        for stage, conditions in sensitive_stages.items():
            stage_temp_range = conditions['temp_range']
            stage_humidity_range = conditions['humidity_range']
            
            if not (stage_temp_range[0] <= temp <= stage_temp_range[1]):
                recommendations.append(f"⚠️ Critical stage: {stage.replace('_', ' ').title()}. Temperature outside optimal range.")
            
            if not (stage_humidity_range[0] <= humidity <= stage_humidity_range[1]):
                recommendations.append(f"⚠️ Critical stage: {stage.replace('_', ' ').title()}. Humidity outside optimal range.")
        
        return recommendations
    
    def _identify_risk_factors(self, crop: Dict, weather_data: Dict) -> List[str]:
        """Identify potential risk factors for a crop based on weather"""
        risk_factors = []
        temp = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        wind_speed = weather_data.get('wind', {}).get('speed', 0) * 3.6
        weather_condition = weather_data.get('weather', [{}])[0].get('description', '').lower()
        
        # Temperature risks
        if temp > 35:
            risk_factors.append("Heat stress risk")
        elif temp < 10:
            risk_factors.append("Cold damage risk")
        
        # Humidity risks
        if humidity > 85:
            risk_factors.append("Fungal disease risk")
        elif humidity < 30:
            risk_factors.append("Drought stress risk")
        
        # Wind risks
        if wind_speed > 50:
            risk_factors.append("Wind damage risk")
        elif wind_speed > 30 and crop['wind_tolerance'] == 'low':
            risk_factors.append("Lodging risk")
        
        # Weather condition risks
        if 'storm' in weather_condition or 'thunder' in weather_condition:
            risk_factors.append("Storm damage risk")
        elif 'rain' in weather_condition and crop['flood_tolerance'] == 'low':
            risk_factors.append("Waterlogging risk")
        
        # Crop-specific risks
        if crop['storm_impact_risk'] == 'high' and 'storm' in weather_condition:
            risk_factors.append("High storm impact risk")
        elif crop['storm_impact_risk'] == 'very_high' and 'storm' in weather_condition:
            risk_factors.append("Very high storm impact risk")
        
        return risk_factors if risk_factors else ["Low risk conditions"]
    
    def _generate_summary(self, recommendations: List[Dict]) -> str:
        """Generate a summary of recommendations"""
        top_crops = [rec for rec in recommendations if rec['suitable']]
        
        if not top_crops:
            return "Current weather conditions are challenging for most crops. Consider protective measures or wait for better conditions."
        
        best_crop = top_crops[0]
        return f"Best suited crop: {best_crop['crop']} (Score: {best_crop['suitability_score']}/100). Current conditions favor {len(top_crops)} crops."
    
    def get_specific_crop_advice(self, crop_name: str, weather_data: Dict) -> Dict:
        """
        Get detailed advice for a specific crop
        
        Args:
            crop_name: Name of the crop
            weather_data: Current weather data
            
        Returns:
            Detailed advice for the specific crop
        """
        crop_info = self.crop_db.get_crop_info(crop_name)
        if not crop_info:
            return {'error': 'Crop not found in database'}
        
        assessment = self.crop_db.assess_weather_suitability(crop_name, weather_data)
        specific_recommendations = self._generate_crop_recommendations(crop_info, weather_data, assessment)
        risk_factors = self._identify_risk_factors(crop_info, weather_data)
        
        return {
            'crop': crop_info['name'],
            'scientific_name': crop_info['scientific_name'],
            'category': crop_info['category'],
            'assessment': assessment,
            'recommendations': specific_recommendations,
            'risk_factors': risk_factors,
            'regional_varieties': crop_info.get('regional_varieties', []),
            'water_requirement': crop_info['water_requirement'],
            'growth_duration': crop_info['growth_duration_days'],
            'action_plan': self._generate_action_plan(crop_info, weather_data, assessment)
        }
    
    def _generate_action_plan(self, crop: Dict, weather_data: Dict, assessment: Dict) -> List[str]:
        """Generate immediate action plan for the crop"""
        action_plan = []
        temp = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        wind_speed = weather_data.get('wind', {}).get('speed', 0) * 3.6
        
        # Priority actions based on current conditions
        if not assessment['suitable']:
            action_plan.append("🚨 URGENT: Current conditions are unsuitable. Take immediate protective measures.")
        
        # Temperature actions
        if temp > crop['optimal_temp_range'][1]:
            action_plan.append("🌡️ Apply mulch to reduce soil temperature")
            action_plan.append("💧 Increase irrigation frequency to cool plants")
            action_plan.append("🌿 Provide shade cloth if possible")
        elif temp < crop['optimal_temp_range'][0]:
            action_plan.append("🌡️ Apply frost protection if needed")
            action_plan.append("🛡️ Use row covers or cold frames")
        
        # Humidity actions
        if humidity < crop['optimal_humidity_range'][0]:
            action_plan.append("💧 Increase irrigation immediately")
            action_plan.append("🌿 Maintain soil moisture with mulch")
        elif humidity > crop['optimal_humidity_range'][1]:
            action_plan.append("🌿 Improve air circulation around plants")
            action_plan.append("🍄 Apply fungicide preventatively if high humidity persists")
        
        # Wind actions
        if wind_speed > 30 and crop['wind_tolerance'] == 'low':
            action_plan.append("💨 Install windbreaks immediately")
            action_plan.append("🌱 Stake or support plants")
            action_plan.append("⚠️ Consider delaying planting if severe winds persist")
        
        # General actions
        action_plan.append("📊 Monitor weather forecast for next 48 hours")
        action_plan.append("👁️ Inspect plants for stress symptoms daily")
        action_plan.append("📝 Keep detailed records of weather impacts")
        
        return action_plan