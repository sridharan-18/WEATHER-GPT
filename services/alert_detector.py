"""
Alert Detector for Weather GPT
Detects severe weather conditions and calculates safety scores
"""

import logging
from typing import Dict, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AlertDetector:
    """Detects severe weather conditions from weather data"""
    
    def __init__(self):
        # Thresholds for different weather conditions
        self.thresholds = {
            'extreme_heat': 40,  # Celsius
            'extreme_cold': 0,   # Celsius
            'high_wind': 50,     # km/h
            'heavy_rain': 50,    # mm/h
            'low_visibility': 1000,  # meters
            'extreme_humidity_high': 90,  # percentage
            'extreme_humidity_low': 10,   # percentage
        }
    
    def detect_severe_weather(self, weather_data: Dict) -> List[Dict]:
        """
        Detect severe weather conditions from weather data
        
        Args:
            weather_data: Weather data from API
            
        Returns:
            List of detected alerts with severity levels
        """
        alerts = []
        
        try:
            main = weather_data.get('main', {})
            weather = weather_data.get('weather', [{}])[0]
            wind = weather_data.get('wind', {})
            visibility = weather_data.get('visibility', 10000)
            
            temp = main.get('temp', 20)
            feels_like = main.get('feels_like', 20)
            humidity = main.get('humidity', 50)
            wind_speed = wind.get('speed', 0) * 3.6  # Convert m/s to km/h
            weather_condition = weather.get('description', '').lower()
            weather_id = weather.get('id', 0)
            
            # Temperature extremes
            if temp >= self.thresholds['extreme_heat']:
                alerts.append({
                    'type': 'Extreme Heat',
                    'severity': 'critical',
                    'message': f'Temperature is {temp}°C. Dangerous heat conditions.',
                    'value': temp,
                    'threshold': self.thresholds['extreme_heat']
                })
            elif temp >= 35:
                alerts.append({
                    'type': 'High Temperature',
                    'severity': 'warning',
                    'message': f'Temperature is {temp}°C. Stay hydrated.',
                    'value': temp,
                    'threshold': 35
                })
            
            if temp <= self.thresholds['extreme_cold']:
                alerts.append({
                    'type': 'Extreme Cold',
                    'severity': 'critical',
                    'message': f'Temperature is {temp}°C. Dangerous cold conditions.',
                    'value': temp,
                    'threshold': self.thresholds['extreme_cold']
                })
            elif temp <= 5:
                alerts.append({
                    'type': 'Low Temperature',
                    'severity': 'warning',
                    'message': f'Temperature is {temp}°C. Dress warmly.',
                    'value': temp,
                    'threshold': 5
                })
            
            # Wind conditions
            if wind_speed >= self.thresholds['high_wind']:
                alerts.append({
                    'type': 'High Wind',
                    'severity': 'critical',
                    'message': f'Wind speed is {wind_speed:.1f} km/h. Dangerous wind conditions.',
                    'value': wind_speed,
                    'threshold': self.thresholds['high_wind']
                })
            elif wind_speed >= 30:
                alerts.append({
                    'type': 'Moderate Wind',
                    'severity': 'advisory',
                    'message': f'Wind speed is {wind_speed:.1f} km/h. Secure loose objects.',
                    'value': wind_speed,
                    'threshold': 30
                })
            
            # Precipitation
            if 'rain' in weather_condition or 'drizzle' in weather_condition:
                # Check for storm conditions
                if 'storm' in weather_condition or 'thunder' in weather_condition:
                    alerts.append({
                        'type': 'Thunderstorm',
                        'severity': 'critical',
                        'message': 'Thunderstorm detected. Seek shelter immediately.',
                        'value': weather_id,
                        'threshold': 200
                    })
                else:
                    alerts.append({
                        'type': 'Rain',
                        'severity': 'advisory',
                        'message': 'Rain expected. Carry an umbrella.',
                        'value': weather_id,
                        'threshold': 500
                    })
            
            # Extreme weather codes (OpenWeatherMap specific)
            if weather_id in [200, 201, 202]:  # Thunderstorm
                alerts.append({
                    'type': 'Thunderstorm',
                    'severity': 'critical',
                    'message': 'Severe thunderstorm with lightning.',
                    'value': weather_id,
                    'threshold': 200
                })
            elif weather_id in [211, 212, 221]:  # Heavy thunderstorm
                alerts.append({
                    'type': 'Severe Thunderstorm',
                    'severity': 'critical',
                    'message': 'Heavy thunderstorm. Take immediate shelter.',
                    'value': weather_id,
                    'threshold': 211
                })
            elif weather_id in [230, 231, 232]:  # Thunderstorm with heavy rain
                alerts.append({
                    'type': 'Thunderstorm with Heavy Rain',
                    'severity': 'critical',
                    'message': 'Thunderstorm with heavy rain. Avoid travel.',
                    'value': weather_id,
                    'threshold': 230
                })
            elif weather_id in [502, 503, 504]:  # Heavy rain
                alerts.append({
                    'type': 'Heavy Rain',
                    'severity': 'warning',
                    'message': 'Heavy rainfall. Possible flooding.',
                    'value': weather_id,
                    'threshold': 502
                })
            elif weather_id in [511, 520, 521, 522]:  # Freezing rain/showers
                alerts.append({
                    'type': 'Freezing Rain',
                    'severity': 'critical',
                    'message': 'Freezing rain. Extremely dangerous conditions.',
                    'value': weather_id,
                    'threshold': 511
                })
            elif weather_id in [600, 601, 602]:  # Snow
                alerts.append({
                    'type': 'Snow',
                    'severity': 'warning',
                    'message': 'Snow conditions. Drive carefully.',
                    'value': weather_id,
                    'threshold': 600
                })
            elif weather_id in [611, 612, 613]:  # Sleet
                alerts.append({
                    'type': 'Sleet',
                    'severity': 'warning',
                    'message': 'Sleet conditions. Slippery surfaces.',
                    'value': weather_id,
                    'threshold': 611
                })
            elif weather_id in [781]:  # Tornado
                alerts.append({
                    'type': 'Tornado',
                    'severity': 'critical',
                    'message': 'TORNADO WARNING! Seek shelter immediately!',
                    'value': weather_id,
                    'threshold': 781
                })
            elif weather_id in [762]:  # Volcanic ash
                alerts.append({
                    'type': 'Volcanic Ash',
                    'severity': 'critical',
                    'message': 'Volcanic ash. Avoid outdoor activities.',
                    'value': weather_id,
                    'threshold': 762
                })
            
            # Visibility
            if visibility <= self.thresholds['low_visibility']:
                alerts.append({
                    'type': 'Low Visibility',
                    'severity': 'warning',
                    'message': f'Visibility is {visibility}m. Drive carefully.',
                    'value': visibility,
                    'threshold': self.thresholds['low_visibility']
                })
            
            # Humidity extremes
            if humidity >= self.thresholds['extreme_humidity_high']:
                alerts.append({
                    'type': 'Extreme Humidity',
                    'severity': 'advisory',
                    'message': f'Humidity is {humidity}%. Very uncomfortable conditions.',
                    'value': humidity,
                    'threshold': self.thresholds['extreme_humidity_high']
                })
            elif humidity <= self.thresholds['extreme_humidity_low']:
                alerts.append({
                    'type': 'Low Humidity',
                    'severity': 'advisory',
                    'message': f'Humidity is {humidity}%. Stay hydrated.',
                    'value': humidity,
                    'threshold': self.thresholds['extreme_humidity_low']
                })
            
            # Feels like temperature extremes
            if feels_like >= 45:
                alerts.append({
                    'type': 'Dangerous Heat Index',
                    'severity': 'critical',
                    'message': f'Feels like {feels_like}°C. Heat stroke risk.',
                    'value': feels_like,
                    'threshold': 45
                })
            elif feels_like <= -10:
                alerts.append({
                    'type': 'Dangerous Wind Chill',
                    'severity': 'critical',
                    'message': f'Feels like {feels_like}°C. Frostbite risk.',
                    'value': feels_like,
                    'threshold': -10
                })
            
            logger.info(f"Detected {len(alerts)} alerts for current conditions")
            return alerts
            
        except Exception as e:
            logger.error(f"Error detecting severe weather: {e}")
            return []
    
    def calculate_safety_score(self, weather_data: Dict) -> int:
        """
        Calculate a safety score (0-100) based on weather conditions
        
        Args:
            weather_data: Weather data from API
            
        Returns:
            Safety score from 0 (dangerous) to 100 (safe)
        """
        try:
            alerts = self.detect_severe_weather(weather_data)
            
            if not alerts:
                return 100  # Perfect conditions
            
            # Start with 100 and deduct points based on alert severity
            score = 100
            
            for alert in alerts:
                severity = alert.get('severity', 'advisory')
                
                if severity == 'critical':
                    score -= 40
                elif severity == 'warning':
                    score -= 20
                elif severity == 'advisory':
                    score -= 10
            
            # Ensure score doesn't go below 0
            score = max(0, score)
            
            logger.info(f"Calculated safety score: {score}")
            return score
            
        except Exception as e:
            logger.error(f"Error calculating safety score: {e}")
            return 50  # Default to middle score on error
    
    def get_risk_level(self, safety_score: int) -> str:
        """
        Get risk level description based on safety score
        
        Args:
            safety_score: Safety score (0-100)
            
        Returns:
            Risk level description
        """
        if safety_score >= 80:
            return "Low Risk"
        elif safety_score >= 60:
            return "Moderate Risk"
        elif safety_score >= 40:
            return "High Risk"
        else:
            return "Very High Risk"