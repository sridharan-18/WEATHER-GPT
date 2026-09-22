"""
Farmer Action Planner for Weather GPT
Generates comprehensive action plans for farmers based on weather conditions
"""

from typing import Dict, List
from datetime import datetime, timedelta
import logging
from .crop_database import CropDatabase
from .crop_advisor import CropAdvisor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FarmerActionPlanner:
    """Generates action plans for farmers based on weather conditions"""
    
    def __init__(self):
        self.crop_db = CropDatabase()
        self.crop_advisor = CropAdvisor()
    
    def generate_comprehensive_action_plan(self, weather_data: Dict, location: str, 
                                          crops: List[str] = None) -> Dict:
        """
        Generate a comprehensive action plan for farmers
        
        Args:
            weather_data: Current weather data
            location: Location name
            crops: List of crops being grown (optional)
            
        Returns:
            Comprehensive action plan with recommendations
        """
        temp = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        wind_speed = weather_data.get('wind', {}).get('speed', 0) * 3.6
        weather_condition = weather_data.get('weather', [{}])[0].get('description', '').lower()
        
        # Initialize action plan
        action_plan = {
            'location': location,
            'timestamp': datetime.now().isoformat(),
            'current_conditions': {
                'temperature': temp,
                'humidity': humidity,
                'wind_speed': wind_speed,
                'weather_condition': weather_condition
            },
            'priority_level': self._determine_priority_level(weather_data),
            'immediate_actions': [],
            'short_term_actions': [],
            'long_term_actions': [],
            'crop_specific_actions': {},
            'resource_requirements': [],
            'safety_considerations': [],
            'monitoring_requirements': []
        }
        
        # Generate immediate actions
        action_plan['immediate_actions'] = self._generate_immediate_actions(weather_data)
        
        # Generate short-term actions (next 24-48 hours)
        action_plan['short_term_actions'] = self._generate_short_term_actions(weather_data)
        
        # Generate long-term actions (next week)
        action_plan['long_term_actions'] = self._generate_long_term_actions(weather_data)
        
        # Generate crop-specific actions if crops are specified
        if crops:
            for crop in crops:
                crop_actions = self._generate_crop_specific_actions(crop, weather_data)
                action_plan['crop_specific_actions'][crop] = crop_actions
        
        # Generate resource requirements
        action_plan['resource_requirements'] = self._generate_resource_requirements(weather_data)
        
        # Generate safety considerations
        action_plan['safety_considerations'] = self._generate_safety_considerations(weather_data)
        
        # Generate monitoring requirements
        action_plan['monitoring_requirements'] = self._generate_monitoring_requirements(weather_data)
        
        return action_plan
    
    def _determine_priority_level(self, weather_data: Dict) -> str:
        """Determine the priority level of actions needed"""
        temp = weather_data['main']['temp']
        wind_speed = weather_data.get('wind', {}).get('speed', 0) * 3.6
        weather_condition = weather_data.get('weather', [{}])[0].get('description', '').lower()
        
        # Critical conditions
        if temp > 40 or temp < 5:
            return 'CRITICAL'
        if wind_speed > 60:
            return 'CRITICAL'
        if 'storm' in weather_condition or 'thunder' in weather_condition:
            return 'CRITICAL'
        
        # High priority conditions
        if temp > 35 or temp < 10:
            return 'HIGH'
        if wind_speed > 40:
            return 'HIGH'
        if 'rain' in weather_condition:
            return 'HIGH'
        
        # Moderate priority
        if temp > 30 or temp < 15:
            return 'MODERATE'
        if wind_speed > 25:
            return 'MODERATE'
        
        return 'LOW'
    
    def _generate_immediate_actions(self, weather_data: Dict) -> List[str]:
        """Generate immediate actions (within hours)"""
        actions = []
        temp = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        wind_speed = weather_data.get('wind', {}).get('speed', 0) * 3.6
        weather_condition = weather_data.get('weather', [{}])[0].get('description', '').lower()
        
        # Weather-specific immediate actions
        if 'storm' in weather_condition or 'thunder' in weather_condition:
            actions.append("🚨 Seek shelter immediately - storm conditions detected")
            actions.append("🚨 Secure all loose equipment and materials")
            actions.append("🚨 Move livestock to protected areas if applicable")
            actions.append("🚨 Prepare emergency contact numbers")
        
        if temp > 35:
            actions.append("🌡️ Increase irrigation frequency to cool plants")
            actions.append("🌡️ Apply shade cloth or temporary shade structures")
            actions.append("🌡️ Monitor for heat stress symptoms")
        
        if temp < 10:
            actions.append("🌡️ Apply frost protection measures")
            actions.append("🌡️ Cover sensitive plants with frost cloth")
            actions.append("🌡️ Run irrigation if frost is expected (water releases heat)")
        
        if wind_speed > 40:
            actions.append("💨 Secure irrigation systems and equipment")
            actions.append("💨 Install windbreaks if time permits")
            actions.append("💨 Delay any spraying operations")
        
        if humidity > 85:
            actions.append("🍄 Monitor for fungal disease development")
            actions.append("🍄 Improve air circulation if possible")
            actions.append("🍄 Prepare fungicide applications if needed")
        
        if humidity < 30:
            actions.append("💧 Increase irrigation immediately")
            actions.append("💧 Apply mulch to conserve soil moisture")
        
        return actions
    
    def _generate_short_term_actions(self, weather_data: Dict) -> List[str]:
        """Generate short-term actions (24-48 hours)"""
        actions = []
        temp = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        wind_speed = weather_data.get('wind', {}).get('speed', 0) * 3.6
        weather_condition = weather_data.get('weather', [{}])[0].get('description', '').lower()
        
        # Weather forecast based actions
        if 'rain' in weather_condition:
            actions.append("🌧️ Plan for potential drainage improvements")
            actions.append("🌧️ Prepare for delayed field operations")
            actions.append("🌧️ Check and repair any drainage systems")
            actions.append("🌧️ Plan alternative indoor activities")
        
        if temp > 30:
            actions.append("🌡️ Schedule irrigation for early morning or evening")
            actions.append("🌡️ Plan for additional shade structures")
            actions.append("🌡️ Monitor water requirements closely")
        
        if wind_speed > 25:
            actions.append("💨 Plan for windbreak installation")
            actions.append("💨 Schedule staking and support for plants")
            actions.append("💨 Avoid spraying during windy periods")
        
        actions.append("📊 Review weather forecast for next 48 hours")
        actions.append("📱 Update emergency contact list")
        actions.append("🛠️ Check and maintain farm equipment")
        actions.append("📋 Update farm records and observations")
        
        return actions
    
    def _generate_long_term_actions(self, weather_data: Dict) -> List[str]:
        """Generate long-term actions (next week)"""
        actions = []
        
        actions.append("🌱 Review and adjust planting schedules based on seasonal patterns")
        actions.append("💧 Assess and improve irrigation infrastructure")
        actions.append("🌳 Plan for windbreak installation if wind is a recurring issue")
        actions.append("🍄 Develop disease management plan for high humidity periods")
        actions.append("📊 Implement weather monitoring system")
        actions.append("🛡️ Invest in protective structures (greenhouses, shade houses)")
        actions.append("📈 Track weather patterns and crop performance")
        actions.append("🌾 Consider crop rotation based on seasonal weather patterns")
        actions.append("💰 Budget for weather-related expenses")
        actions.append("📚 Stay updated on long-term weather forecasts")
        
        return actions
    
    def _generate_crop_specific_actions(self, crop_name: str, weather_data: Dict) -> Dict:
        """Generate crop-specific actions"""
        crop_info = self.crop_db.get_crop_info(crop_name)
        if not crop_info:
            return {'error': 'Crop not found'}
        
        assessment = self.crop_db.assess_weather_suitability(crop_name, weather_data)
        
        actions = {
            'crop': crop_info['name'],
            'suitability': assessment['suitable'],
            'immediate_actions': [],
            'irrigation_actions': [],
            'protection_actions': [],
            'harvest_actions': []
        }
        
        temp = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        wind_speed = weather_data.get('wind', {}).get('speed', 0) * 3.6
        
        # Irrigation actions based on water requirement
        if crop_info['water_requirement'] == 'high':
            if humidity < 60:
                actions['irrigation_actions'].append("Increase irrigation frequency to 2-3 times daily")
                actions['irrigation_actions'].append("Ensure soil moisture remains at 60-80%")
                actions['irrigation_actions'].append("Consider drip irrigation for efficiency")
            else:
                actions['irrigation_actions'].append("Maintain regular irrigation schedule")
                actions['irrigation_actions'].append("Monitor soil moisture levels")
        
        elif crop_info['water_requirement'] == 'medium':
            if humidity < 50:
                actions['irrigation_actions'].append("Increase irrigation to daily")
                actions['irrigation_actions'].append("Monitor for drought stress")
            else:
                actions['irrigation_actions'].append("Maintain 2-3 day irrigation interval")
        
        elif crop_info['water_requirement'] == 'low':
            if humidity < 40:
                actions['irrigation_actions'].append("Light irrigation as needed")
                actions['irrigation_actions'].append("Avoid overwatering")
            else:
                actions['irrigation_actions'].append("Minimal irrigation required")
                actions['irrigation_actions'].append("Ensure good drainage")
        
        # Protection actions based on conditions
        if not assessment['temperature']['suitable']:
            if temp > crop_info['optimal_temp_range'][1]:
                actions['protection_actions'].append("Apply shade cloth during peak hours")
                actions['protection_actions'].append("Increase irrigation for cooling effect")
                actions['protection_actions'].append("Mulch to reduce soil temperature")
            else:
                actions['protection_actions'].append("Apply frost protection if needed")
                actions['protection_actions'].append("Use row covers for sensitive crops")
        
        if not assessment['wind']['suitable']:
            actions['protection_actions'].append("Install windbreaks or supports")
            actions['protection_actions'].append("Stake tall plants")
            actions['protection_actions'].append("Delay planting if severe winds persist")
        
        # Harvest timing recommendations
        harvest_conditions = crop_info.get('harvest_conditions', {})
        harvest_temp_range = harvest_conditions.get('temp_range', (20, 30))
        harvest_humidity_range = harvest_conditions.get('humidity_range', (40, 60))
        
        if harvest_temp_range[0] <= temp <= harvest_temp_range[1] and \
           harvest_humidity_range[0] <= humidity <= harvest_humidity_range[1]:
            actions['harvest_actions'].append("Current conditions are suitable for harvesting")
            actions['harvest_actions'].append("Plan harvest for early morning or late afternoon")
        else:
            actions['harvest_actions'].append("Delay harvest until conditions improve")
            if temp > harvest_temp_range[1]:
                actions['harvest_actions'].append("Too hot for harvest - risk of quality loss")
            elif temp < harvest_temp_range[0]:
                actions['harvest_actions'].append("Too cold for harvest - risk of damage")
            if humidity > harvest_humidity_range[1]:
                actions['harvest_actions'].append("Too humid - risk of post-harvest diseases")
        
        return actions
    
    def _generate_resource_requirements(self, weather_data: Dict) -> List[str]:
        """Generate resource requirements based on weather conditions"""
        resources = []
        temp = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        wind_speed = weather_data.get('wind', {}).get('speed', 0) * 3.6
        weather_condition = weather_data.get('weather', [{}])[0].get('description', '').lower()
        
        if temp > 30:
            resources.append("💧 Additional water supply for increased irrigation")
            resources.append("🌿 Shade cloth or temporary shade structures")
            resources.append("🚛 Water tankers if water supply is limited")
        
        if temp < 15:
            resources.append("🛡️ Frost protection materials (frost cloth, row covers)")
            resources.append("🔥 Heating equipment for sensitive crops")
        
        if wind_speed > 30:
            resources.append("🌳 Windbreak materials (netting, fabric, plants)")
            resources.append("🔨 Stakes and support materials")
            resources.append("🔧 Tools for securing equipment")
        
        if 'rain' in weather_condition:
            resources.append("🚧 Drainage improvement materials")
            resources.append("🌊 Pump and hose for water removal")
            resources.append("🏠 Indoor storage for harvested produce")
        
        if humidity > 80:
            resources.append("🍄 Fungicides and disease management supplies")
            resources.append("🌿 Improved ventilation equipment")
        
        resources.append("📱 Mobile device for weather alerts")
        resources.append("🛠️ Basic farm equipment maintenance supplies")
        resources.append("📋 Record-keeping materials")
        
        return resources
    
    def _generate_safety_considerations(self, weather_data: Dict) -> List[str]:
        """Generate safety considerations for farm workers"""
        safety = []
        temp = weather_data['main']['temp']
        wind_speed = weather_data.get('wind', {}).get('speed', 0) * 3.6
        weather_condition = weather_data.get('weather', [{}])[0].get('description', '').lower()
        
        if temp > 32:
            safety.append("🌡️ Provide workers with frequent water breaks")
            safety.append("🌡️ Schedule work during cooler hours (early morning/evening)")
            safety.append("🌡️ Ensure adequate shade for rest areas")
            safety.append("🌡️ Monitor workers for heat exhaustion symptoms")
        
        if temp < 15:
            safety.append("🧥 Ensure workers have appropriate warm clothing")
            safety.append("🧥 Provide warm beverages during breaks")
            safety.append("🧥 Monitor for hypothermia in extended cold exposure")
        
        if wind_speed > 40:
            safety.append("💨 Avoid working with tall equipment in high winds")
            safety.append("💨 Secure all loose materials and tools")
            safety.append("💨 Use appropriate eye protection")
        
        if 'storm' in weather_condition or 'thunder' in weather_condition:
            safety.append("⚡ Stop all outdoor work immediately")
            safety.append("⚡ Seek shelter in buildings or vehicles")
            safety.append("⚡ Avoid open areas and tall objects")
            safety.append("⚡ Do not use electrical equipment during storms")
        
        if 'rain' in weather_condition:
            safety.append("🌧️ Ensure workers have appropriate rain gear")
            safety.append("🌧️ Use caution on wet surfaces")
            safety.append("🌧️ Avoid electrical work in wet conditions")
        
        safety.append("📱 Keep emergency contact numbers accessible")
        safety.append("🚑 Ensure first aid kit is stocked and accessible")
        safety.append("📞 Have communication plan for emergencies")
        
        return safety
    
    def _generate_monitoring_requirements(self, weather_data: Dict) -> List[str]:
        """Generate monitoring requirements based on weather conditions"""
        monitoring = []
        temp = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        wind_speed = weather_data.get('wind', {}).get('speed', 0) * 3.6
        weather_condition = weather_data.get('weather', [{}])[0].get('description', '').lower()
        
        monitoring.append("🌡️ Monitor soil temperature daily")
        monitoring.append("💧 Monitor soil moisture levels regularly")
        monitoring.append("🌿 Monitor plant stress symptoms twice daily")
        monitoring.append("📊 Track weather conditions hourly during extreme events")
        
        if temp > 30:
            monitoring.append("🌡️ Monitor for heat stress symptoms (wilting, leaf scorch)")
            monitoring.append("💧 Monitor irrigation system effectiveness")
        
        if temp < 15:
            monitoring.append("🌡️ Monitor for frost damage")
            monitoring.append("🛡️ Check frost protection effectiveness")
        
        if wind_speed > 25:
            monitoring.append("💨 Monitor for physical damage to plants")
            monitoring.append("💨 Check windbreak effectiveness")
        
        if 'rain' in weather_condition:
            monitoring.append("🌧️ Monitor field drainage and water accumulation")
            monitoring.append("🌧️ Check for signs of waterlogging")
        
        if humidity > 80:
            monitoring.append("🍄 Monitor for fungal disease symptoms")
            monitoring.append("🍄 Check disease pressure in susceptible crops")
        
        monitoring.append("📱 Stay updated with weather forecasts")
        monitoring.append("📋 Document weather impacts and plant responses")
        monitoring.append("🔍 Regular field inspections for pest and disease pressure")
        
        return monitoring