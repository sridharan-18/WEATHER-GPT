"use client"

import { FormEvent, useEffect, useState } from "react"
import Link from "next/link"
import { ArrowLeft, Bot, Loader2, MapPin, Send } from "lucide-react"
import { getWeather, weatherCodeToText, type WeatherResponse } from "@/lib/weather"

interface WeatherContext {
  location: string
  temperature: number
  humidity: number
  windSpeed: number
  rainProbability: number
  condition: string
  riskScore: number
  riskLevel: string
}

function buildContext(weather: WeatherResponse): WeatherContext {
  const c = weather.current
  const rain = weather.hourly.precipitation_probability[0] ?? 0
  let risk = 0
  if (c.temperature_2m >= 38) risk += 25
  else if (c.temperature_2m >= 34) risk += 12
  else if (c.temperature_2m <= 8) risk += 15
  if (rain >= 80) risk += 25
  else if (rain >= 50) risk += 12
  if (c.wind_speed_10m >= 50) risk += 25
  else if (c.wind_speed_10m >= 30) risk += 12
  if (c.visibility < 2000) risk += 20
  else if (c.visibility < 5000) risk += 8
  if ([95, 96, 99].includes(c.weather_code)) risk += 30
  const score = Math.max(0, Math.min(100, 100 - risk))
  return {
    location: "Coimbatore, India",
    temperature: c.temperature_2m,
    humidity: c.relative_humidity_2m,
    windSpeed: c.wind_speed_10m,
    rainProbability: rain,
    condition: weatherCodeToText(c.weather_code),
    riskScore: score,
    riskLevel: score >= 80 ? "Safe" : score >= 60 ? "Low Risk" : score >= 40 ? "Moderate Risk" : score >= 20 ? "High Risk" : "Critical Risk",
  }
}

export default function AssistantPage() {
  const [message, setMessage] = useState("")
  const [answer, setAnswer] = useState("")
  const [loading, setLoading] = useState(false)
  const [weatherLoading, setWeatherLoading] = useState(true)
  const [error, setError] = useState("")
  const [weatherContext, setWeatherContext] = useState<WeatherContext | null>(null)

  useEffect(() => {
    getWeather(11.0168, 76.9558)
      .then((data) => setWeatherContext(buildContext(data)))
      .catch(() => setError("Unable to load live weather context."))
      .finally(() => setWeatherLoading(false))
  }, [])

  async function askAssistant(event: FormEvent) {
    event.preventDefault()
    if (!message.trim() || !weatherContext) return
    setLoading(true); setError(""); setAnswer("")
    try {
      const response = await fetch("/api/assistant", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ message, weather: weatherContext }) })
      const data = await response.json()
      if (!response.ok) throw new Error(data.error || "Assistant request failed")
      setAnswer(data.answer)
    } catch (e) { setError(e instanceof Error ? e.message : "Assistant request failed") }
    finally { setLoading(false) }
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-sky-100 p-6 md:p-10">
      <div className="max-w-3xl mx-auto">
        <Link href="/" className="inline-flex items-center gap-2 text-sky-700 hover:text-sky-900 mb-6"><ArrowLeft className="w-4 h-4" /> Back to WeatherGPT</Link>
        <section className="bg-white rounded-2xl shadow-lg overflow-hidden">
          <div className="bg-gradient-to-r from-indigo-600 to-sky-600 p-6 text-white flex items-center gap-3"><Bot className="w-8 h-8" /><div><h1 className="text-2xl font-bold">WeatherGPT Assistant</h1><p className="text-white/85">Ask questions using live weather context.</p></div></div>
          <div className="p-6">
            {weatherLoading ? <div className="rounded-xl bg-sky-50 p-4 mb-6 flex gap-3"><Loader2 className="w-5 h-5 animate-spin" /> Loading live weather...</div> : weatherContext && <div className="rounded-xl bg-sky-50 p-4 mb-6"><p className="font-semibold flex items-center gap-2"><MapPin className="w-4 h-4" />{weatherContext.location}</p><p className="text-sm text-gray-600 mt-1">{weatherContext.temperature.toFixed(1)}°C · {weatherContext.condition} · Rain {weatherContext.rainProbability}% · Wind {weatherContext.windSpeed.toFixed(0)} km/h · Risk {weatherContext.riskScore}/100 ({weatherContext.riskLevel})</p></div>}
            <form onSubmit={askAssistant} className="flex gap-2"><input value={message} onChange={(e) => setMessage(e.target.value)} placeholder="e.g. Is it safe to travel now?" disabled={!weatherContext || loading} className="flex-1 rounded-xl border px-4 py-3 outline-none focus:ring-2 focus:ring-sky-400 disabled:bg-gray-100" /><button disabled={loading || !weatherContext || !message.trim()} className="rounded-xl bg-sky-600 text-white px-5 py-3 disabled:opacity-60">{loading ? <Loader2 className="w-5 h-5 animate-spin" /> : <Send className="w-5 h-5" />}</button></form>
            <div className="flex flex-wrap gap-2 mt-4">{["Will it rain today?", "Is it safe to travel?", "Should I irrigate?"].map((p) => <button key={p} onClick={() => setMessage(p)} className="rounded-full bg-gray-100 px-3 py-2 text-sm">{p}</button>)}</div>
            {error && <div className="mt-6 rounded-xl bg-red-50 border border-red-200 p-4 text-red-700">{error}</div>}
            {answer && <div className="mt-6 rounded-xl bg-gray-50 border p-5 whitespace-pre-wrap">{answer}</div>}
          </div>
        </section>
      </div>
    </main>
  )
}
