"use client"

import { useCallback, useEffect, useMemo, useState, type ReactNode } from "react"
import Link from "next/link"
import {
  ArrowUpRight,
  AlertTriangle,
  CheckCircle2,
  Cloud,
  CloudLightning,
  CloudRain,
  Droplets,
  Eye,
  Flame,
  Gauge,
  LocateFixed,
  Map,
  MapPin,
  MessageCircle,
  Navigation,
  PhoneCall,
  RefreshCw,
  Search,
  Shield,
  ShieldAlert,
  Siren,
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
import { calculateHourlyRisk, calculateWeatherRisks } from "@/lib/risk"
import WeatherControls from "@/components/WeatherControls"

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

  const risk = useMemo(() => (weather ? calculateWeatherRisks(weather) : null), [weather])
  const hourlyRisk = useMemo(() => (weather ? calculateHourlyRisk(weather) : []), [weather])

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
  const safestPoint = hourlyRisk.length ? hourlyRisk.reduce((best, point) => point.score < best.score ? point : best, hourlyRisk[0]) : null
  const activeHazards = risk.hazards.filter((hazard) => hazard.score >= 50)

  return (
    <main className="min-h-screen bg-gradient-to-br from-sky-50 via-white to-indigo-100 p-4 md:p-8">
      <div className="max-w-7xl mx-auto">
        <header className="mb-8">
          <div className="flex flex-col lg:flex-row lg:items-end lg:justify-between gap-5">
            <div>
              <div className="flex items-center gap-3"><h1 className="text-4xl md:text-5xl font-bold text-gray-900">WeatherGPT</h1><WeatherControls hazards={risk?.hazards} location={location.name} /></div>
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
              <div className="text-7xl font-bold text-sky-600">{risk.safetyScore}</div>
              <div className="text-2xl font-semibold text-gray-700 mt-2">{risk.level}</div>
              <div className="text-sm text-gray-500 mt-1">out of 100</div>
            </div>
            <div className="h-3 bg-gray-200 rounded-full overflow-hidden">
              <div className="h-full bg-sky-500 transition-all duration-500" style={{ width: `${risk.safetyScore}%` }} />
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

        <section className="mt-6 bg-slate-950 text-white rounded-2xl shadow-lg p-6 md:p-7">
          <div className="flex flex-col md:flex-row md:items-end md:justify-between gap-3 mb-6">
            <div>
              <p className="text-xs font-semibold uppercase tracking-[0.2em] text-cyan-300">Risk intelligence</p>
              <h2 className="text-2xl font-semibold mt-2">Today&apos;s hazard profile</h2>
            </div>
            <p className="text-sm text-slate-400 max-w-md">Each signal is calculated from current conditions and the next six hours of live forecast data.</p>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3">
            {risk.hazards.map((hazard) => (
              <div key={hazard.key} className="rounded-xl bg-white/10 border border-white/10 p-4">
                <div className="flex items-center justify-between gap-2">
                  <div className="flex items-center gap-2 text-slate-200">
                    <HazardIcon name={hazard.key} />
                    <span className="font-medium">{hazard.label}</span>
                  </div>
                  <span className="text-sm font-semibold text-cyan-200">{hazard.score}%</span>
                </div>
                <div className="mt-4 h-2 rounded-full bg-white/10 overflow-hidden">
                  <div className={`h-full rounded-full ${hazard.score >= 75 ? "bg-red-400" : hazard.score >= 50 ? "bg-orange-400" : hazard.score >= 25 ? "bg-amber-300" : "bg-emerald-400"}`} style={{ width: `${Math.max(hazard.score, 4)}%` }} />
                </div>
                <p className="text-xs text-slate-300 mt-3 min-h-8">{hazard.detail}</p>
                <p className="text-xs text-slate-400 mt-2">{hazard.action}</p>
              </div>
            ))}
          </div>
        </section>

        <section className="mt-6 grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 bg-white rounded-2xl shadow-lg p-6">
            <div className="flex items-start justify-between gap-4 mb-5">
              <div>
                <p className="text-xs font-semibold uppercase tracking-[0.18em] text-sky-600">Decision window</p>
                <h2 className="text-xl font-semibold mt-1">12-hour risk outlook</h2>
              </div>
              <TrendingUp className="w-5 h-5 text-sky-500" />
            </div>
            <div className="flex items-end gap-2 h-40 border-b border-gray-100 pb-2">
              {hourlyRisk.map((point, index) => (
                <div key={point.time} className="flex-1 h-full flex flex-col items-center justify-end gap-2 min-w-0">
                  <span className="text-xs font-semibold text-gray-700">{point.score}</span>
                  <div className={`w-full max-w-10 rounded-t-lg transition-all ${point.score >= 60 ? "bg-red-400" : point.score >= 35 ? "bg-amber-400" : "bg-emerald-400"}`} style={{ height: `${Math.max(8, point.score)}%` }} title={`${point.score}% risk`} />
                  <span className="text-[11px] text-gray-500 truncate w-full text-center">{index === 0 ? "Now" : formatHour(point.time)}</span>
                </div>
              ))}
            </div>
            <div className="mt-4 flex flex-wrap gap-x-5 gap-y-2 text-xs text-gray-500">
              <span><i className="inline-block w-2 h-2 rounded-full bg-emerald-400 mr-1" />Safe</span>
              <span><i className="inline-block w-2 h-2 rounded-full bg-amber-400 mr-1" />Moderate</span>
              <span><i className="inline-block w-2 h-2 rounded-full bg-red-400 mr-1" />High</span>
              <span className="ml-auto">Risk is recalculated from live forecast signals</span>
            </div>
          </div>

          <div className="bg-cyan-950 text-white rounded-2xl shadow-lg p-6">
            <div className="flex items-center gap-2 text-cyan-200">
              <Navigation className="w-5 h-5" />
              <p className="text-xs font-semibold uppercase tracking-[0.18em]">Safe travel window</p>
            </div>
            <h2 className="text-3xl font-semibold mt-5">{safestPoint ? formatHour(safestPoint.time) : "--"}</h2>
            <p className="text-cyan-100 mt-1">Lowest projected risk in the next 12 hours</p>
            <div className="mt-6 rounded-xl bg-white/10 p-4">
              <div className="flex items-center justify-between text-sm"><span>Average risk</span><strong>{safestPoint?.score ?? 0}/100</strong></div>
              <div className="h-2 rounded-full bg-white/10 mt-3"><div className="h-full rounded-full bg-emerald-300" style={{ width: `${Math.max(5, 100 - (safestPoint?.score ?? 0))}%` }} /></div>
              <p className="text-xs text-cyan-100 mt-3">Travel with normal caution and check the map before departure.</p>
            </div>
          </div>
        </section>

        <section className="mt-6 grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="bg-white rounded-2xl shadow-lg p-6 lg:col-span-2">
            <div className="flex items-center justify-between gap-4 mb-5">
              <div className="flex items-center gap-2"><ShieldAlert className="w-6 h-6 text-orange-500" /><h2 className="text-xl font-semibold">Impact-based alerts</h2></div>
              <span className="text-xs font-semibold uppercase tracking-wider text-gray-400">Live signals</span>
            </div>
            {activeHazards.length ? (
              <div className="space-y-3">
                {activeHazards.slice(0, 3).map((hazard) => (
                  <div key={hazard.key} className="flex items-start gap-3 rounded-xl border border-orange-100 bg-orange-50 p-4">
                    <AlertTriangle className="w-5 h-5 text-orange-500 shrink-0 mt-0.5" />
                    <div><p className="font-semibold text-gray-900">{hazard.label} risk is {hazard.level.toLowerCase()}</p><p className="text-sm text-gray-600 mt-1">{hazard.detail}. {hazard.action}</p></div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="flex items-center gap-3 rounded-xl bg-emerald-50 border border-emerald-100 p-4 text-emerald-800"><CheckCircle2 className="w-5 h-5" /><span>No active high-risk signals detected for this location.</span></div>
            )}
          </div>
          <div className="bg-white rounded-2xl shadow-lg p-6">
            <div className="flex items-center gap-2 mb-4"><Map className="w-6 h-6 text-sky-600" /><h2 className="text-xl font-semibold">Live risk map</h2></div>
            <p className="text-sm text-gray-600">See your location, risk halo, and hazard context on the interactive map.</p>
            <Link href="/map" className="mt-6 inline-flex items-center gap-2 rounded-xl bg-sky-600 text-white px-4 py-3 font-medium hover:bg-sky-700">Open map <ArrowUpRight className="w-4 h-4" /></Link>
          </div>
        </section>

        <section className="mt-6 grid grid-cols-1 md:grid-cols-3 gap-4">
          <DecisionCard icon={<Siren className="w-5 h-5" />} title="Farmer mode" text="Time irrigation and crop protection around the next rain window." />
          <DecisionCard icon={<Navigation className="w-5 h-5" />} title="Travel mode" text="Use the safest window and visibility signal before leaving." />
          <DecisionCard icon={<MessageCircle className="w-5 h-5" />} title="Ask WeatherGPT" text="Get a grounded answer using this location's live risk signals." href="/assistant" />
        </section>

        <section className="mt-6 mb-8 rounded-2xl bg-red-950 text-white p-6 md:p-7">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-5">
            <div><div className="flex items-center gap-2 text-red-200"><PhoneCall className="w-5 h-5" /><p className="text-xs font-semibold uppercase tracking-[0.18em]">Emergency action centre</p></div><h2 className="text-xl font-semibold mt-2">Need immediate help?</h2><p className="text-sm text-red-100 mt-1">Use local emergency services for life-threatening situations.</p></div>
            <div className="flex flex-wrap gap-2"><a href="tel:112" className="rounded-xl bg-white text-red-950 px-4 py-3 font-semibold hover:bg-red-50">112 Emergency</a><a href="tel:108" className="rounded-xl bg-red-800 px-4 py-3 font-semibold hover:bg-red-700">108 Ambulance</a><a href="tel:101" className="rounded-xl bg-red-800 px-4 py-3 font-semibold hover:bg-red-700">101 Fire</a></div>
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

function HazardIcon({ name }: { name: string }) {
  if (name === "rain") return <CloudRain className="w-4 h-4 text-cyan-300" />
  if (name === "storm") return <CloudLightning className="w-4 h-4 text-yellow-300" />
  if (name === "heat") return <Flame className="w-4 h-4 text-orange-300" />
  if (name === "wind") return <Wind className="w-4 h-4 text-sky-300" />
  return <Eye className="w-4 h-4 text-violet-300" />
}

function DecisionCard({ icon, title, text, href }: { icon: ReactNode; title: string; text: string; href?: string }) {
  const content = (
    <div className="h-full rounded-2xl border border-gray-200 bg-white p-5 shadow-sm hover:border-sky-300 hover:shadow-md transition">
      <div className="flex items-center gap-2 text-sky-600">{icon}<h3 className="font-semibold text-gray-900">{title}</h3></div>
      <p className="text-sm text-gray-600 mt-3">{text}</p>
      {href && <span className="inline-flex items-center gap-1 text-sm font-semibold text-sky-700 mt-4">Open assistant <ArrowUpRight className="w-4 h-4" /></span>}
    </div>
  )

  return href ? <Link href={href} className="block">{content}</Link> : content
}
