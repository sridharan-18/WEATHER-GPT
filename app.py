from flask import Flask, render_template, request, jsonify
import os
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configuration
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY', 'your_openweathermap_api_key')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'your_openai_api_key')

# Initialize weather assistant service
try:
    from services import WeatherAssistant
    weather_assistant = WeatherAssistant(
        openai_api_key=OPENAI_API_KEY,
        weather_api_key=WEATHER_API_KEY
    )
    ASSISTANT_AVAILABLE = True
except ImportError:
    ASSISTANT_AVAILABLE = False
    print("Weather assistant service not available. Using fallback implementation.")
    # Fallback to inline implementation
    weather_assistant = None

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

# Initialize multilingual and accessibility services (optional - only if configured)
try:
    from services import TranslationService, VoiceAssistant, translation_service, voice_assistant
    MULTILINGUAL_AVAILABLE = True
except ImportError:
    MULTILINGUAL_AVAILABLE = False
    translation_service = None
    voice_assistant = None
    print("Multilingual and accessibility services not available. Install required dependencies for these features.")

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages with AI integration"""
    data = request.get_json(silent=True)
    if data is None or not isinstance(data, dict):
        return jsonify({'error': 'Invalid or missing JSON'}), 400
    user_message = data.get('message', '')
    
    if not user_message:
        return jsonify({'response': 'Please provide a message.'})
    
    try:
        if ASSISTANT_AVAILABLE and weather_assistant:
            # Use modular weather assistant service
            result = weather_assistant.process_query(user_message)
            return jsonify(result)
        else:
            # Fallback to inline implementation
            return chat_fallback(user_message)
            
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'response': 'Sorry, I encountered an error processing your request. Please try again.'})


def _get_json_body():
    """Safely parse the request body as JSON.

    Returns the parsed dictionary, or None when the body is missing or not
    valid JSON. API routes use this instead of request.json so they can
    return a clean JSON error (rather than an HTML 415/500 page) for
    malformed payloads.
    """
    return request.get_json(silent=True)


def chat_fallback(user_message):
    """Fallback chat implementation when service is unavailable"""
    import requests
    
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

# Fallback functions (used when service is unavailable)
def extract_location(message):
    """Extract location from user message using whole-word matching.

    Extracts only the words immediately following a keyword (up to 2),
    stopping at common filler words. This avoids picking up trailing
    words like "today" or "tomorrow" as part of the location.
    """
    message_lower = message.lower()
    location_keywords = ['in', 'at', 'for', 'near']
    filler_words = {'today', 'tomorrow', 'and', 'please', 'if', 'the', 'a', 'an', 'it', 'of', 'on', 'to', 'with', 'from', 'is'}
    words = message_lower.split()

    for index, word in enumerate(words):
        if word in location_keywords:
            # Take up to 2 words after the keyword, stopping at filler words
            # like "today" or "tomorrow". This prevents trailing words from
            # being incorrectly included in the extracted location.
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
    return None


def get_weather_data(location):
    """Get weather data from OpenWeatherMap API"""
    import requests
    try:
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            'q': location,
            'appid': WEATHER_API_KEY,
            'units': 'metric'
        }
        
        response = requests.get(url, params=params, timeout=10)
        
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
            return generate_openai_response(user_message, weather_data)
        else:
            return generate_rule_based_response(user_message, weather_data)
    except Exception as e:
        print(f"Error generating AI response: {e}")
        return generate_rule_based_response(user_message, weather_data)


def generate_openai_response(user_message, weather_data):
    """Generate response using OpenAI API"""
    try:
        import openai
        
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        
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
        # Use .get() with defaults so the function doesn't crash on partial
        # weather data (e.g. a malformed or incomplete API response).
        main = weather_data.get('main', {}) or {}
        temp = main.get('temp')
        humidity = main.get('humidity')
        weather_list = weather_data.get('weather', []) or []
        description = weather_list[0].get('description', 'unknown') if weather_list else 'unknown'
        location = weather_data.get('name', 'Unknown location')

        advice = []
        
        if isinstance(temp, (int, float)):
            if temp > 30:
                advice.append("🥵 It's quite hot! Stay hydrated and avoid direct sunlight.")
            elif temp < 5:
                advice.append("❄️ It's very cold! Wear heavy layers and protect exposed skin.")
            elif temp < 15:
                advice.append("🧥 It's chilly - dress warmly!")
            else:
                advice.append("😊 Pleasant temperature - great for outdoor activities!")
        
        if isinstance(humidity, (int, float)):
            if humidity > 80:
                advice.append("💧 High humidity - it might feel muggy. Consider staying indoors.")
            elif humidity < 30:
                advice.append("🌵 Low humidity - stay moisturized and drink plenty of water.")
        
        if isinstance(description, str) and description:
            desc_lower = description.lower()
            if 'rain' in desc_lower or 'drizzle' in desc_lower:
                advice.append("☔ Don't forget an umbrella or raincoat!")
            elif 'clear' in desc_lower:
                advice.append("😎 Great weather for outdoor activities!")
            elif 'cloud' in desc_lower:
                advice.append("☁️ Partly cloudy - pleasant weather overall.")
            elif 'storm' in desc_lower or 'thunder' in desc_lower:
                advice.append("⚡ Stormy conditions - stay indoors and avoid travel if possible.")
        
        # Format values for display (convert None to 'unknown' for safety).
        temp_display = f"{temp}°C" if temp is not None else "unknown°C"
        feels_like = main.get('feels_like')
        feels_like_display = f"{feels_like}°C" if feels_like is not None else temp_display
        response = f"📍 Weather in {location}: {description}, {temp_display} (feels like {feels_like_display})\n\n"
        response += "💡 Advice:\n" + "\n".join(f"• {tip}" for tip in advice)
        
        return response
    else:
        if 'hello' in message_lower or 'hi' in message_lower:
            return "Hello! 👋 I'm your weather assistant. Ask me about weather conditions in any location, and I'll provide you with current information and actionable advice!"
        elif 'help' in message_lower:
            return "I can help you with:\n• Current weather conditions for any location\n• Actionable advice based on weather\n• Hazard risk information\n\nJust ask something like 'What's the weather like in Sulur?' or 'Should I carry an umbrella today?'"
        else:
            return "I'd be happy to help with weather information! Please specify a location, for example: 'What's the weather like in [city name]?'"


@app.route('/api/weather/<location>')
def weather(location):
    """Get weather data for a specific location"""
    if ASSISTANT_AVAILABLE and weather_assistant:
        weather_data = weather_assistant.get_weather_data(location)
    else:
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
    
    data = _get_json_body()
    if data is None:
        return jsonify({'error': 'Invalid or missing JSON'}), 400
    email = data.get('email')
    name = data.get('name', '')
    phone = data.get('phone', '')
    locations = data.get('locations', ['Sulur'])
    
    if not email:
        return jsonify({'error': 'Email is required'}), 400
    
    email = email.strip().lower()
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return jsonify({'error': 'Invalid email format'}), 400
    
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
    
    data = _get_json_body()
    if data is None:
        return jsonify({'error': 'Invalid or missing JSON'}), 400
    email = data.get('email')
    
    if not email:
        return jsonify({'error': 'Email is required'}), 400
    
    email = email.strip().lower()
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return jsonify({'error': 'Invalid email format'}), 400
    
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
    
    data = _get_json_body()
    if data is None:
        return jsonify({'error': 'Invalid or missing JSON'}), 400
    email = data.get('email')
    phone = data.get('phone')
    
    if not email:
        return jsonify({'error': 'Email is required'}), 400
    
    email = email.strip().lower()
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return jsonify({'error': 'Invalid email format'}), 400
    
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
    
    data = _get_json_body()
    if data is None:
        return jsonify({'error': 'Invalid or missing JSON'}), 400
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
    
    data = _get_json_body()
    if data is None:
        return jsonify({'error': 'Invalid or missing JSON'}), 400
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
    
    data = _get_json_body()
    if data is None:
        return jsonify({'error': 'Invalid or missing JSON'}), 400
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
    
    data = _get_json_body()
    if data is None:
        return jsonify({'error': 'Invalid or missing JSON'}), 400
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
    
    data = _get_json_body()
    if data is None:
        return jsonify({'error': 'Invalid or missing JSON'}), 400
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

# Multilingual API endpoints
@app.route('/api/languages')
def get_supported_languages():
    """Get all supported languages"""
    if not MULTILINGUAL_AVAILABLE:
        return jsonify({'error': 'Multilingual services not available'}), 503
    
    return jsonify({
        'languages': translation_service.get_supported_languages(),
        'current_language': translation_service.get_current_language()
    })

@app.route('/api/language', methods=['POST'])
def set_language():
    """Set the current language"""
    if not MULTILINGUAL_AVAILABLE:
        return jsonify({'error': 'Multilingual services not available'}), 503
    
    data = _get_json_body()
    if data is None:
        return jsonify({'error': 'Invalid or missing JSON'}), 400
    language = data.get('language', 'en')
    
    success = translation_service.set_language(language)
    if success:
        return jsonify({
            'message': f'Language set to {translation_service.supported_languages[language]}',
            'current_language': translation_service.get_current_language()
        })
    else:
        return jsonify({'error': 'Invalid language code'}), 400

@app.route('/api/translate', methods=['POST'])
def translate_text():
    """Translate text to target language"""
    if not MULTILINGUAL_AVAILABLE:
        return jsonify({'error': 'Multilingual services not available'}), 503
    
    data = _get_json_body()
    if data is None:
        return jsonify({'error': 'Invalid or missing JSON'}), 400
    text = data.get('text', '')
    target_language = data.get('language', None)
    
    if not text:
        return jsonify({'error': 'Text is required'}), 400
    
    # For simple UI translations, use the translation service
    # For full AI responses, you would use a translation API
    translated = translation_service.translate(text, target_language)
    
    return jsonify({
        'original': text,
        'translated': translated,
        'language': target_language or translation_service.get_current_language()
    })

@app.route('/api/translate-weather', methods=['POST'])
def translate_weather_response():
    """Translate AI weather response to target language"""
    if not MULTILINGUAL_AVAILABLE:
        return jsonify({'error': 'Multilingual services not available'}), 503
    
    data = _get_json_body()
    if data is None:
        return jsonify({'error': 'Invalid or missing JSON'}), 400
    response = data.get('response', '')
    target_language = data.get('language', None)
    
    if not response:
        return jsonify({'error': 'Response is required'}), 400
    
    translated = translation_service.translate_weather_response(response, target_language)
    
    return jsonify({
        'original': response,
        'translated': translated,
        'language': target_language or translation_service.get_current_language()
    })

# Voice Assistant API endpoints
@app.route('/api/voice/status')
def get_voice_status():
    """Get voice assistant status"""
    if not MULTILINGUAL_AVAILABLE:
        return jsonify({'error': 'Voice assistant not available'}), 503
    
    return jsonify({
        'enabled': voice_assistant.is_enabled(),
        'language': voice_assistant.get_language(),
        'settings': voice_assistant.get_voice_settings(),
        'accessibility_features': voice_assistant.get_accessibility_features()
    })

@app.route('/api/voice/enable', methods=['POST'])
def enable_voice():
    """Enable voice assistant"""
    if not MULTILINGUAL_AVAILABLE:
        return jsonify({'error': 'Voice assistant not available'}), 503
    
    voice_assistant.enable()
    return jsonify({
        'message': 'Voice assistant enabled',
        'status': voice_assistant.get_accessibility_features()
    })

@app.route('/api/voice/disable', methods=['POST'])
def disable_voice():
    """Disable voice assistant"""
    if not MULTILINGUAL_AVAILABLE:
        return jsonify({'error': 'Voice assistant not available'}), 503
    
    voice_assistant.disable()
    return jsonify({
        'message': 'Voice assistant disabled',
        'status': voice_assistant.get_accessibility_features()
    })

@app.route('/api/voice/settings', methods=['POST'])
def update_voice_settings():
    """Update voice assistant settings"""
    if not MULTILINGUAL_AVAILABLE:
        return jsonify({'error': 'Voice assistant not available'}), 503
    
    data = _get_json_body()
    if data is None:
        return jsonify({'error': 'Invalid or missing JSON'}), 400
    voice_assistant.update_voice_settings(data)
    
    return jsonify({
        'message': 'Voice settings updated',
        'settings': voice_assistant.get_voice_settings()
    })

@app.route('/api/voice/speak', methods=['POST'])
def text_to_speech():
    """Generate text-to-speech configuration"""
    if not MULTILINGUAL_AVAILABLE:
        return jsonify({'error': 'Voice assistant not available'}), 503
    
    data = _get_json_body()
    if data is None:
        return jsonify({'error': 'Invalid or missing JSON'}), 400
    text = data.get('text', '')
    language = data.get('language', None)
    
    if not text:
        return jsonify({'error': 'Text is required'}), 400
    
    tts_config = voice_assistant.generate_tts_response(text, language)
    
    return jsonify(tts_config)

@app.route('/api/voice/listen', methods=['POST'])
def speech_to_text():
    """Generate speech-to-text configuration"""
    if not MULTILINGUAL_AVAILABLE:
        return jsonify({'error': 'Voice assistant not available'}), 503
    
    data = _get_json_body()
    if data is None:
        return jsonify({'error': 'Invalid or missing JSON'}), 400
    language = data.get('language', None)
    
    stt_config = voice_assistant.generate_stt_config(language)
    
    return jsonify(stt_config)

@app.route('/api/voice/commands')
def get_voice_commands():
    """Get supported voice commands"""
    if not MULTILINGUAL_AVAILABLE:
        return jsonify({'error': 'Voice assistant not available'}), 503
    
    language = request.args.get('language', None)
    commands = voice_assistant.get_voice_commands(language)
    
    return jsonify({
        'commands': commands,
        'language': language or voice_assistant.get_language()
    })

@app.route('/api/voice/parse', methods=['POST'])
def parse_voice_command():
    """Parse voice command and extract intent"""
    if not MULTILINGUAL_AVAILABLE:
        return jsonify({'error': 'Voice assistant not available'}), 503
    
    data = _get_json_body()
    if data is None:
        return jsonify({'error': 'Invalid or missing JSON'}), 400
    text = data.get('text', '')
    language = data.get('language', None)
    
    if not text:
        return jsonify({'error': 'Text is required'}), 400
    
    parsed_command = voice_assistant.parse_voice_command(text, language)
    
    return jsonify(parsed_command)

@app.route('/api/accessibility')
def get_accessibility_features():
    """Get all accessibility features"""
    if not MULTILINGUAL_AVAILABLE:
        return jsonify({'error': 'Accessibility features not available'}), 503
    
    return jsonify(voice_assistant.get_accessibility_features())

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