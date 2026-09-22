"""
Crop Database for Weather GPT
Contains comprehensive crop information with weather requirements and growth stages
"""

from typing import Dict, List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CropDatabase:
    """Database of crops with their weather requirements and characteristics"""
    
    def __init__(self):
        self.crops = {
            'rice': {
                'name': 'Rice',
                'scientific_name': 'Oryza sativa',
                'category': 'Cereal',
                'growth_duration_days': 120,
                'optimal_temp_range': (20, 35),
                'optimal_humidity_range': (60, 80),
                'water_requirement': 'high',
                'optimal_rainfall_mm': (1500, 2500),
                'sensitive_stages': {
                    'flowering': {'temp_range': (25, 32), 'humidity_range': (70, 85)},
                    'grain_filling': {'temp_range': (22, 30), 'humidity_range': (65, 80)}
                },
                'drought_tolerance': 'low',
                'flood_tolerance': 'high',
                'wind_tolerance': 'medium',
                'storm_impact_risk': 'high',
                'ideal_soil_moisture': (60, 80),
                'harvest_conditions': {'temp_range': (25, 32), 'humidity_range': (50, 70)},
                'regional_varieties': ['BPT 5204', 'CO 51', 'ADT 43', 'ASD 16']
            },
            'wheat': {
                'name': 'Wheat',
                'scientific_name': 'Triticum aestivum',
                'category': 'Cereal',
                'growth_duration_days': 110,
                'optimal_temp_range': (15, 25),
                'optimal_humidity_range': (40, 60),
                'water_requirement': 'medium',
                'optimal_rainfall_mm': (300, 600),
                'sensitive_stages': {
                    'germination': {'temp_range': (12, 25), 'humidity_range': (50, 70)},
                    'heading': {'temp_range': (15, 22), 'humidity_range': (45, 65)}
                },
                'drought_tolerance': 'medium',
                'flood_tolerance': 'low',
                'wind_tolerance': 'medium',
                'storm_impact_risk': 'medium',
                'ideal_soil_moisture': (40, 60),
                'harvest_conditions': {'temp_range': (20, 30), 'humidity_range': (30, 50)},
                'regional_varieties': ['HD 2967', 'Lokwan', 'GW 322', 'PBW 343']
            },
            'maize': {
                'name': 'Maize (Corn)',
                'scientific_name': 'Zea mays',
                'category': 'Cereal',
                'growth_duration_days': 100,
                'optimal_temp_range': (20, 30),
                'optimal_humidity_range': (50, 70),
                'water_requirement': 'medium',
                'optimal_rainfall_mm': (500, 800),
                'sensitive_stages': {
                    'silking': {'temp_range': (22, 28), 'humidity_range': (55, 75)},
                    'pollination': {'temp_range': (21, 30), 'humidity_range': (50, 70)}
                },
                'drought_tolerance': 'medium',
                'flood_tolerance': 'low',
                'wind_tolerance': 'low',
                'storm_impact_risk': 'high',
                'ideal_soil_moisture': (50, 70),
                'harvest_conditions': {'temp_range': (25, 35), 'humidity_range': (40, 60)},
                'regional_varieties': ['Pioneer 30Y87', 'DeKalb 9140', 'NK 6240', 'Hybrid 2070']
            },
            'cotton': {
                'name': 'Cotton',
                'scientific_name': 'Gossypium hirsutum',
                'category': 'Fiber',
                'growth_duration_days': 150,
                'optimal_temp_range': (21, 32),
                'optimal_humidity_range': (50, 70),
                'water_requirement': 'medium',
                'optimal_rainfall_mm': (500, 900),
                'sensitive_stages': {
                    'flowering': {'temp_range': (25, 32), 'humidity_range': (55, 75)},
                    'boll_opening': {'temp_range': (20, 30), 'humidity_range': (40, 60)}
                },
                'drought_tolerance': 'medium',
                'flood_tolerance': 'low',
                'wind_tolerance': 'medium',
                'storm_impact_risk': 'medium',
                'ideal_soil_moisture': (45, 65),
                'harvest_conditions': {'temp_range': (25, 35), 'humidity_range': (30, 50)},
                'regional_varieties': ['RCH 659', 'JK 669', 'DCH 32', 'MCU 5']
            },
            'sugarcane': {
                'name': 'Sugarcane',
                'scientific_name': 'Saccharum officinarum',
                'category': 'Industrial Crop',
                'growth_duration_days': 365,
                'optimal_temp_range': (20, 35),
                'optimal_humidity_range': (60, 80),
                'water_requirement': 'high',
                'optimal_rainfall_mm': (1500, 2500),
                'sensitive_stages': {
                    'germination': {'temp_range': (25, 32), 'humidity_range': (70, 85)},
                    'tillering': {'temp_range': (22, 30), 'humidity_range': (65, 80)}
                },
                'drought_tolerance': 'low',
                'flood_tolerance': 'medium',
                'wind_tolerance': 'low',
                'storm_impact_risk': 'high',
                'ideal_soil_moisture': (60, 80),
                'harvest_conditions': {'temp_range': (20, 30), 'humidity_range': (40, 60)},
                'regional_varieties': ['CO 86032', 'CO 85036', 'CO 91015', 'CO 96014']
            },
            'groundnut': {
                'name': 'Groundnut (Peanut)',
                'scientific_name': 'Arachis hypogaea',
                'category': 'Oilseed',
                'growth_duration_days': 90,
                'optimal_temp_range': (25, 35),
                'optimal_humidity_range': (50, 70),
                'water_requirement': 'low',
                'optimal_rainfall_mm': (400, 600),
                'sensitive_stages': {
                    'flowering': {'temp_range': (25, 32), 'humidity_range': (55, 75)},
                    'pod_filling': {'temp_range': (22, 30), 'humidity_range': (50, 70)}
                },
                'drought_tolerance': 'high',
                'flood_tolerance': 'low',
                'wind_tolerance': 'medium',
                'storm_impact_risk': 'medium',
                'ideal_soil_moisture': (30, 50),
                'harvest_conditions': {'temp_range': (25, 35), 'humidity_range': (30, 50)},
                'regional_varieties': ['TMV 2', 'Girnar 2', 'TG 37A', 'JL 24']
            },
            'turmeric': {
                'name': 'Turmeric',
                'scientific_name': 'Curcuma longa',
                'category': 'Spice',
                'growth_duration_days': 210,
                'optimal_temp_range': (20, 30),
                'optimal_humidity_range': (60, 80),
                'water_requirement': 'medium',
                'optimal_rainfall_mm': (1000, 1500),
                'sensitive_stages': {
                    'germination': {'temp_range': (22, 28), 'humidity_range': (70, 85)},
                    'rhizome_development': {'temp_range': (20, 28), 'humidity_range': (65, 80)}
                },
                'drought_tolerance': 'medium',
                'flood_tolerance': 'low',
                'wind_tolerance': 'high',
                'storm_impact_risk': 'low',
                'ideal_soil_moisture': (50, 70),
                'harvest_conditions': {'temp_range': (25, 32), 'humidity_range': (40, 60)},
                'regional_varieties': ['Suguna', 'Prabha', 'Suvarna', 'Roma']
            },
            'tomato': {
                'name': 'Tomato',
                'scientific_name': 'Solanum lycopersicum',
                'category': 'Vegetable',
                'growth_duration_days': 90,
                'optimal_temp_range': (18, 28),
                'optimal_humidity_range': (50, 70),
                'water_requirement': 'medium',
                'optimal_rainfall_mm': (400, 600),
                'sensitive_stages': {
                    'flowering': {'temp_range': (20, 26), 'humidity_range': (55, 75)},
                    'fruit_set': {'temp_range': (18, 25), 'humidity_range': (50, 70)}
                },
                'drought_tolerance': 'low',
                'flood_tolerance': 'low',
                'wind_tolerance': 'low',
                'storm_impact_risk': 'high',
                'ideal_soil_moisture': (50, 70),
                'harvest_conditions': {'temp_range': (20, 28), 'humidity_range': (40, 60)},
                'regional_varieties': ['Arka Vikas', 'Pusa Ruby', 'Rashmi', 'Sakthi']
            },
            'coconut': {
                'name': 'Coconut',
                'scientific_name': 'Cocos nucifera',
                'category': 'Tree Crop',
                'growth_duration_days': 3650,  # 10 years
                'optimal_temp_range': (20, 35),
                'optimal_humidity_range': (60, 80),
                'water_requirement': 'high',
                'optimal_rainfall_mm': (1500, 2500),
                'sensitive_stages': {
                    'flowering': {'temp_range': (25, 32), 'humidity_range': (70, 85)},
                    'nut_development': {'temp_range': (22, 30), 'humidity_range': (65, 80)}
                },
                'drought_tolerance': 'medium',
                'flood_tolerance': 'medium',
                'wind_tolerance': 'medium',
                'storm_impact_risk': 'high',
                'ideal_soil_moisture': (60, 80),
                'harvest_conditions': {'temp_range': (25, 32), 'humidity_range': (50, 70)},
                'regional_varieties': ['East Coast Tall', 'West Coast Tall', 'Chowghat Orange Dwarf', 'Kerala Tall']
            },
            'banana': {
                'name': 'Banana',
                'scientific_name': 'Musa paradisiaca',
                'category': 'Fruit',
                'growth_duration_days': 365,
                'optimal_temp_range': (20, 30),
                'optimal_humidity_range': (70, 85),
                'water_requirement': 'high',
                'optimal_rainfall_mm': (1500, 2500),
                'sensitive_stages': {
                    'flowering': {'temp_range': (22, 28), 'humidity_range': (75, 90)},
                    'fruit_development': {'temp_range': (20, 28), 'humidity_range': (70, 85)}
                },
                'drought_tolerance': 'low',
                'flood_tolerance': 'medium',
                'wind_tolerance': 'low',
                'storm_impact_risk': 'very_high',
                'ideal_soil_moisture': (65, 85),
                'harvest_conditions': {'temp_range': (25, 32), 'humidity_range': (50, 70)},
                'regional_varieties': ['Grand Naine', 'Rasthali', 'Poovan', 'Nendran']
            }
        }
    
    def get_crop_info(self, crop_name: str) -> Dict:
        """Get information for a specific crop"""
        crop_key = crop_name.lower().replace(' ', '_')
        return self.crops.get(crop_key, None)
    
    def get_all_crops(self) -> List[Dict]:
        """Get information for all crops"""
        return list(self.crops.values())
    
    def get_crops_by_category(self, category: str) -> List[Dict]:
        """Get crops by category"""
        return [crop for crop in self.crops.values() if crop['category'] == category]
    
    def get_crops_by_water_requirement(self, requirement: str) -> List[Dict]:
        """Get crops by water requirement level"""
        return [crop for crop in self.crops.values() if crop['water_requirement'] == requirement]
    
    def get_regional_varieties(self, crop_name: str) -> List[str]:
        """Get regional varieties for a crop"""
        crop_info = self.get_crop_info(crop_name)
        return crop_info.get('regional_varieties', []) if crop_info else []
    
    def get_sensitive_stages(self, crop_name: str) -> Dict:
        """Get sensitive growth stages for a crop"""
        crop_info = self.get_crop_info(crop_name)
        return crop_info.get('sensitive_stages', {}) if crop_info else {}
    
    def assess_weather_suitability(self, crop_name: str, weather_data: Dict) -> Dict:
        """Assess if current weather is suitable for a crop"""
        crop_info = self.get_crop_info(crop_name)
        if not crop_info:
            return {'suitable': False, 'reason': 'Crop not found in database'}
        
        temp = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        wind_speed = weather_data.get('wind', {}).get('speed', 0) * 3.6  # Convert to km/h
        
        optimal_temp_range = crop_info['optimal_temp_range']
        optimal_humidity_range = crop_info['optimal_humidity_range']
        
        temp_suitable = optimal_temp_range[0] <= temp <= optimal_temp_range[1]
        humidity_suitable = optimal_humidity_range[0] <= humidity <= optimal_humidity_range[1]
        
        # Check wind tolerance
        wind_suitable = True
        if crop_info['wind_tolerance'] == 'low' and wind_speed > 30:
            wind_suitable = False
        elif crop_info['wind_tolerance'] == 'medium' and wind_speed > 50:
            wind_suitable = False
        
        overall_suitable = temp_suitable and humidity_suitable and wind_suitable
        
        return {
            'suitable': overall_suitable,
            'temperature': {
                'current': temp,
                'optimal_range': optimal_temp_range,
                'suitable': temp_suitable,
                'deviation': temp - sum(optimal_temp_range) / 2
            },
            'humidity': {
                'current': humidity,
                'optimal_range': optimal_humidity_range,
                'suitable': humidity_suitable,
                'deviation': humidity - sum(optimal_humidity_range) / 2
            },
            'wind': {
                'current_speed': wind_speed,
                'tolerance': crop_info['wind_tolerance'],
                'suitable': wind_suitable
            },
            'overall_assessment': self._get_assessment_message(overall_suitable, temp_suitable, humidity_suitable, wind_suitable)
        }
    
    def _get_assessment_message(self, overall: bool, temp: bool, humidity: bool, wind: bool) -> str:
        """Generate assessment message"""
        if overall:
            return "Current weather conditions are suitable for this crop."
        
        issues = []
        if not temp:
            issues.append("temperature outside optimal range")
        if not humidity:
            issues.append("humidity outside optimal range")
        if not wind:
            issues.append("wind speed too high for this crop")
        
        return f"Caution: {', '.join(issues)}. Consider protective measures."