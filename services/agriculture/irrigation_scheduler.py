"""
Irrigation Scheduler for Weather GPT
Provides smart irrigation scheduling based on weather conditions and crop requirements
"""

from typing import Dict, List
from datetime import datetime, timedelta
import logging
from .crop_database import CropDatabase

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class IrrigationScheduler:
    """Provides irrigation scheduling recommendations based on weather and crop needs"""
    
    def __init__(self):
        self.crop_db = CropDatabase()
    
    def generate_irrigation_schedule(self, weather_data: Dict, crop_name: str, 
                                    current_soil_moisture: int = 50) -> Dict:
        """
        Generate irrigation schedule for a specific crop
        
        Args:
            weather_data: Current weather data
            crop_name: Name of the crop
            current_soil_moisture: Current soil moisture percentage (0-100)
            
        Returns:
            Irrigation schedule with recommendations
        """
        crop_info = self.crop_db.get_crop_info(crop_name)
        if not crop_info:
            return {'error': 'Crop not found in database'}
        
        temp = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        wind_speed = weather_data.get('wind', {}).get('speed', 0) * 3.6
        weather_condition = weather_data.get('weather', [{}])[0].get('description', '').lower()
        
        # Calculate irrigation needs
        irrigation_needs = self._calculate_irrigation_needs(
            crop_info, weather_data, current_soil_moisture
        )
        
        # Generate schedule
        schedule = self._generate_irrigation_schedule(
            crop_info, irrigation_needs, weather_data
        )
        
        # Get water conservation tips
        conservation_tips = self._get_water_conservation_tips(weather_data, crop_info)
        
        return {
            'crop': crop_info['name'],
            'water_requirement': crop_info['water_requirement'],
            'current_conditions': {
                'temperature': temp,
                'humidity': humidity,
                'wind_speed': wind_speed,
                'weather_condition': weather_condition,
                'current_soil_moisture': current_soil_moisture
            },
            'irrigation_needs': irrigation_needs,
            'schedule': schedule,
            'conservation_tips': conservation_tips,
            'next_irrigation': self._calculate_next_irrigation(irrigation_needs, weather_data)
        }
    
    def _calculate_irrigation_needs(self, crop: Dict, weather_data: Dict, 
                                   current_soil_moisture: int) -> Dict:
        """Calculate irrigation needs based on conditions"""
        temp = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        wind_speed = weather_data.get('wind', {}).get('speed', 0) * 3.6
        weather_condition = weather_data.get('weather', [{}])[0].get('description', '').lower()
        
        # Base water requirement
        base_requirement = self._get_base_water_requirement(crop['water_requirement'])
        
        # Temperature adjustment
        temp_factor = self._calculate_temperature_factor(temp)
        
        # Humidity adjustment
        humidity_factor = self._calculate_humidity_factor(humidity)
        
        # Wind adjustment (wind increases evaporation)
        wind_factor = self._calculate_wind_factor(wind_speed)
        
        # Weather condition adjustment
        weather_factor = self._calculate_weather_factor(weather_condition)
        
        # Calculate adjusted requirement
        adjusted_requirement = base_requirement * temp_factor * humidity_factor * wind_factor * weather_factor
        
        # Soil moisture deficit
        ideal_moisture = crop.get('ideal_soil_moisture', (50, 70))
        target_moisture = sum(ideal_moisture) / 2
        moisture_deficit = max(0, target_moisture - current_soil_moisture)
        
        # Urgency level
        urgency = self._determine_irrigation_urgency(
            current_soil_moisture, ideal_moisture, temp, weather_condition
        )
        
        return {
            'base_requirement_mm': base_requirement,
            'adjusted_requirement_mm': round(adjusted_requirement, 2),
            'temperature_factor': round(temp_factor, 2),
            'humidity_factor': round(humidity_factor, 2),
            'wind_factor': round(wind_factor, 2),
            'weather_factor': round(weather_factor, 2),
            'current_soil_moisture': current_soil_moisture,
            'target_soil_moisture': target_moisture,
            'moisture_deficit': round(moisture_deficit, 2),
            'urgency': urgency,
            'recommended_volume_liter_per_sqm': round(adjusted_requirement, 2)  # 1mm = 1 liter per sqm
        }
    
    def _get_base_water_requirement(self, water_requirement: str) -> float:
        """Get base water requirement in mm per day"""
        requirements = {
            'high': 8.0,      # 8mm per day for high water requirement crops
            'medium': 5.0,    # 5mm per day for medium water requirement crops
            'low': 2.5        # 2.5mm per day for low water requirement crops
        }
        return requirements.get(water_requirement, 5.0)
    
    def _calculate_temperature_factor(self, temp: float) -> float:
        """Calculate temperature adjustment factor"""
        if temp > 35:
            return 1.5  # High temperature increases water needs
        elif temp > 30:
            return 1.3
        elif temp > 25:
            return 1.1
        elif temp > 20:
            return 1.0  # Optimal temperature
        elif temp > 15:
            return 0.9
        elif temp > 10:
            return 0.7
        else:
            return 0.5  # Low temperature reduces water needs
    
    def _calculate_humidity_factor(self, humidity: float) -> float:
        """Calculate humidity adjustment factor"""
        if humidity < 30:
            return 1.4  # Low humidity increases evaporation
        elif humidity < 50:
            return 1.2
        elif humidity < 70:
            return 1.0  # Optimal humidity
        elif humidity < 85:
            return 0.8
        else:
            return 0.6  # High humidity reduces evaporation
    
    def _calculate_wind_factor(self, wind_speed: float) -> float:
        """Calculate wind adjustment factor"""
        if wind_speed > 40:
            return 1.3  # High wind increases evaporation
        elif wind_speed > 30:
            return 1.2
        elif wind_speed > 20:
            return 1.1
        elif wind_speed > 10:
            return 1.0  # Normal wind
        else:
            return 0.9  # Low wind reduces evaporation
    
    def _calculate_weather_factor(self, weather_condition: str) -> float:
        """Calculate weather condition adjustment factor"""
        if 'rain' in weather_condition or 'drizzle' in weather_condition:
            return 0.3  # Rain reduces irrigation need
        elif 'cloud' in weather_condition:
            return 0.8  # Cloudy conditions reduce evaporation
        elif 'clear' in weather_condition:
            return 1.2  # Clear sky increases evaporation
        else:
            return 1.0  # Normal conditions
    
    def _determine_irrigation_urgency(self, current_moisture: int, ideal_range: tuple, 
                                     temp: float, weather_condition: str) -> str:
        """Determine irrigation urgency level"""
        if current_moisture < ideal_range[0] - 20:
            return 'CRITICAL'
        elif current_moisture < ideal_range[0] - 10:
            return 'HIGH'
        elif current_moisture < ideal_range[0]:
            return 'MODERATE'
        elif current_moisture > ideal_range[1] + 10:
            return 'NONE - Excess moisture'
        elif 'rain' in weather_condition:
            return 'LOW - Rain expected'
        else:
            return 'LOW'
    
    def _generate_irrigation_schedule(self, crop: Dict, irrigation_needs: Dict, 
                                    weather_data: Dict) -> List[Dict]:
        """Generate irrigation schedule for next 7 days"""
        schedule = []
        urgency = irrigation_needs['urgency']
        daily_requirement = irrigation_needs['adjusted_requirement_mm']
        
        # Generate schedule based on urgency
        if urgency == 'CRITICAL':
            # Irrigate immediately and frequently
            schedule.append({
                'day': 'Today',
                'time': 'Immediate',
                'amount_mm': daily_requirement * 1.5,
                'method': 'Flood irrigation or heavy watering',
                'priority': 'URGENT'
            })
            schedule.append({
                'day': 'Tomorrow',
                'time': 'Morning',
                'amount_mm': daily_requirement,
                'method': 'Regular irrigation',
                'priority': 'HIGH'
            })
            schedule.append({
                'day': 'Day 3',
                'time': 'Morning',
                'amount_mm': daily_requirement * 0.8,
                'method': 'Regular irrigation',
                'priority': 'MODERATE'
            })
        
        elif urgency == 'HIGH':
            # Irrigate today and tomorrow
            schedule.append({
                'day': 'Today',
                'time': 'Evening',
                'amount_mm': daily_requirement * 1.2,
                'method': 'Regular irrigation',
                'priority': 'HIGH'
            })
            schedule.append({
                'day': 'Tomorrow',
                'time': 'Morning',
                'amount_mm': daily_requirement,
                'method': 'Regular irrigation',
                'priority': 'MODERATE'
            })
            schedule.append({
                'day': 'Day 3',
                'time': 'Morning',
                'amount_mm': daily_requirement * 0.8,
                'method': 'Light irrigation',
                'priority': 'LOW'
            })
        
        elif urgency == 'MODERATE':
            # Regular schedule
            schedule.append({
                'day': 'Today',
                'time': 'Evening',
                'amount_mm': daily_requirement,
                'method': 'Regular irrigation',
                'priority': 'MODERATE'
            })
            schedule.append({
                'day': 'Day 2',
                'time': 'Morning',
                'amount_mm': daily_requirement,
                'method': 'Regular irrigation',
                'priority': 'LOW'
            })
            schedule.append({
                'day': 'Day 4',
                'time': 'Morning',
                'amount_mm': daily_requirement,
                'method': 'Regular irrigation',
                'priority': 'LOW'
            })
        
        elif urgency == 'LOW':
            # Maintenance schedule
            schedule.append({
                'day': 'Tomorrow',
                'time': 'Morning',
                'amount_mm': daily_requirement * 0.8,
                'method': 'Light irrigation',
                'priority': 'LOW'
            })
            schedule.append({
                'day': 'Day 3',
                'time': 'Morning',
                'amount_mm': daily_requirement,
                'method': 'Regular irrigation',
                'priority': 'LOW'
            })
            schedule.append({
                'day': 'Day 5',
                'time': 'Morning',
                'amount_mm': daily_requirement,
                'method': 'Regular irrigation',
                'priority': 'LOW'
            })
        
        else:  # NONE - Excess moisture
            schedule.append({
                'day': 'Today',
                'time': 'Monitor',
                'amount_mm': 0,
                'method': 'No irrigation - monitor drainage',
                'priority': 'MONITOR'
            })
            schedule.append({
                'day': 'Day 2',
                'time': 'Morning',
                'amount_mm': daily_requirement * 0.5,
                'method': 'Light irrigation if needed',
                'priority': 'MONITOR'
            })
        
        return schedule
    
    def _calculate_next_irrigation(self, irrigation_needs: Dict, weather_data: Dict) -> Dict:
        """Calculate when next irrigation should occur"""
        urgency = irrigation_needs['urgency']
        
        if urgency == 'CRITICAL':
            return {
                'timing': 'Immediate',
                'reason': 'Soil moisture critically low',
                'recommended': 'Irrigate immediately with full recommended amount'
            }
        elif urgency == 'HIGH':
            return {
                'timing': 'Within 12 hours',
                'reason': 'Soil moisture below optimal level',
                'recommended': 'Irrigate by evening with increased amount'
            }
        elif urgency == 'MODERATE':
            return {
                'timing': 'Within 24 hours',
                'reason': 'Soil moisture approaching lower limit',
                'recommended': 'Irrigate by next morning'
            }
        elif urgency == 'LOW':
            return {
                'timing': 'Within 48 hours',
                'reason': 'Soil moisture within acceptable range',
                'recommended': 'Monitor and irrigate as scheduled'
            }
        else:
            return {
                'timing': 'Delay irrigation',
                'reason': 'Excess soil moisture',
                'recommended': 'Monitor drainage, delay irrigation until moisture improves'
            }
    
    def _get_water_conservation_tips(self, weather_data: Dict, crop: Dict) -> List[str]:
        """Get water conservation tips based on conditions"""
        tips = []
        temp = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        wind_speed = weather_data.get('wind', {}).get('speed', 0) * 3.6
        weather_condition = weather_data.get('weather', [{}])[0].get('description', '').lower()
        
        # General conservation tips
        tips.append("💧 Use drip irrigation for maximum efficiency")
        tips.append("🌅 Irrigate early morning or late evening to reduce evaporation")
        tips.append("🌿 Apply mulch to reduce soil evaporation")
        tips.append("📊 Monitor soil moisture to avoid overwatering")
        
        # Condition-specific tips
        if temp > 30:
            tips.append("🌡️ Increase irrigation frequency but reduce duration to maintain moisture")
            tips.append("🌿 Use shade cloth to reduce evaporation")
        
        if humidity < 40:
            tips.append("💧 Focus irrigation on root zone to minimize evaporation")
            tips.append("🌿 Increase mulch thickness to conserve moisture")
        
        if wind_speed > 20:
            tips.append("💨 Avoid irrigation during windy periods to reduce drift")
            tips.append("🌿 Use windbreaks to reduce evaporation")
        
        if 'rain' in weather_condition:
            tips.append("🌧️ Skip irrigation if significant rain is expected")
            tips.append("🌊 Use rainwater harvesting systems")
        
        # Crop-specific tips
        if crop['water_requirement'] == 'high':
            tips.append("🌾 Consider water-efficient varieties if available")
            tips.append("💧 Implement deficit irrigation strategies if appropriate")
        
        tips.append("📱 Use soil moisture sensors for precision irrigation")
        tips.append("🔄 Implement crop rotation to improve soil water retention")
        
        return tips
    
    def get_multi_crop_irrigation_plan(self, weather_data: Dict, 
                                     crops_with_moisture: List[Dict]) -> Dict:
        """
        Generate irrigation plan for multiple crops
        
        Args:
            weather_data: Current weather data
            crops_with_moisture: List of dicts with crop name and current soil moisture
            
        Returns:
            Multi-crop irrigation plan
        """
        plans = []
        
        for crop_data in crops_with_moisture:
            crop_name = crop_data['crop']
            soil_moisture = crop_data.get('soil_moisture', 50)
            
            plan = self.generate_irrigation_schedule(weather_data, crop_name, soil_moisture)
            plans.append(plan)
        
        # Sort by urgency
        urgency_order = {'CRITICAL': 0, 'HIGH': 1, 'MODERATE': 2, 'LOW': 3, 'NONE': 4}
        plans.sort(key=lambda x: urgency_order.get(x['irrigation_needs']['urgency'], 5))
        
        return {
            'timestamp': datetime.now().isoformat(),
            'weather_summary': {
                'temperature': weather_data['main']['temp'],
                'humidity': weather_data['main']['humidity'],
                'condition': weather_data.get('weather', [{}])[0].get('description', '')
            },
            'irrigation_plans': plans,
            'overall_priority': plans[0]['irrigation_needs']['urgency'] if plans else 'NONE',
            'recommendations': self._generate_multi_crop_recommendations(plans)
        }
    
    def _generate_multi_crop_recommendations(self, plans: List[Dict]) -> List[str]:
        """Generate recommendations for managing multiple crops"""
        recommendations = []
        
        if not plans:
            return ["No crops specified for irrigation planning"]
        
        # Check for critical needs
        critical_crops = [p for p in plans if p['irrigation_needs']['urgency'] == 'CRITICAL']
        if critical_crops:
            crop_names = [c['crop'] for c in critical_crops]
            recommendations.append(f"🚨 CRITICAL: Irrigate {', '.join(crop_names)} immediately")
        
        # Check for water requirements
        high_water_crops = [p for p in plans if p['water_requirement'] == 'high']
        if high_water_crops:
            crop_names = [c['crop'] for c in high_water_crops]
            recommendations.append(f"💧 Prioritize water allocation for {', '.join(crop_names)}")
        
        # Timing recommendations
        recommendations.append("🌅 Schedule irrigation for early morning to minimize evaporation")
        recommendations.append("📊 Monitor soil moisture across all fields regularly")
        recommendations.append("💧 Consider implementing zone-based irrigation for efficiency")
        
        return recommendations