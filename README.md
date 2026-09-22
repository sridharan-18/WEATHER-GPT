# 🌤️ Weather GPT - Interactive Hazard Map

An interactive weather application with hazard mapping and AI-powered conversational assistance.

## Features

### 🗺️ Interactive Hazard Map
- **Leaflet-based map** with hyperlocal zoom capabilities
- **Multiple hazard risk layers:**
  - 🌊 Flood Risk
  - 🔥 Heat Risk  
  - ⚡ Lightning Risk
  - 👁️ Visibility Risk
- Color-coded risk indicators (High/Medium/Low)
- Click-to-explore location details

### 🤖 AI Conversational Assistant
- **GPT-powered weather Q&A** for natural language queries
- **Actionable weather advice** tailored to current conditions
- **Location-specific insights** with personalized recommendations
- Examples:
  - "What's the weather like in Sulur today?"
  - "Should I carry an umbrella?"
  - "Is it safe to travel tomorrow?"

### 🔔 Proactive Notifications
- **Severe-weather alerts** via email and SMS
- **Daily weather digests** with safety scores
- **Real-time monitoring** of multiple locations
- **Smart alert detection** based on weather conditions
- **User subscription management** with customizable preferences

### 🌾 Agricultural Advisory System
- **Crop-specific recommendations** based on weather conditions
- **Smart irrigation scheduling** with water conservation tips
- **Farmer action plans** with immediate and long-term recommendations
- **Harvest timing recommendations** for optimal quality
- **Storm impact analysis** with protection and recovery measures
- **Multi-crop support** including rice, wheat, maize, cotton, vegetables, and fruits
- **Growth stage sensitivity** analysis for vulnerable periods

## Tech Stack

- **Frontend:** HTML, CSS, JavaScript, Leaflet.js
- **Backend:** Flask (Python)
- **AI Integration:** OpenAI GPT API
- **Weather Data:** OpenWeatherMap API
- **Mapping:** OpenStreetMap via Leaflet
- **Email Notifications:** SMTP (Gmail, etc.)
- **SMS Notifications:** Twilio API
- **Task Scheduling:** Python Schedule Library
- **Agricultural Intelligence:** Custom crop database and advisory algorithms

## Installation

1. **Clone the repository**
```bash
git clone https://github.com/sridharan-18/WEATHER-GPT.git
cd WEATHER-GPT
```

2. **Create virtual environment**
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
source venv/bin/activate  # On Mac/Linux
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp .env.example .env
```

Edit `.env` and add your API keys:
```
# Weather API Configuration
WEATHER_API_KEY=your_openweathermap_api_key
OPENAI_API_KEY=your_openai_api_key

# Email Notification Configuration (SMTP)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_specific_password
FROM_EMAIL=noreply@weathergpt.com

# SMS Notification Configuration (Twilio)
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_FROM_NUMBER=+1234567890

# Scheduler Configuration
SCHEDULER_ENABLED=true
DAILY_DIGEST_TIME=08:00
WEATHER_CHECK_INTERVAL=3600
```

### Getting API Keys

- **OpenWeatherMap:** Sign up at [openweathermap.org](https://openweathermap.org/api)
- **OpenAI:** Get API key at [platform.openai.com](https://platform.openai.com/api-keys)
- **Twilio (SMS):** Get account at [twilio.com](https://www.twilio.com)
- **Gmail SMTP:** Use App Password if 2FA is enabled

## Usage

1. **Run the application**
```bash
python app.py
```

2. **Open browser**
Navigate to `http://localhost:5000`

3. **Use the map:**
   - Toggle hazard layers using checkboxes
   - Click on map to see location details
   - Zoom into hyperlocal regions

4. **Chat with AI assistant:**
   - Ask weather questions in natural language
   - Get personalized advice for any location
   - Receive actionable recommendations

5. **Enable notifications (optional):**
   - Configure email/SMS settings in `.env`
   - Subscribe to daily digests and severe weather alerts
   - Run the scheduler: `python start_scheduler.py`

6. **Use agricultural features:**
   - Navigate to the Agriculture section in the web interface
   - Get crop recommendations based on current weather
   - Use irrigation scheduling for water management
   - Generate farmer action plans for comprehensive guidance
   - Get harvest timing recommendations
   - Analyze storm impact on your crops

## Project Structure

```
WEATHER-GPT/
├── app.py                 # Flask backend with AI integration
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .gitignore            # Git ignore rules
├── start_scheduler.py    # Standalone scheduler script
├── test_notifications.py # Notification system test script
├── test_crop_db_direct.py # Agricultural features test script
├── services/
│   ├── __init__.py      # Services package initialization
│   ├── notification_service.py  # Main notification coordinator
│   ├── email_service.py  # Email notification handler
│   ├── sms_service.py    # SMS notification handler
│   ├── alert_detector.py # Severe weather detection
│   ├── subscription_manager.py # User subscription management
│   ├── scheduler.py      # Task scheduling system
│   └── agriculture/
│       ├── __init__.py  # Agriculture services package
│       ├── crop_database.py  # Comprehensive crop database
│       ├── crop_advisor.py    # Crop recommendation engine
│       ├── farmer_action_planner.py # Action plan generator
│       ├── irrigation_scheduler.py  # Smart irrigation scheduling
│       ├── harvest_advisor.py   # Harvest timing recommendations
│       └── storm_impact_analyzer.py # Storm impact analysis
├── static/
│   ├── css/
│   │   └── style.css     # Application styling
│   └── js/
│       ├── map.js        # Leaflet map functionality
│       ├── chat.js       # Chat interface logic
│       └── agriculture.js # Agricultural features interface
└── templates/
    └── index.html        # Main HTML template
```

## Features in Detail

### Hazard Risk Layers
The map displays four types of environmental hazards:
- **Flood Risk:** Water accumulation and flooding potential
- **Heat Risk:** Temperature extremes and heat waves
- **Lightning Risk:** Electrical storm activity
- **Visibility Risk:** Fog, haze, and visibility impairment

Each risk level is color-coded:
- 🔴 Red: High risk
- 🟡 Yellow: Medium risk  
- 🟢 Green: Low risk

### AI Assistant Capabilities
- Natural language understanding for weather queries
- Context-aware responses based on current conditions
- Personalized recommendations (clothing, travel, activities)
- Safety advisories for extreme weather events

### Notification System Features
- **Severe Weather Detection:** Automatically detects dangerous conditions
  - Extreme temperatures (heat/cold)
  - Thunderstorms and lightning
  - Heavy rain and flooding
  - High winds
  - Low visibility
  - Tornadoes and extreme events

- **Safety Scoring:** Calculates 0-100 safety score based on conditions
  - 80-100: Low Risk (Green)
  - 60-79: Moderate Risk (Yellow)
  - 40-59: High Risk (Orange)
  - 0-39: Very High Risk (Red)

- **Smart Notifications:**
  - Email alerts for all severe weather
  - SMS alerts for critical conditions only
  - Daily weather digests at scheduled times
  - Location-specific monitoring

- **Subscription Management:**
  - Subscribe/unsubscribe via API
  - Custom notification preferences
  - Multiple location monitoring
  - Email and SMS channel control

### Agricultural Advisory Features
- **Crop Database:** Comprehensive database with 10+ crops including:
  - Cereals: Rice, Wheat, Maize
  - Commercial: Cotton, Sugarcane
  - Oilseeds: Groundnut
  - Vegetables: Tomato
  - Fruits: Banana, Coconut
  - Spices: Turmeric

- **Crop Recommendations:** AI-powered crop suggestions based on:
  - Current weather conditions
  - Temperature and humidity suitability
  - Wind tolerance assessment
  - Growth stage sensitivity
  - Risk factor identification

- **Irrigation Scheduling:** Smart water management with:
  - Weather-adjusted irrigation timing
  - Soil moisture-based recommendations
  - Water conservation tips
  - Multi-crop irrigation planning
  - Urgency-based scheduling

- **Harvest Advisory:** Optimal harvesting guidance with:
  - Weather suitability assessment
  - Quality impact predictions
  - Harvest timing recommendations
  - Post-harvest storage advice
  - Multi-crop harvest planning

- **Storm Impact Analysis:** Comprehensive storm assessment with:
  - Severity level determination
  - Crop-specific vulnerability analysis
  - Damage percentage estimation
  - Protection measure recommendations
  - Recovery action plans
  - Multi-crop impact comparison

- **Farmer Action Plans:** Comprehensive planning with:
  - Immediate action priorities
  - Short-term recommendations (24-48 hours)
  - Long-term planning (1 week+)
  - Safety considerations for workers
  - Resource requirements
  - Monitoring requirements

## API Endpoints

### Weather Endpoints
- `GET /` - Main application page
- `GET /api/weather/<location>` - Get weather data for a location
- `GET /api/safety-score/<location>` - Get safety score for a location
- `POST /api/chat` - AI chat interface

### Notification Endpoints
- `POST /api/subscribe` - Subscribe to weather notifications
  ```json
  {
    "email": "user@example.com",
    "name": "John Doe",
    "phone": "+1234567890",
    "locations": ["Sulur", "Chennai"]
  }
  ```
- `POST /api/unsubscribe` - Unsubscribe from notifications
  ```json
  {
    "email": "user@example.com"
  }
  ```
- `GET /api/subscriber/<email>` - Get subscriber information
- `POST /api/test-notification` - Send test notification
  ```json
  {
    "email": "user@example.com",
    "phone": "+1234567890"
  }
  ```

### Agricultural Endpoints
- `GET /api/agriculture/crops` - Get all available crops
- `GET /api/agriculture/crop/<crop_name>` - Get information for a specific crop
- `GET /api/agriculture/recommendations/<location>` - Get crop recommendations based on weather
- `POST /api/agriculture/crop-advice` - Get detailed advice for a specific crop
  ```json
  {
    "crop": "rice",
    "location": "Sulur"
  }
  ```
- `POST /api/agriculture/action-plan` - Get comprehensive farmer action plan
  ```json
  {
    "location": "Sulur",
    "crops": ["rice", "wheat"]
  }
  ```
- `POST /api/agriculture/irrigation` - Get irrigation schedule
  ```json
  {
    "crop": "rice",
    "location": "Sulur",
    "soil_moisture": 50
  }
  ```
- `POST /api/agriculture/harvest` - Get harvest recommendations
  ```json
  {
    "crop": "rice",
    "location": "Sulur",
    "growth_stage": "mature"
  }
  ```
- `POST /api/agriculture/storm-impact` - Get storm impact analysis
  ```json
  {
    "crop": "rice",
    "location": "Sulur",
    "growth_stage": "mature"
  }
  ```

## Testing

Run the notification system test:
```bash
python test_notifications.py
```

This will verify:
- Environment variable configuration
- Module imports
- Alert detection system
- Subscription management
- Weather API connectivity

Run the agricultural features test:
```bash
python test_crop_db_direct.py
```

This will verify:
- Crop database functionality
- Weather suitability assessment
- Crop-specific recommendations
- Agricultural service integration

## Deployment

The application can be deployed to various platforms:
- **Heroku:** Use the Procfile and deploy via Git
- **Render:** Connect GitHub repository for automatic deployment
- **Railway:** Simple deployment with environment variables
- **Vercel:** Serverless deployment option

### Production Scheduler Setup

For production deployment, run the scheduler as a background process:

**Using systemd (Linux):**
```ini
# /etc/systemd/system/weather-scheduler.service
[Unit]
Description=Weather GPT Scheduler
After=network.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/path/to/WEATHER-GPT
ExecStart=/usr/bin/python3 start_scheduler.py
Restart=always

[Install]
WantedBy=multi-user.target
```

**Using Supervisor:**
```ini
# /etc/supervisor/conf.d/weather-scheduler.conf
[program:weather-scheduler]
directory=/path/to/WEATHER-GPT
command=python3 start_scheduler.py
autostart=true
autorestart=true
user=your_user
```

**Using Docker:**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "start_scheduler.py"]
```

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Author

Created by sridharan-18

## Acknowledgments

- Leaflet.js for the mapping library
- OpenWeatherMap for weather data
- OpenAI for GPT integration
- OpenStreetMap for map tiles
- Twilio for SMS notifications
- Python Schedule for task scheduling