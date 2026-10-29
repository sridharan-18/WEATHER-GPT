"""
Weather Assistant Service
Modular service for AI-powered weather conversational assistant with actionable advice
"""

import os
from typing import Dict, Optional, List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WeatherAssistant:
    """Modular weather assistant with GPT integration and actionable advice"""
    
    def __init__(self, openai_api_key: Optional[str] = None, weather_api_key: Optional[str] = None):
        """
        Initialize the weather assistant
        
        Args:
            openai_api_key: OpenAI API key for GPT integration
            weather_api_key: OpenWeatherMap API key for weather data
        """
        self.openai_api_key = openai_api_key or os.getenv('OPENAI_API_KEY', 'your_openai_api_key')
        self.weather_api_key = weather_api_key or os.getenv('WEATHER_API_KEY', 'your_openweathermap_api_key')
        self.weather_base_url = "http://api.openweathermap.org/data/2.5"
        self.use_gpt = self.openai_api_key and self.openai_api_key != 'your_openai_api_key'
        
        # Actionable advice categories
        self.advice_categories = {
            'clothing': {
                'hot': "Wear light, breathable clothing like cotton. Use sunglasses and a hat.",
                'cold': "Layer up with thermal wear, sweaters, and jackets. Don't forget gloves and a scarf.",
                'mild': "Comfortable layers work best. Bring a light jacket for evenings.",
                'rain': "Waterproof jacket or raincoat. Waterproof shoes are recommended."
            },
            'health': {
                'hot': "Stay hydrated! Drink plenty of water. Avoid prolonged sun exposure between 10 AM and 4 PM.",
                'cold': "Keep extremities covered. Warm beverages help. Watch for signs of hypothermia.",
                'mild': "Good conditions for outdoor exercise. Stay active and hydrated.",
                'rain': "Be careful of slippery surfaces. Keep dry to prevent illness."
            },
            'travel': {
                'hot': "Early morning or late evening travel is best. Use AC in vehicles.",
                'cold': "Check vehicle fluids and tire pressure. Keep emergency kit in car.",
                'mild': "Great travel conditions. Perfect for road trips.",
                'rain': "Reduce speed, increase following distance. Check weather updates before leaving."
            },
            'outdoor': {
                'hot': "Avoid strenuous activities during peak heat. Take frequent breaks in shade.",
                'cold': "Warm up before activities. Watch for frostbite on exposed skin.",
                'mild': "Excellent conditions for outdoor sports and activities.",
                'rain': "Indoor activities recommended. If outdoors, use covered areas."
            }
        }
    
    def get_weather_data(self, location: str) -> Optional[Dict]:
        """
        Fetch weather data from OpenWeatherMap API
        
        Args:
            location: City name or location identifier
            
        Returns:
            Weather data dictionary or None if error
        """
        try:
            import requests
            
            url = f"{self.weather_base_url}/weather"
            params = {
                'q': location,
                'appid': self.weather_api_key,
                'units': 'metric'
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Weather API error: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error fetching weather data: {e}")
            return None
    
    def extract_location(self, message: str) -> Optional[str]:
        """
        Extract location from user message using pattern matching
        
        Args:
            message: User's message
            
        Returns:
            Extracted location or None
        """
        message_lower = message.lower()
        
        # Common location keywords
        location_keywords = ['in', 'at', 'for', 'near', 'of', 'from']
        filler_words = ['today', 'tomorrow', 'yesterday', 'now', 'right', 'the', 'what', 'like', 'is', 'weather', 'temperature', 'forecast', 'here', 'there', 'current']
        
        words = message_lower.split()
        
        for index, word in enumerate(words):
            if word in location_keywords:
                # Take up to 2 words after the keyword, stopping at filler words
                location_words = []
                for w in words[index + 1:]:
                    w = w.strip('?.,!:\t')
                    if not w:
                        continue
                    if w.lower() in filler_words:
                        break
                    location_words.append(w)
                    if len(location_words) >= 2:
                        break
                potential_location = ' '.join(location_words)
                if potential_location and len(potential_location) > 2:
                    return potential_location.title()
        
        # If no location found but user asks for weather, return None to use geolocation
        if 'weather' in message_lower or 'temperature' in message_lower or 'forecast' in message_lower:
            return None  # Will trigger geolocation prompt
        
        return None
    
    def categorize_weather(self, weather_data: Dict) -> str:
        """
        Categorize weather conditions (hot, cold, mild, rain)
        
        Args:
            weather_data: Weather data dictionary
            
        Returns:
            Weather category string
        """
        try:
            temp = weather_data['main']['temp']
            description = weather_data['weather'][0]['description'].lower()
            
            if 'rain' in description or 'drizzle' in description or 'storm' in description:
                return 'rain'
            elif temp > 28:
                return 'hot'
            elif temp < 10:
                return 'cold'
            else:
                return 'mild'
        except (KeyError, TypeError):
            return 'mild'
    
    def generate_actionable_advice(self, weather_data: Dict, categories: Optional[List[str]] = None) -> Dict[str, str]:
        """
        Generate actionable advice based on weather conditions
        
        Args:
            weather_data: Weather data dictionary
            categories: List of advice categories to include (default: all)
            
        Returns:
            Dictionary with advice by category
        """
        if categories is None:
            categories = list(self.advice_categories.keys())
        
        weather_category = self.categorize_weather(weather_data)
        advice = {}
        
        for category in categories:
            if category in self.advice_categories:
                advice[category] = self.advice_categories[category].get(weather_category, "No specific advice available.")
        
        return advice
    
    def generate_gpt_response(self, user_message: str, weather_data: Optional[Dict] = None) -> str:
        """
        Generate response using OpenAI GPT with enhanced prompts
        
        Args:
            user_message: User's message
            weather_data: Optional weather data for context
            
        Returns:
            AI-generated response
        """
        try:
            import openai
            
            client = openai.OpenAI(api_key=self.openai_api_key)
            
            # Enhanced system prompt with actionable advice focus
            system_prompt = """You are a helpful weather assistant with expertise in providing actionable advice. 
            Your responses should:
            1. Be concise and practical
            2. Include specific, actionable recommendations
            3. Cover clothing, health, travel, and outdoor activities
            4. Use emojis to make responses engaging
            5. Prioritize safety in adverse conditions
            6. Suggest specific actions (e.g., "carry an umbrella" not just "it might rain")"""
            
            if weather_data:
                temp = weather_data['main']['temp']
                humidity = weather_data['main']['humidity']
                description = weather_data['weather'][0]['description']
                location = weather_data['name']
                feels_like = weather_data['main'].get('feels_like', temp)
                
                # Generate actionable advice
                advice = self.generate_actionable_advice(weather_data)
                
                weather_context = f"""
Current weather in {location}:
- Temperature: {temp}°C (feels like {feels_like}°C)
- Humidity: {humidity}%
- Conditions: {description}

Actionable Advice:
"""
                for category, tip in advice.items():
                    weather_context += f"- {category.title()}: {tip}\n"
                
                system_prompt += "\n\n" + weather_context
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=200,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise
    
    def generate_rule_based_response(self, user_message: str, weather_data: Optional[Dict] = None) -> str:
        """
        Generate rule-based response without AI (fallback)
        
        Args:
            user_message: User's message
            weather_data: Optional weather data for context
            
        Returns:
            Rule-based response
        """
        message_lower = user_message.lower()
        
        if weather_data:
            main = weather_data.get('main', {}) or {}
            temp = main.get('temp')
            humidity = main.get('humidity')
            weather_list = weather_data.get('weather', []) or []
            description = weather_list[0].get('description', 'unknown') if weather_list else 'unknown'
            location = weather_data.get('name', 'Unknown location')
            feels_like = main.get('feels_like', temp)
            
            # Generate actionable advice
            advice_dict = self.generate_actionable_advice(weather_data)
            
            response = f"📍 Weather in {location}: {description}, {temp}°C (feels like {feels_like}°C)\n\n"
            response += "💡 Actionable Advice:\n"
            
            for category, tip in advice_dict.items():
                response += f"\n{category.title()}:\n• {tip}\n"
            
            return response
        else:
            # General responses without weather data
            if 'hello' in message_lower or 'hi' in message_lower:
                return "Hello! 👋 I'm your global weather assistant. Ask me about weather conditions in any location worldwide - cities, towns, or coordinates. I'll provide you with current information and actionable advice!"
            elif 'help' in message_lower:
                return "I can help you with:\n• Current weather conditions for any location worldwide\n• Actionable advice based on weather\n• Hazard risk information\n• Agricultural recommendations for farmers\n\nJust ask something like 'What's the weather like in Tokyo?' or 'Should I carry an umbrella in London?'"
            else:
                return "I'd be happy to help with weather information! Please specify a location (any city worldwide), for example: 'What's the weather like in [city name]?' or 'Weather forecast for [place]'"
    
    def get_response(self, user_message: str, location: Optional[str] = None) -> str:
        """
        Get AI response for user message
        
        Args:
            user_message: User's message
            location: Optional location (extracted from message if not provided)
            
        Returns:
            AI-generated response
        """
        # Extract location if not provided
        if not location:
            location = self.extract_location(user_message)
        
        # Get weather data if location is found
        weather_data = None
        if location:
            weather_data = self.get_weather_data(location)
        
        # Generate response
        try:
            if self.use_gpt:
                return self.generate_gpt_response(user_message, weather_data)
            else:
                return self.generate_rule_based_response(user_message, weather_data)
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return self.generate_rule_based_response(user_message, weather_data)
