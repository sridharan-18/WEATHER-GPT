from flask import Flask, render_template, request, jsonify
import requests
import os
from datetime import datetime
import json

app = Flask(__name__)

# Configuration
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY', 'your_openweathermap_api_key')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'your_openai_api_key')

# Weather API base URL
WEATHER_BASE_URL = "http://api.openweathermap.org/data/2.5"

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages with AI integration"""
    data = request.json
    user_message = data.get('message', '')
    
    if not user_message:
        return jsonify({'response': 'Please provide a message.'})
    
    try:
        # Extract location from message if present
        location = extract_location(user_message)
        
        if location:
            # Get weather data for the location
            weather_data = get_weather_data(location)
            if weather_data:
                # Generate AI response with weather context
                ai_response = generate_ai_response(user_message, weather_data)
                return jsonify({'response': ai_response})
            else:
                return jsonify({'response': f"Sorry, I couldn't find weather data for {location}. Please try a different location or check the spelling."})
        else:
            # General AI response without weather data
            ai_response = generate_ai_response(user_message, None)
            return jsonify({'response': ai_response})
            
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'response': 'Sorry, I encountered an error processing your request. Please try again.'})

def extract_location(message):
    """Extract location from user message"""
    # Simple location extraction - looks for common patterns
    message_lower = message.lower()
    
    # Common location keywords
    location_keywords = ['in', 'at', 'for', 'near']
    
    for keyword in location_keywords:
        if keyword in message_lower:
            # Get text after the keyword
            parts = message_lower.split(keyword)
            if len(parts) > 1:
                potential_location = parts[1].strip()
                # Remove common question words
                potential_location = potential_location.replace('what', '').replace('the', '').replace('weather', '').replace('like', '').replace('is', '').replace('?', '').replace('.', '').strip()
                
                if potential_location and len(potential_location) > 2:
                    return potential_location.title()
    
    # Default location if none found
    return None

def get_weather_data(location):
    """Get weather data from OpenWeatherMap API"""
    try:
        # Get current weather
        url = f"{WEATHER_BASE_URL}/weather"
        params = {
            'q': location,
            'appid': WEATHER_API_KEY,
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

def generate_ai_response(user_message, weather_data):
    """Generate AI response using OpenAI or fallback logic"""
    try:
        if OPENAI_API_KEY and OPENAI_API_KEY != 'your_openai_api_key':
            # Use OpenAI API
            return generate_openai_response(user_message, weather_data)
        else:
            # Fallback to rule-based responses
            return generate_rule_based_response(user_message, weather_data)
    except Exception as e:
        print(f"Error generating AI response: {e}")
        return generate_rule_based_response(user_message, weather_data)

def generate_openai_response(user_message, weather_data):
    """Generate response using OpenAI API"""
    try:
        import openai
        
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        
        # Build context
        context = "You are a helpful weather assistant. Provide actionable advice based on weather conditions."
        
        if weather_data:
            temp = weather_data['main']['temp']
            humidity = weather_data['main']['humidity']
            description = weather_data['weather'][0]['description']
            location = weather_data['name']
            
            weather_context = f"""
Current weather in {location}:
- Temperature: {temp}°C
- Humidity: {humidity}%
- Conditions: {description}
"""
            context += weather_context
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": context},
                {"role": "user", "content": user_message}
            ],
            max_tokens=150,
            temperature=0.7
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return generate_rule_based_response(user_message, weather_data)

def generate_rule_based_response(user_message, weather_data):
    """Generate rule-based responses without AI"""
    message_lower = user_message.lower()
    
    if weather_data:
        temp = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        description = weather_data['weather'][0]['description']
        location = weather_data['name']
        
        # Generate actionable advice based on conditions
        advice = []
        
        if temp > 30:
            advice.append("🥵 It's quite hot! Stay hydrated and avoid direct sunlight.")
        elif temp < 15:
            advice.append("🧥 It's chilly - dress warmly!")
        elif temp < 5:
            advice.append("❄️ It's very cold! Wear heavy layers and protect exposed skin.")
        
        if humidity > 80:
            advice.append("💧 High humidity - it might feel muggy. Consider staying indoors.")
        elif humidity < 30:
            advice.append("🌵 Low humidity - stay moisturized and drink plenty of water.")
        
        if 'rain' in description or 'drizzle' in description:
            advice.append("☔ Don't forget an umbrella or raincoat!")
        elif 'clear' in description:
            advice.append("😎 Great weather for outdoor activities!")
        elif 'cloud' in description:
            advice.append("☁️ Partly cloudy - pleasant weather overall.")
        
        if 'storm' in description or 'thunder' in description:
            advice.append("⚡ Stormy conditions - stay indoors and avoid travel if possible.")
        
        response = f"📍 Weather in {location}: {description}, {temp}°C (feels like {weather_data['main']['feels_like']}°C)\n\n"
        response += "💡 Advice:\n" + "\n".join(f"• {tip}" for tip in advice)
        
        return response
    else:
        # General responses without weather data
        if 'hello' in message_lower or 'hi' in message_lower:
            return "Hello! 👋 I'm your weather assistant. Ask me about weather conditions in any location, and I'll provide you with current information and actionable advice!"
        elif 'help' in message_lower:
            return "I can help you with:\n• Current weather conditions for any location\n• Actionable advice based on weather\n• Hazard risk information\n\nJust ask something like 'What's the weather like in Sulur?' or 'Should I carry an umbrella today?'"
        else:
            return "I'd be happy to help with weather information! Please specify a location, for example: 'What's the weather like in [city name]?'"

@app.route('/api/weather/<location>')
def weather(location):
    """Get weather data for a specific location"""
    weather_data = get_weather_data(location)
    if weather_data:
        return jsonify(weather_data)
    else:
        return jsonify({'error': 'Location not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)