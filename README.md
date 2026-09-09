# WeatherGPT — Hyperlocal Weather Risk Intelligence

WeatherGPT turns live meteorological data into a 0–100 safety score, explainable hazards and actionable weather advice.

## Current features

- **Live weather data** using Open-Meteo
- **Location search** for cities and towns
- **Use My Location** with browser geolocation
- **Weather Safety Score** calculated from live conditions
- **Explainable risk factors** showing why risk changes
- **Live Conditions** for temperature, feels-like temperature, humidity, wind, pressure and condition
- **Next 8 Hours** with temperature and rain probability
- **7-Day Forecast**
- **Hazard Breakdown**
- **Farmer Actions** based on rainfall, wind and storms
- Responsive dashboard built with Next.js and Tailwind CSS

## Roadmap

- Interactive Leaflet hazard map
- AI WeatherGPT conversational assistant
- Proactive severe-weather notifications
- Flood, heat, lightning and visibility risk layers
- Crop-specific recommendations
- Tamil and other Indian regional languages
- Voice assistant
- Historical weather/risk analytics
- PWA/mobile installation

## Tech Stack

- **Frontend:** Next.js 14 + TypeScript
- **Styling:** Tailwind CSS
- **Icons:** Lucide React
- **Weather & Geocoding:** Open-Meteo
- **Runtime:** Node.js 18+

## Getting Started

```bash
npm install
npm run dev
```

Open `http://localhost:3000` in your browser.

### Build for production

```bash
npm run build
npm start
```

## Architecture

```text
Browser
  │
  ├── Location search ──> Open-Meteo Geocoding API
  │
  ├── GPS coordinates ──> Open-Meteo Forecast API
  │
  └── Live weather ─────> Risk Engine ─────> Safety Score
                                      └─────> Hazard explanations
```

## Safety score

The current prototype derives a transparent 0–100 score from live temperature, rain probability, wind, visibility and thunderstorm conditions. The score is intentionally explainable so users can see which factors are affecting the result.

This score is an application-level indicator, not an official emergency warning. Official government alerts should remain the source of truth for emergency decisions.

## License

MIT
