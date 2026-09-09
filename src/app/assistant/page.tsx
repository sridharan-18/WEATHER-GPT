"use client"

import { FormEvent, useState } from "react"
import Link from "next/link"
import { ArrowLeft, Bot, Send } from "lucide-react"

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

const defaultWeather: WeatherContext = {
  location: "Coimbatore, India",
  temperature: 28,
  humidity: 70,
  windSpeed: 12,
  rainProbability: 40,
  condition: "Partly cloudy",
  riskScore: 75,
  riskLevel: "Low Risk",
}

export default function AssistantPage() {
  const [message, setMessage] = useState("")
  const [answer, setAnswer] = useState("")
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")

  async function askAssistant(event: FormEvent) {
    event.preventDefault()
    if (!message.trim()) return

    setLoading(true)
    setError("")
    setAnswer("")

    try {
      const response = await fetch("/api/assistant", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message, weather: defaultWeather }),
      })
      const data = await response.json()
      if (!response.ok) throw new Error(data.error || "Assistant request failed")
      setAnswer(data.answer)
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "Assistant request failed")
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-sky-100 p-6 md:p-10">
      <div className="max-w-3xl mx-auto">
        <Link href="/" className="inline-flex items-center gap-2 text-sky-700 hover:text-sky-900 mb-6">
          <ArrowLeft className="w-4 h-4" /> Back to WeatherGPT
        </Link>

        <section className="bg-white rounded-2xl shadow-lg overflow-hidden">
          <div className="bg-gradient-to-r from-indigo-600 to-sky-600 p-6 text-white">
            <div className="flex items-center gap-3">
              <Bot className="w-8 h-8" />
              <div>
                <h1 className="text-2xl font-bold">WeatherGPT Assistant</h1>
                <p className="text-white/85">Ask weather questions and get action-oriented advice.</p>
              </div>
            </div>
          </div>

          <div className="p-6">
            <div className="rounded-xl bg-sky-50 p-4 mb-6">
              <p className="font-semibold text-gray-900">Current context: {defaultWeather.location}</p>
              <p className="text-sm text-gray-600 mt-1">
                {defaultWeather.temperature}°C · {defaultWeather.condition} · Rain {defaultWeather.rainProbability}% · Wind {defaultWeather.windSpeed} km/h · Risk {defaultWeather.riskScore}/100 ({defaultWeather.riskLevel})
              </p>
            </div>

            <form onSubmit={askAssistant} className="flex gap-2">
              <input
                value={message}
                onChange={(event) => setMessage(event.target.value)}
                placeholder="e.g. Is it safe to travel now?"
                className="flex-1 rounded-xl border border-gray-200 px-4 py-3 outline-none focus:ring-2 focus:ring-sky-400"
              />
              <button disabled={loading} className="rounded-xl bg-sky-600 text-white px-5 py-3 hover:bg-sky-700 disabled:opacity-60">
                <Send className="w-5 h-5" />
              </button>
            </form>

            <div className="flex flex-wrap gap-2 mt-4">
              {["Will it rain today?", "Is it safe to travel?", "Should I irrigate?"].map((prompt) => (
                <button key={prompt} onClick={() => setMessage(prompt)} className="rounded-full bg-gray-100 px-3 py-2 text-sm hover:bg-gray-200">
                  {prompt}
                </button>
              ))}
            </div>

            {loading && <p className="mt-6 text-gray-500">WeatherGPT is thinking...</p>}
            {error && <div className="mt-6 rounded-xl bg-red-50 border border-red-200 p-4 text-red-700">{error}</div>}
            {answer && <div className="mt-6 rounded-xl bg-gray-50 border border-gray-100 p-5 whitespace-pre-wrap text-gray-800">{answer}</div>}
          </div>
        </section>
      </div>
    </main>
  )
}
