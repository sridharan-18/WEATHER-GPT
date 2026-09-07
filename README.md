# WeatherGPT — Hyperlocal Weather Risk Intelligence

Turn raw meteorological data into a 0-100 safety score, explainable alerts and actionable advice.

## Features

- **Weather Safety Score**: 0-100 safety score based on current conditions
- **Live Conditions**: Real-time weather data display
- **12-Hour Risk Forecast**: Predictive risk assessment
- **Hazard Breakdown**: Detailed hazard analysis
- **Actions for Farmer**: Actionable recommendations
- **Hazard Map**: Interactive weather visualization (Phase 2)
- **WeatherGPT Assistant**: Conversational AI for weather insights (Phase 2)

## Tech Stack

- **Frontend**: Next.js 14 with TypeScript
- **UI Components**: shadcn/ui
- **Styling**: Tailwind CSS
- **Weather API**: OpenWeatherMap
- **State Management**: React Context
- **Icons**: Lucide React

## Getting Started

### Prerequisites

- Node.js 18+ 
- npm or yarn
- OpenWeatherMap API key

### Installation

```bash
# Install dependencies
npm install

# Set up environment variables
cp .env.example .env.local

# Add your OpenWeatherMap API key to .env.local
NEXT_PUBLIC_OPENWEATHER_API_KEY=your_api_key_here

# Run development server
npm run dev
```

### Environment Variables

```
NEXT_PUBLIC_OPENWEATHER_API_KEY=your_openweathermap_api_key
```

## Project Structure

```
WeatherGPT/
├── src/
│   ├── app/              # Next.js app directory
│   ├── components/       # React components
│   ├── lib/             # Utility functions
│   ├── types/           # TypeScript types
│   └── hooks/           # Custom React hooks
├── public/              # Static assets
└── package.json
```

## Features Overview

### Weather Safety Score Algorithm

The safety score (0-100) is calculated based on:
- Temperature extremes
- Precipitation intensity
- Wind speed
- Visibility
- Severe weather alerts
- Historical risk patterns

### Risk Categories

- **0-20**: Critical Risk - Take immediate shelter
- **21-40**: High Risk - Avoid outdoor activities
- **41-60**: Moderate Risk - Exercise caution
- **61-80**: Low Risk - Normal activities
- **81-100**: Safe - Ideal conditions

## API Integration

Uses OpenWeatherMap API for:
- Current weather data
- 12-hour forecast
- Weather alerts
- Historical data

## Future Enhancements (Phase 2)

- Interactive Leaflet hazard maps
- WeatherGPT conversational assistant
- Multi-location support
- Historical risk analytics
- Mobile app

## License

MIT
