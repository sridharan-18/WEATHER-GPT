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

## Tech Stack

- **Frontend:** HTML, CSS, JavaScript, Leaflet.js
- **Backend:** Flask (Python)
- **AI Integration:** OpenAI GPT API
- **Weather Data:** OpenWeatherMap API
- **Mapping:** OpenStreetMap via Leaflet

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
WEATHER_API_KEY=your_openweathermap_api_key
OPENAI_API_KEY=your_openai_api_key
```

### Getting API Keys

- **OpenWeatherMap:** Sign up at [openweathermap.org](https://openweathermap.org/api)
- **OpenAI:** Get API key at [platform.openai.com](https://platform.openai.com/api-keys)

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

## Project Structure

```
WEATHER-GPT/
├── app.py                 # Flask backend with AI integration
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .gitignore            # Git ignore rules
├── static/
│   ├── css/
│   │   └── style.css     # Application styling
│   └── js/
│       ├── map.js        # Leaflet map functionality
│       └── chat.js       # Chat interface logic
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

## Deployment

The application can be deployed to various platforms:
- **Heroku:** Use the Procfile and deploy via Git
- **Render:** Connect GitHub repository for automatic deployment
- **Railway:** Simple deployment with environment variables
- **Vercel:** Serverless deployment option

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