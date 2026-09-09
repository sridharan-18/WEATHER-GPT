# WeatherGPT

WeatherGPT is a hyperlocal weather intelligence and action assistant. The current prototype provides live forecast data, location search, browser geolocation, a transparent weather-risk score, 12-hour and 7-day forecasts, farmer decision support, and a rule-based conversational assistant.

## Key features
- Live weather and forecast data from Open-Meteo
- Search any location or use browser location
- Transparent 0-100 weather risk score with reasons and actions
- 12-hour precipitation and temperature outlook
- 7-day forecast
- Farmer support for irrigation, spraying and field work
- Conversational questions about rain, travel, farming and heat
- Responsive Next.js + TypeScript + Tailwind UI

## Run locally

```bash
npm install
npm run dev
```

Open `http://localhost:3000`.

## Data
Weather data is retrieved at runtime from Open-Meteo. The risk score is a decision-support heuristic and should not replace official emergency or meteorological alerts.
