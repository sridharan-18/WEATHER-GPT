from flask import Flask, render_template, request, jsonify
import requests
import os
from datetime import datetime
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configuration
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY', 'your_openweathermap_api_key')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'your_openai_api_key')

# Weather API base URL
WEATHER_BASE_URL = "http://api.openweathermap.org/data/2.5"

# Initialize notification services (optional - only if configured)
try:
    from services import NotificationService, SubscriptionManager, AlertDetector
    notification_service = NotificationService()
    subscription_manager = SubscriptionManager()
    alert_detector = AlertDetector()
    SERVICES_AVAILABLE = True
except ImportError:
    SERVICES_AVAILABLE = False
    print("Notification services not available. Install required dependencies for full functionality.")

# Initialize agricultural services (optional - only if configured)
try:
    from services import CropDatabase, CropAdvisor, FarmerActionPlanner, IrrigationScheduler, HarvestAdvisor, StormImpactAnalyzer
    crop_database = CropDatabase()
    crop_advisor = CropAdvisor()
    farmer_action_planner = FarmerActionPlanner()
    irrigation_scheduler = IrrigationScheduler()
    harvest_advisor = HarvestAdvisor()
    storm_impact_analyzer = StormImpactAnalyzer()
    AGRICULTURE_AVAILABLE = True
except ImportError:
    AGRICULTURE_AVAILABLE = False
    print("Agricultural services not available. Install required dependencies for agricultural features.")

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

# Notification API endpoints
@app.route('/api/subscribe', methods=['POST'])
def subscribe():
    """Subscribe to weather notifications"""
    if not SERVICES_AVAILABLE:
        return jsonify({'error': 'Notification services not available'}), 503
    
    data = request.json
    email = data.get('email')
    name = data.get('name', '')
    phone = data.get('phone', '')
    locations = data.get('locations', ['Sulur'])
    
    if not email:
        return jsonify({'error': 'Email is required'}), 400
    
    success = subscription_manager.add_subscriber(email, name, phone, locations)
    if success:
        return jsonify({'message': 'Successfully subscribed to weather notifications'})
    else:
        return jsonify({'error': 'Failed to subscribe. Email may already exist.'}), 400

@app.route('/api/unsubscribe', methods=['POST'])
def unsubscribe():
    """Unsubscribe from weather notifications"""
    if not SERVICES_AVAILABLE:
        return jsonify({'error': 'Notification services not available'}), 503
    
    data = request.json
    email = data.get('email')
    
    if not email:
        return jsonify({'error': 'Email is required'}), 400
    
    success = subscription_manager.remove_subscriber(email)
    if success:
        return jsonify({'message': 'Successfully unsubscribed'})
    else:
        return jsonify({'error': 'Failed to unsubscribe. Email not found.'}), 404

@app.route('/api/subscriber/<email>')
def get_subscriber(email):
    """Get subscriber information"""
    if not SERVICES_AVAILABLE:
        return jsonify({'error': 'Notification services not available'}), 503
    
    subscriber = subscription_manager.get_subscriber(email)
    if subscriber:
        return jsonify(subscriber)
    else:
        return jsonify({'error': 'Subscriber not found'}), 404

@app.route('/api/test-notification', methods=['POST'])
def test_notification():
    """Send a test notification"""
    if not SERVICES_AVAILABLE:
        return jsonify({'error': 'Notification services not available'}), 503
    
    data = request.json
    email = data.get('email')
    phone = data.get('phone')
    
    if not email:
        return jsonify({'error': 'Email is required'}), 400
    
    success = notification_service.send_test_notification(email, phone)
    if success:
        return jsonify({'message': 'Test notification sent successfully'})
    else:
        return jsonify({'error': 'Failed to send test notification'}), 500

@app.route('/api/safety-score/<location>')
def safety_score(location):
    """Get safety score for a location"""
    if not SERVICES_AVAILABLE:
        return jsonify({'error': 'Notification services not available'}), 503
    
    weather_data = get_weather_data(location)
    if weather_data:
        score = alert_detector.calculate_safety_score(weather_data)
        risk_level = alert_detector.get_risk_level(score)
        return jsonify({
            'location': location,
            'safety_score': score,
            'risk_level': risk_level,
            'weather': weather_data
        })
    else:
        return jsonify({'error': 'Location not found'}), 404

# Agricultural API endpoints
@app.route('/api/agriculture/crops')
def get_crops():
    """Get all available crops"""
    if not AGRICULTURE_AVAILABLE:
        return jsonify({'error': 'Agricultural services not available'}), 503
    
    crops = crop_database.get_all_crops()
    return jsonify({'crops': crops})

@app.route('/api/agriculture/crop/<crop_name>')
def get_crop_info(crop_name):
    """Get information for a specific crop"""
    if not AGRICULTURE_AVAILABLE:
        return jsonify({'error': 'Agricultural services not available'}), 503
    
    crop_info = crop_database.get_crop_info(crop_name)
    if crop_info:
        return jsonify(crop_info)
    else:
        return jsonify({'error': 'Crop not found'}), 404

@app.route('/api/agriculture/recommendations/<location>')
def get_crop_recommendations(location):
    """Get crop recommendations based on weather conditions"""
    if not AGRICULTURE_AVAILABLE:
        return jsonify({'error': 'Agricultural services not available'}), 503
    
    weather_data = get_weather_data(location)
    if weather_data:
        recommendations = crop_advisor.get_crop_recommendations(weather_data, location)
        return jsonify(recommendations)
    else:
        return jsonify({'error': 'Location not found'}), 404

@app.route('/api/agriculture/crop-advice', methods=['POST'])
def get_specific_crop_advice():
    """Get detailed advice for a specific crop"""
    if not AGRICULTURE_AVAILABLE:
        return jsonify({'error': 'Agricultural services not available'}), 503
    
    data = request.json
    crop_name = data.get('crop')
    location = data.get('location', 'Sulur')
    
    if not crop_name:
        return jsonify({'error': 'Crop name is required'}), 400
    
    weather_data = get_weather_data(location)
    if weather_data:
        advice = crop_advisor.get_specific_crop_advice(crop_name, weather_data)
        return jsonify(advice)
    else:
        return jsonify({'error': 'Location not found'}), 404

@app.route('/api/agriculture/action-plan', methods=['POST'])
def get_farmer_action_plan():
    """Get comprehensive farmer action plan"""
    if not AGRICULTURE_AVAILABLE:
        return jsonify({'error': 'Agricultural services not available'}), 503
    
    data = request.json
    location = data.get('location', 'Sulur')
    crops = data.get('crops', [])
    
    weather_data = get_weather_data(location)
    if weather_data:
        action_plan = farmer_action_planner.generate_comprehensive_action_plan(
            weather_data, location, crops
        )
        return jsonify(action_plan)
    else:
        return jsonify({'error': 'Location not found'}), 404

@app.route('/api/agriculture/irrigation', methods=['POST'])
def get_irrigation_schedule():
    """Get irrigation schedule for a crop"""
    if not AGRICULTURE_AVAILABLE:
        return jsonify({'error': 'Agricultural services not available'}), 503
    
    data = request.json
    crop_name = data.get('crop')
    location = data.get('location', 'Sulur')
    soil_moisture = data.get('soil_moisture', 50)
    
    if not crop_name:
        return jsonify({'error': 'Crop name is required'}), 400
    
    weather_data = get_weather_data(location)
    if weather_data:
        schedule = irrigation_scheduler.generate_irrigation_schedule(
            weather_data, crop_name, soil_moisture
        )
        return jsonify(schedule)
    else:
        return jsonify({'error': 'Location not found'}), 404

@app.route('/api/agriculture/harvest', methods=['POST'])
def get_harvest_recommendations():
    """Get harvest recommendations for a crop"""
    if not AGRICULTURE_AVAILABLE:
        return jsonify({'error': 'Agricultural services not available'}), 503
    
    data = request.json
    crop_name = data.get('crop')
    location = data.get('location', 'Sulur')
    growth_stage = data.get('growth_stage', 'mature')
    
    if not crop_name:
        return jsonify({'error': 'Crop name is required'}), 400
    
    weather_data = get_weather_data(location)
    if weather_data:
        harvest_rec = harvest_advisor.get_harvest_recommendations(
            weather_data, crop_name, growth_stage
        )
        return jsonify(harvest_rec)
    else:
        return jsonify({'error': 'Location not found'}), 404

@app.route('/api/agriculture/storm-impact', methods=['POST'])
def get_storm_impact_analysis():
    """Get storm impact analysis for a crop"""
    if not AGRICULTURE_AVAILABLE:
        return jsonify({'error': 'Agricultural services not available'}), 503
    
    data = request.json
    crop_name = data.get('crop')
    location = data.get('location', 'Sulur')
    growth_stage = data.get('growth_stage', 'mature')
    
    if not crop_name:
        return jsonify({'error': 'Crop name is required'}), 400
    
    weather_data = get_weather_data(location)
    if weather_data:
        storm_analysis = storm_impact_analyzer.analyze_storm_impact(
            weather_data, crop_name, growth_stage
        )
        return jsonify(storm_analysis)
    else:
        return jsonify({'error': 'Location not found'}), 404

if __name__ == '__main__':
    # Start scheduler if enabled
    if os.getenv('SCHEDULER_ENABLED', 'false').lower() == 'true' and SERVICES_AVAILABLE:
        try:
            from services import start_scheduler
            start_scheduler()
            print("Weather notification scheduler started")
        except Exception as e:
            print(f"Failed to start scheduler: {e}")
    
    app.run(debug=True, host='0.0.0.0', port=5000)