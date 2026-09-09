export interface LocationResult {
  id: number
  name: string
  latitude: number
  longitude: number
  country?: string
  country_code?: string
  admin1?: string
  timezone?: string
}

export interface WeatherResponse {
  latitude: number
  longitude: number
  timezone: string
  current: {
    time: string
    temperature_2m: number
    apparent_temperature: number
    relative_humidity_2m: number
    precipitation: number
    weather_code: number
    cloud_cover: number
    pressure_msl: number
    wind_speed_10m: number
    wind_direction_10m: number
    visibility: number
  }
  hourly: {
    time: string[]
    temperature_2m: number[]
    precipitation_probability: number[]
    precipitation: number[]
    weather_code: number[]
    wind_speed_10m: number[]
    visibility: number[]
  }
  daily: {
    time: string[]
    weather_code: number[]
    temperature_2m_max: number[]
    temperature_2m_min: number[]
    precipitation_sum: number[]
    precipitation_probability_max: number[]
    wind_speed_10m_max: number[]
    sunrise: string[]
    sunset: string[]
  }
}

const FORECAST_BASE_URL = "https://api.open-meteo.com/v1/forecast"
const GEOCODING_BASE_URL = "https://geocoding-api.open-meteo.com/v1/search"

export async function searchLocations(query: string): Promise<LocationResult[]> {
  const params = new URLSearchParams({
    name: query,
    count: "6",
    language: "en",
    format: "json",
  })

  const response = await fetch(`${GEOCODING_BASE_URL}?${params.toString()}`)
  if (!response.ok) {
    throw new Error("Location search failed")
  }

  const data = await response.json()
  return data.results ?? []
}

export async function getWeather(
  latitude: number,
  longitude: number,
): Promise<WeatherResponse> {
  const params = new URLSearchParams({
    latitude: latitude.toString(),
    longitude: longitude.toString(),
    current: [
      "temperature_2m",
      "apparent_temperature",
      "relative_humidity_2m",
      "precipitation",
      "weather_code",
      "cloud_cover",
      "pressure_msl",
      "wind_speed_10m",
      "wind_direction_10m",
      "visibility",
    ].join(","),
    hourly: [
      "temperature_2m",
      "precipitation_probability",
      "precipitation",
      "weather_code",
      "wind_speed_10m",
      "visibility",
    ].join(","),
    daily: [
      "weather_code",
      "temperature_2m_max",
      "temperature_2m_min",
      "precipitation_sum",
      "precipitation_probability_max",
      "wind_speed_10m_max",
      "sunrise",
      "sunset",
    ].join(","),
    forecast_days: "7",
    timezone: "auto",
    temperature_unit: "celsius",
    wind_speed_unit: "kmh",
    precipitation_unit: "mm",
  })

  const response = await fetch(`${FORECAST_BASE_URL}?${params.toString()}`, {
    cache: "no-store",
  })

  if (!response.ok) {
    throw new Error("Weather service is unavailable")
  }

  return response.json()
}

export function weatherCodeToText(code: number): string {
  if (code === 0) return "Clear sky"
  if ([1, 2, 3].includes(code)) return "Partly cloudy"
  if ([45, 48].includes(code)) return "Foggy"
  if ([51, 53, 55, 56, 57].includes(code)) return "Drizzle"
  if ([61, 63, 65, 66, 67].includes(code)) return "Rain"
  if ([71, 73, 75, 77].includes(code)) return "Snow"
  if ([80, 81, 82].includes(code)) return "Rain showers"
  if ([85, 86].includes(code)) return "Snow showers"
  if ([95, 96, 99].includes(code)) return "Thunderstorm"
  return "Unknown"
}
