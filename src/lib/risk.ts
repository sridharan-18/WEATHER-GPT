import type { WeatherResponse } from "@/lib/weather"

export type HazardKey = "rain" | "storm" | "heat" | "wind" | "visibility"

export interface HazardScore {
  key: HazardKey
  label: string
  score: number
  level: "Safe" | "Moderate" | "High" | "Extreme"
  detail: string
  action: string
}

export interface WeatherRiskSummary {
  safetyScore: number
  level: "Safe" | "Low risk" | "Moderate risk" | "High risk" | "Critical risk"
  hazards: HazardScore[]
  reasons: string[]
}

function clamp(value: number) {
  return Math.max(0, Math.min(100, Math.round(value)))
}

function levelFor(score: number): HazardScore["level"] {
  if (score >= 75) return "Extreme"
  if (score >= 50) return "High"
  if (score >= 25) return "Moderate"
  return "Safe"
}

function riskLabel(score: number): WeatherRiskSummary["level"] {
  if (score >= 80) return "Critical risk"
  if (score >= 60) return "High risk"
  if (score >= 35) return "Moderate risk"
  if (score >= 15) return "Low risk"
  return "Safe"
}

function maxNextHours(values: number[], currentTime: string, times: string[], hours = 6) {
  const start = Math.max(0, times.findIndex((time) => time >= currentTime))
  const window = values.slice(start >= 0 ? start : 0, (start >= 0 ? start : 0) + hours)
  return window.length ? Math.max(...window) : 0
}

export function calculateWeatherRisks(weather: WeatherResponse): WeatherRiskSummary {
  const { current, hourly } = weather
  const nextRain = maxNextHours(hourly.precipitation_probability, current.time, hourly.time)
  const nextWind = maxNextHours(hourly.wind_speed_10m, current.time, hourly.time)
  const nextVisibility = Math.min(...hourly.visibility.slice(0, 6).filter(Boolean), current.visibility)
  const stormCodes = [95, 96, 99]
  const stormAhead = hourly.weather_code.some((code, index) => index < 8 && stormCodes.includes(code))
  const rain = clamp(Math.max(nextRain, current.precipitation > 0 ? 45 : 0))
  const storm = stormAhead || stormCodes.includes(current.weather_code) ? 85 : 0
  const heat = clamp((Math.max(current.temperature_2m, current.apparent_temperature) - 24) * 6.25)
  const wind = clamp((Math.max(current.wind_speed_10m, nextWind) - 15) * 2.4)
  const visibility = clamp((10000 - Math.min(current.visibility, nextVisibility)) / 80)

  const hazards: HazardScore[] = [
    {
      key: "rain",
      label: "Rain",
      score: rain,
      level: levelFor(rain),
      detail: `${nextRain}% chance in the next 6 hours`,
      action: rain >= 50 ? "Carry rain protection and plan covered travel." : "Outdoor plans are broadly favorable.",
    },
    {
      key: "storm",
      label: "Storm",
      score: storm,
      level: levelFor(storm),
      detail: storm ? "Thunderstorm signal in the near-term forecast" : "No thunderstorm signal detected",
      action: storm ? "Avoid exposed areas and postpone outdoor activity." : "No storm precautions needed right now.",
    },
    {
      key: "heat",
      label: "Heat",
      score: heat,
      level: levelFor(heat),
      detail: `Feels like ${Math.round(current.apparent_temperature)}°C`,
      action: heat >= 50 ? "Take shade breaks and drink water regularly." : "Normal heat precautions are enough.",
    },
    {
      key: "wind",
      label: "Wind",
      score: wind,
      level: levelFor(wind),
      detail: `Up to ${Math.round(Math.max(current.wind_speed_10m, nextWind))} km/h expected`,
      action: wind >= 50 ? "Secure loose objects and avoid exposed routes." : "Wind should not disrupt most plans.",
    },
    {
      key: "visibility",
      label: "Visibility",
      score: visibility,
      level: levelFor(visibility),
      detail: `${(Math.min(current.visibility, nextVisibility) / 1000).toFixed(1)} km visibility`,
      action: visibility >= 50 ? "Use extra caution while driving, especially at night." : "Visibility is suitable for normal travel.",
    },
  ]

  const weightedRisk = hazards.reduce((total, hazard) => {
    const weight = hazard.key === "rain" ? 0.3 : hazard.key === "storm" ? 0.25 : hazard.key === "heat" ? 0.2 : hazard.key === "wind" ? 0.15 : 0.1
    return total + hazard.score * weight
  }, 0)
  const riskScore = clamp(weightedRisk)
  const reasons = hazards
    .filter((hazard) => hazard.score >= 25)
    .sort((left, right) => right.score - left.score)
    .slice(0, 3)
    .map((hazard) => `${hazard.label}: ${hazard.detail}`)

  return {
    safetyScore: 100 - riskScore,
    level: riskLabel(riskScore),
    hazards,
    reasons: reasons.length ? reasons : ["No significant weather hazards detected"],
  }
}
