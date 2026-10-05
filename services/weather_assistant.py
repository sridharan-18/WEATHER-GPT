"""
Weather Assistant Service - Modular AI-powered conversational assistant
Provides intelligent weather queries with actionable advice
"""

import os
from typing import Optional, Dict, Any
import requests


class WeatherAssistant:
    """AI-powered weather assistant with GPT integration and rule-based fallback"""
    
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
    
    def extract_location(self, message: str) -> Optional[str]:
        """
        Extract location from user message using pattern matching
        
        Args:
            message: User's message
            
        Returns:
            Extracted location or None
        """
        message_lower = message.lower()
        location_keywords = ['in', 'at', 'for', 'near']
        
        for keyword in location_keywords:
            if keyword in message_lower:
                parts = message_lower.split(keyword)
                if len(parts) > 1:
                    potential_location = parts[1].strip()
                    # Remove common question words
                    potential_location = potential_location.replace('what', '').replace('the', '') \
                        .replace('weather', '').replace('like', '').replace('is', '') \
                        .replace('?', '').replace('.', '').strip()
                    
                    if potential_location and len(potential_location) > 2:
                        return potential_location.title()
        
        return None
    
    def get_weather_data(self, location: str) -> Optional[Dict[str, Any]]:
        """
        Fetch weather data from OpenWeatherMap API
        
        Args:
            location: Location name
            
        Returns:
            Weather data dictionary or None
        """
        try:
            url = f"{self.weather_base_url}/weather"
            params = {
                'q': location,
                'appid': self.weather_api_key,
                'units': 'metric'
            }
            
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Weather API error: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"Error fetching weather data: {e}")
            return None
    
    def generate_actionable_advice(self, weather_data: Dict[str, Any]) -> list:
        """
        Generate actionable advice based on weather conditions
        
        Args:
            weather_data: Weather data dictionary
            
        Returns:
            List of actionable advice strings
        """
        advice = []
        temp = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        description = weather_data['weather'][0]['description'].lower()
        wind_speed = weather_data.get('wind', {}).get('speed', 0)
        visibility = weather_data.get('visibility', 10000) / 1000  # Convert to km
        
        # Temperature-based advice
        if temp > 35:
            advice.append("🥵 Extreme heat! Stay hydrated, avoid direct sunlight, and limit outdoor activities.")
        elif temp > 30:
            advice.append("🥵 It's quite hot! Stay hydrated and avoid direct sunlight.")
        elif temp < 5:
            advice.append("❄️ It's very cold! Wear heavy layers, protect exposed skin, and limit time outdoors.")
        elif temp < 15:
            advice.append("🧥 It's chilly - dress warmly in layers!")
        elif temp > 20 and temp < 28:
            advice.append("😊 Pleasant temperature - great for outdoor activities!")
        
        # Humidity-based advice
        if humidity > 85:
            advice.append("💧 Very high humidity - it feels muggy. Stay indoors if possible.")
        elif humidity > 70:
            advice.append("💧 High humidity - might feel uncomfortable. Consider air conditioning.")
        elif humidity < 20:
            advice.append("🌵 Very low humidity - use moisturizer and drink plenty of water.")
        elif humidity < 30:
            advice.append("🌵 Low humidity - stay moisturized and drink plenty of water.")
        
        # Precipitation-based advice
        if 'rain' in description or 'drizzle' in description:
            advice.append("☔ Don't forget an umbrella or raincoat!")
            advice.append("🚗 Drive carefully as roads may be slippery.")
        elif 'storm' in description or 'thunder' in description:
            advice.append("⚡ Stormy conditions - stay indoors and avoid travel if possible.")
            advice.append("🏠 Stay away from windows and unplug electronics.")
        elif 'snow' in description:
            advice.append("❄️ Snow expected - wear warm, waterproof clothing.")
            advice.append("🚗 Drive slowly and keep emergency supplies in your car.")
        
        # Wind-based advice
        if wind_speed > 20:
            advice.append("💨 Strong winds! Secure loose objects and be cautious while driving.")
        elif wind_speed > 10:
            advice.append("🌬️ Breezy conditions - hold onto hats and light objects.")
        
        # Visibility-based advice
        if visibility < 1:
            advice.append("🌫️ Very poor visibility - avoid driving if possible.")
        elif visibility < 5:
            advice.append("🌫️ Reduced visibility - use fog lights and drive slowly.")
        
        # Clear weather advice
        if 'clear' in description:
            advice.append("😎 Clear skies - perfect weather for outdoor activities!")
            advice.append("🧴 Don't forget sunscreen if you're going outside.")
        elif 'cloud' in description:
            advice.append("☁️ Partly cloudy - pleasant weather overall.")
        
        # UV index advice (if available)
        if 'uvi' in weather_data:
            uvi = weather_data['uvi']
            if uvi > 8:
                advice.append("☀️ Very high UV index - use SPF 30+ sunscreen and avoid peak sun hours.")
            elif uvi > 6:
                advice.append("☀️ High UV index - use sunscreen and seek shade during peak hours.")
        
        return advice
    
    def generate_gpt_response(self, user_message: str, weather_data: Optional[Dict[str, Any]]) -> str:
        """
        Generate response using OpenAI GPT API
        
        Args:
            user_message: User's message
            weather_data: Optional weather data for context
            
        Returns:
            AI-generated response
        """
        try:
            import openai
            
            client = openai.OpenAI(api_key=self.openai_api_key)
            
            # Build comprehensive system prompt
            system_prompt = """You are a helpful weather assistant. Your role is to:
1. Provide accurate weather information
2. Give actionable, practical advice based on conditions
3. Be concise but informative
4. Use appropriate emojis to make responses engaging
5. Prioritize safety in extreme weather conditions

Always include specific, actionable recommendations like:
- "Carry an umbrella" for rain
- "Wear sunscreen" for sunny weather
- "Stay hydrated" for hot weather
- "Dress in layers" for cold weather
- "Avoid travel" for storms"""
            
            if weather_data:
                temp = weather_data['main']['temp']
                humidity = weather_data['main']['humidity']
                description = weather_data['weather'][0]['description']
                location = weather_data['name']
                feels_like = weather_data['main']['feels_like']
                wind_speed = weather_data.get('wind', {}).get('speed', 0)
                
                weather_context = f"""
Current weather in {location}:
- Temperature: {temp}°C (feels like {feels_like}°C)
- Humidity: {humidity}%
- Conditions: {description}
- Wind Speed: {wind_speed} m/s
"""
                system_prompt += weather_context
            
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
            print(f"OpenAI API error: {e}")
            # Fallback to rule-based response
            return self.generate_rule_based_response(user_message, weather_data)
    
    def generate_rule_based_response(self, user_message: str, weather_data: Optional[Dict[str, Any]]) -> str:
        """
        Generate response using rule-based logic (fallback when GPT unavailable)
        
        Args:
            user_message: User's message
            weather_data: Optional weather data for context
            
        Returns:
            Rule-based response
        """
        message_lower = user_message.lower()
        
        if weather_data:
            temp = weather_data['main']['temp']
            humidity = weather_data['main']['humidity']
            description = weather_data['weather'][0]['description']
            location = weather_data['name']
            feels_like = weather_data['main']['feels_like']
            
            # Generate actionable advice
            advice = self.generate_actionable_advice(weather_data)
            
            response = f"📍 Weather in {location}: {description}, {temp}°C (feels like {feels_like}°C)\n\n"
            response += "💡 Actionable Advice:\n" + "\n".join(f"• {tip}" for tip in advice)
            
            return response
        else:
            # General responses without weather data
            if 'hello' in message_lower or 'hi' in message_lower:
                return "Hello! 👋 I'm your AI weather assistant. Ask me about weather conditions in any location, and I'll provide you with current information and actionable advice!"
            elif 'help' in message_lower:
                return """I can help you with:
• Current weather conditions for any location
• Actionable advice based on weather (e.g., carry umbrella, wear sunscreen)
• Hazard risk information
• Travel recommendations based on weather

Try asking:
• "What's the weather like in Sulur?"
• "Should I carry an umbrella today?"
• "Is it safe to travel in this weather?"
• "What should I wear today?\""""
            else:
                return "I'd be happy to help with weather information! Please specify a location, for example: 'What's the weather like in [city name]?'"
    
    def process_query(self, user_message: str) -> Dict[str, Any]:
        """
        Process a user query and generate a response
        
        Args:
            user_message: User's message
            
        Returns:
            Dictionary with response and metadata
        """
        try:
            # Extract location from message
            location = self.extract_location(user_message)
            
            if location:
                # Get weather data for the location
                weather_data = self.get_weather_data(location)
                
                if weather_data:
                    # Generate AI response with weather context
                    if self.use_gpt:
                        response = self.generate_gpt_response(user_message, weather_data)
                    else:
                        response = self.generate_rule_based_response(user_message, weather_data)
                    
                    return {
                        'response': response,
                        'location': location,
                        'weather_data': weather_data,
                        'used_gpt': self.use_gpt,
                        'success': True
                    }
                else:
                    return {
                        'response': f"Sorry, I couldn't find weather data for {location}. Please try a different location or check the spelling.",
                        'location': location,
                        'success': False
                    }
            else:
                # General AI response without weather data
                if self.use_gpt:
                    response = self.generate_gpt_response(user_message, None)
                else:
                    response = self.generate_rule_based_response(user_message, None)
                
                return {
                    'response': response,
                    'location': None,
                    'used_gpt': self.use_gpt,
                    'success': True
                }
                
        except Exception as e:
            print(f"Error processing query: {e}")
            return {
                'response': 'Sorry, I encountered an error processing your request. Please try again.',
                'success': False
            }
