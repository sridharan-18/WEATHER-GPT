"use client"

import { useCallback, useEffect, useMemo, useState, type ReactNode } from "react"
import {
  AlertTriangle,
  Cloud,
  Droplets,
  Gauge,
  LocateFixed,
  MapPin,
  RefreshCw,
  Search,
  Shield,
  Sun,
  Thermometer,
  TrendingUp,
  Wind,
  X,
} from "lucide-react"
import {
  getWeather,
  searchLocations,
  weatherCodeToText,
  type LocationResult,
  type WeatherResponse,
} from "@/lib/weather"

interface RiskResult {
  score: number
  level: string
  reasons: string[]
}

function calculateRisk(weather: WeatherResponse): RiskResult {
  const current = weather.current
  let risk = 0
  const reasons: string[] = []

  if (current.temperature_2m >= 38) {
    risk += 25
    reasons.push("Extreme heat")
  } else if (current.temperature_2m >= 34) {
    risk += 12
    reasons.push("High temperature")
  } else if (current.temperature_2m <= 8) {
    risk += 15
    reasons.push("Low temperature")
  }

  const rainProbability = weather.hourly.precipitation_probability[0] ?? 0
  if (rainProbability >= 80) {
    risk += 25
    reasons.push("High rain probability")
  } else if (rainProbability >= 50) {
    risk += 12
    reasons.push("Moderate rain probability")
  }

  if (current.wind_speed_10m >= 50) {
    risk += 25
    reasons.push("Very strong winds")
  } else if (current.wind_speed_10m >= 30) {
    risk += 12
    reasons.push("Strong winds")
  }

  if (current.visibility < 2000) {
    risk += 20
    reasons.push("Poor visibility")
  } else if (current.visibility < 5000) {
    risk += 8
    reasons.push("Reduced visibility")
  }

  if ([95, 96, 99].includes(current.weather_code)) {
    risk += 30
    reasons.push("Thunderstorm conditions")
  }

  const score = Math.max(0, Math.min(100, 100 - risk))
  const level = score >= 80 ? "Safe" : score >= 60 ? "Low Risk" : score >= 40 ? "Moderate Risk" : score >= 20 ? "High Risk" : "Critical Risk"

  return {
    score,
    level,
    reasons: reasons.length ? reasons : ["No significant weather hazards detected"],
  }
}

function formatHour(value: string) {
  return new Date(value).toLocaleTimeString([], { hour: "numeric" })
}

function formatDay(value: string) {
  return new Date(`${value}T12:00:00`).toLocaleDateString([], { weekday: "short" })
}

export default function Home() {
  const [weather, setWeather] = useState<WeatherResponse | null>(null)
  const [location, setLocation] = useState<LocationResult>({
    id: 0,
    name: "Coimbatore",
    latitude: 11.0168,
    longitude: 76.9558,
    country: "India",
    country_code: "IN",
  })
  const [query, setQuery] = useState("")
  const [results, setResults] = useState<LocationResult[]>([])
  const [loading, setLoading] = useState(true)
  const [searching, setSearching] = useState(false)
  const [error, setError] = useState("")

  const loadWeather = useCallback(async (nextLocation: LocationResult) => {
    setLoading(true)
    setError("")
    try {
      const data = await getWeather(nextLocation.latitude, nextLocation.longitude)
      setWeather(data)
      setLocation(nextLocation)
    } catch {
      setError("Unable to load live weather. Please try again.")
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    void loadWeather(location)
  }, [loadWeather, location.latitude, location.longitude])

  const risk = useMemo(() => (weather ? calculateRisk(weather) : null), [weather])

  async function handleSearch() {
    if (!query.trim()) return
    setSearching(true)
    setError("")
    try {
      const matches = await searchLocations(query.trim())
      setResults(matches)
      if (!matches.length) setError("No locations found.")
    } catch {
      setError("Location search failed.")
    } finally {
      setSearching(false)
    }
  }

  function useMyLocation() {
    if (!navigator.geolocation) {
      setError("Geolocation is not supported by this browser.")
      return
    }

    setLoading(true)
    navigator.geolocation.getCurrentPosition(
      (position) => {
        const currentLocation: LocationResult = {
          id: Date.now(),
          name: "My Location",
          latitude: position.coords.latitude,
          longitude: position.coords.longitude,
        }
        void loadWeather(currentLocation)
      },
      () => {
        setLoading(false)
        setError("Location access was denied. Search for a city instead.")
      },
      { enableHighAccuracy: true, timeout: 10000 },
    )
  }

  if (loading && !weather) {
    return (
      <main className="min-h-screen flex items-center justify-center bg-gradient-to-br from-sky-50 to-indigo-100 p-6">
        <div className="text-center">
          <Cloud className="w-16 h-16 mx-auto mb-4 text-sky-500 animate-pulse" />
          <h1 className="text-2xl font-bold text-gray-900">WeatherGPT</h1>
          <p className="text-gray-600 mt-2">Loading live weather data...</p>
        </div>
      </main>
    )
  }

  if (!weather || !risk) return null

  const hourlyStart = weather.hourly.time.findIndex((time) => time >= weather.current.time)
  const start = hourlyStart >= 0 ? hourlyStart : 0
  const hourly = weather.hourly.time.slice(start, start + 8)

  return (
    <main className="min-h-screen bg-gradient-to-br from-sky-50 via-white to-indigo-100 p-4 md:p-8">
      <div className="max-w-7xl mx-auto">
        <header className="mb-8">
          <div className="flex flex-col lg:flex-row lg:items-end lg:justify-between gap-5">
            <div>
              <h1 className="text-4xl md:text-5xl font-bold text-gray-900">WeatherGPT</h1>
              <p className="text-gray-600 text-lg mt-2">Hyperlocal Weather Risk Intelligence</p>
            </div>

            <div className="flex flex-col sm:flex-row gap-2 w-full lg:w-auto">
              <div className="relative flex-1 lg:w-80">
                <Search className="absolute left-3 top-3.5 w-5 h-5 text-gray-400" />
                <input
                  value={query}
                  onChange={(event) => setQuery(event.target.value)}
                  onKeyDown={(event) => event.key === "Enter" && void handleSearch()}
                  placeholder="Search city or town..."
                  className="w-full rounded-xl border border-gray-200 bg-white pl-10 pr-10 py-3 outline-none focus:ring-2 focus:ring-sky-400"
                />
                {query && (
                  <button onClick={() => { setQuery(""); setResults([]) }} className="absolute right-3 top-3.5 text-gray-400">
                    <X className="w-5 h-5" />
                  </button>
                )}
                {results.length > 0 && (
                  <div className="absolute z-20 top-14 left-0 right-0 bg-white rounded-xl shadow-xl border border-gray-100 overflow-hidden">
                    {results.map((result) => (
                      <button
                        key={`${result.id}-${result.latitude}`}
                        onClick={() => { setResults([]); setQuery(""); void loadWeather(result) }}
                        className="w-full text-left px-4 py-3 hover:bg-sky-50 border-b last:border-0"
                      >
                        <span className="font-medium">{result.name}</span>
                        <span className="text-sm text-gray-500 ml-2">{result.admin1 ? `${result.admin1}, ` : ""}{result.country}</span>
                      </button>
                    ))}
                  </div>
                )}
              </div>
              <button onClick={() => void handleSearch()} disabled={searching} className="rounded-xl bg-sky-600 text-white px-5 py-3 font-medium hover:bg-sky-700 disabled:opacity-60">
                {searching ? "Searching..." : "Search"}
              </button>
              <button onClick={useMyLocation} className="rounded-xl bg-white border border-gray-200 px-4 py-3 font-medium text-gray-700 hover:bg-gray-50 flex items-center justify-center gap-2">
                <LocateFixed className="w-5 h-5" /> My Location
              </button>
            </div>
          </div>

          <div className="mt-4 flex items-center gap-2 text-sm text-gray-500">
            <MapPin className="w-4 h-4" />
            <span>{location.name}{location.country ? `, ${location.country}` : ""}</span>
            <span>•</span>
            <span>Live data</span>
            <button onClick={() => void loadWeather(location)} className="ml-2 text-sky-600 hover:text-sky-800" title="Refresh">
              <RefreshCw className={`w-4 h-4 ${loading ? "animate-spin" : ""}`} />
            </button>
          </div>

          {error && <div className="mt-4 rounded-xl bg-red-50 border border-red-200 px-4 py-3 text-red-700">{error}</div>}
        </header>

        <section className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="bg-white rounded-2xl shadow-lg p-6">
            <div className="flex items-center gap-2 mb-4">
              <Shield className="w-6 h-6 text-sky-500" />
              <h2 className="text-xl font-semibold">Weather Safety Score</h2>
            </div>
            <div className="text-center py-6">
              <div className="text-7xl font-bold text-sky-600">{risk.score}</div>
              <div className="text-2xl font-semibold text-gray-700 mt-2">{risk.level}</div>
              <div className="text-sm text-gray-500 mt-1">out of 100</div>
            </div>
            <div className="h-3 bg-gray-200 rounded-full overflow-hidden">
              <div className="h-full bg-sky-500 transition-all duration-500" style={{ width: `${risk.score}%` }} />
            </div>
            <div className="mt-5 space-y-2">
              {risk.reasons.slice(0, 3).map((reason) => (
                <div key={reason} className="flex gap-2 text-sm text-gray-600">
                  <AlertTriangle className="w-4 h-4 text-amber-500 shrink-0 mt-0.5" />
                  {reason}
                </div>
              ))}
            </div>
          </div>

          <div className="bg-white rounded-2xl shadow-lg p-6 lg:col-span-2">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-2">
                <Cloud className="w-6 h-6 text-sky-500" />
                <h2 className="text-xl font-semibold">Live Conditions</h2>
              </div>
              <span className="text-sm text-gray-500">Updated {new Date(weather.current.time).toLocaleTimeString([], { hour: "numeric", minute: "2-digit" })}</span>
            </div>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
              <Metric icon={<Thermometer className="w-5 h-5" />} label="Temperature" value={`${weather.current.temperature_2m.toFixed(1)}°C`} />
              <Metric icon={<Sun className="w-5 h-5" />} label="Feels like" value={`${weather.current.apparent_temperature.toFixed(1)}°C`} />
              <Metric icon={<Droplets className="w-5 h-5" />} label="Humidity" value={`${weather.current.relative_humidity_2m}%`} />
              <Metric icon={<Wind className="w-5 h-5" />} label="Wind" value={`${weather.current.wind_speed_10m.toFixed(0)} km/h`} />
              <Metric icon={<Gauge className="w-5 h-5" />} label="Pressure" value={`${weather.current.pressure_msl.toFixed(0)} hPa`} />
              <Metric icon={<Cloud className="w-5 h-5" />} label="Condition" value={weatherCodeToText(weather.current.weather_code)} />
            </div>
          </div>
        </section>

        <section className="mt-6 bg-white rounded-2xl shadow-lg p-6">
          <div className="flex items-center gap-2 mb-5">
            <TrendingUp className="w-6 h-6 text-sky-500" />
            <h2 className="text-xl font-semibold">Next 8 Hours</h2>
          </div>
          <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-8 gap-3">
            {hourly.map((time, index) => {
              const actualIndex = start + index
              const rain = weather.hourly.precipitation_probability[actualIndex] ?? 0
              const temp = weather.hourly.temperature_2m[actualIndex] ?? 0
              return (
                <div key={time} className="rounded-xl bg-sky-50 p-4 text-center">
                  <p className="text-sm font-medium text-gray-600">{index === 0 ? "Now" : formatHour(time)}</p>
                  <p className="text-2xl font-bold text-gray-900 mt-2">{Math.round(temp)}°</p>
                  <p className="text-sm text-sky-700 mt-2">🌧️ {rain}%</p>
                </div>
              )
            })}
          </div>
        </section>

        <section className="mt-6 bg-white rounded-2xl shadow-lg p-6">
          <div className="flex items-center gap-2 mb-5">
            <Cloud className="w-6 h-6 text-indigo-500" />
            <h2 className="text-xl font-semibold">7-Day Forecast</h2>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-7 gap-3">
            {weather.daily.time.map((day, index) => (
              <div key={day} className="rounded-xl border border-gray-100 p-4 text-center">
                <p className="font-semibold">{index === 0 ? "Today" : formatDay(day)}</p>
                <p className="text-3xl mt-3">{weatherCodeToText(weather.daily.weather_code[index]).includes("Rain") ? "🌧️" : "☁️"}</p>
                <p className="text-sm text-gray-600 mt-2">{weatherCodeToText(weather.daily.weather_code[index])}</p>
                <p className="font-semibold mt-2">{Math.round(weather.daily.temperature_2m_max[index])}° / {Math.round(weather.daily.temperature_2m_min[index])}°</p>
                <p className="text-sm text-sky-700 mt-1">Rain {weather.daily.precipitation_probability_max[index]}%</p>
              </div>
            ))}
          </div>
        </section>

        <section className="mt-6 grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="bg-white rounded-2xl shadow-lg p-6">
            <div className="flex items-center gap-2 mb-4">
              <AlertTriangle className="w-6 h-6 text-orange-500" />
              <h2 className="text-xl font-semibold">Hazard Breakdown</h2>
            </div>
            <div className="space-y-3">
              {risk.reasons.map((reason) => (
                <div key={reason} className="p-4 rounded-xl bg-orange-50 border border-orange-100 text-gray-700">{reason}</div>
              ))}
            </div>
          </div>

          <div className="bg-white rounded-2xl shadow-lg p-6">
            <div className="flex items-center gap-2 mb-4">
              <Shield className="w-6 h-6 text-green-500" />
              <h2 className="text-xl font-semibold">Actions for Farmer</h2>
            </div>
            <div className="space-y-3 text-gray-700">
              <p>💧 <strong>Irrigation:</strong> Use rainfall probability before scheduling irrigation.</p>
              <p>🌱 <strong>Crop protection:</strong> Avoid spraying when rain is likely soon.</p>
              <p>🌬️ <strong>Field work:</strong> Reconsider work during strong winds or thunderstorms.</p>
            </div>
          </div>
        </section>

        <section className="mt-6 mb-8 bg-gradient-to-r from-indigo-600 to-sky-600 rounded-2xl shadow-lg p-6 text-white">
          <div className="flex items-center gap-2 mb-2">
            <Shield className="w-6 h-6" />
            <h2 className="text-xl font-semibold">WeatherGPT Assistant</h2>
          </div>
          <p className="text-white/90">Live weather intelligence is now connected. Ask natural-language questions about this location in the next phase.</p>
          <div className="mt-4 flex flex-wrap gap-2">
            <span className="rounded-full bg-white/15 px-3 py-1 text-sm">Will it rain today?</span>
            <span className="rounded-full bg-white/15 px-3 py-1 text-sm">Is it safe to travel?</span>
            <span className="rounded-full bg-white/15 px-3 py-1 text-sm">Should I irrigate?</span>
          </div>
        </section>
      </div>
    </main>
  )
}

function Metric({ icon, label, value }: { icon: ReactNode; label: string; value: string }) {
  return (
    <div className="p-4 bg-gray-50 rounded-xl">
      <div className="flex items-center gap-2 text-gray-500 mb-2">{icon}<span className="text-sm">{label}</span></div>
      <p className="font-semibold text-gray-900">{value}</p>
    </div>
  )
}
