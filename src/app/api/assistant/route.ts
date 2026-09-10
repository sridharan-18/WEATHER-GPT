import { NextResponse } from "next/server"

interface AssistantRequest {
  message?: string
  mode?: string
  weather?: {
    location?: string
    temperature?: number
    humidity?: number
    windSpeed?: number
    rainProbability?: number
    condition?: string
    riskScore?: number
    riskLevel?: string
    hazards?: Array<{ label?: string; probability?: number | null; detail?: string }>
  }
}

function fallbackAnswer(message: string, mode: string, weather: NonNullable<AssistantRequest["weather"]>) {
  const rain = weather.rainProbability ?? 0
  const wind = weather.windSpeed ?? 0
  const temp = weather.temperature ?? 0
  const modeLabel = mode || "citizen"
  const advice = modeLabel === "farmer"
    ? rain >= 60 ? "Avoid spraying or irrigating immediately before rain. Work early and recheck the next forecast." : "Conditions are suitable for routine field work; keep monitoring rain before spraying."
    : modeLabel === "fisherman"
      ? wind >= 30 || rain >= 70 ? "Avoid exposed water and check an official marine warning before departure." : "Weather signals are currently moderate for a short trip; check the official marine bulletin first."
      : modeLabel === "disaster-management"
        ? rain >= 70 || wind >= 40 ? "Escalate monitoring, verify local warnings, and prepare response teams for weather impacts." : "No strong weather escalation signal is present in this forecast snapshot."
        : rain >= 60 ? "Carry rain protection and consider postponing exposed outdoor plans." : "No major rain signal is present in the current forecast window."

  return `Mode: ${modeLabel}\n\nBased on the live context: ${Math.round(temp)}°C, rain ${rain}%, wind ${Math.round(wind)} km/h, risk ${weather.riskScore ?? "unknown"}/100.\n\nRecommendation:\n${advice}\n\nThis is a rule-based fallback using the supplied weather data. It is not an official warning.`
}

export async function POST(request: Request) {
  try {
    const body = (await request.json()) as AssistantRequest
    const message = body.message?.trim()

    if (!message) {
      return NextResponse.json({ error: "Message is required" }, { status: 400 })
    }

    const apiKey = process.env.OPENAI_API_KEY
    const weather = body.weather ?? {}
    if (!apiKey) {
      return NextResponse.json({ answer: fallbackAnswer(message, body.mode ?? "citizen", weather), fallback: true })
    }

    const context = JSON.stringify(weather)
    const systemPrompt = `You are WeatherGPT, a safety-focused weather decision assistant for the ${body.mode ?? "citizen"} mode. Use only the supplied live weather context to answer the user's question. Be concise, practical, and explain the main weather factor behind your advice. Never invent weather values or probabilities. If earthquake, volcano, or tsunami data is unavailable, say that no connected warning feed can assess it. Do not present the app's safety score as an official government warning. Weather context: ${context}`

    const response = await fetch("https://api.openai.com/v1/responses", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${apiKey}`,
      },
      body: JSON.stringify({
        model: process.env.OPENAI_MODEL || "gpt-5.6-luna",
        input: [
          { role: "system", content: systemPrompt },
          { role: "user", content: message },
        ],
      }),
    })

    if (!response.ok) {
      const details = await response.text()
      console.error("OpenAI API error:", details)
      return NextResponse.json({ error: "AI service request failed" }, { status: 502 })
    }

    const data = await response.json()
    const answer = data.output_text || data.output?.flatMap((item: { content?: Array<{ text?: string }> }) => item.content ?? []).map((item: { text?: string }) => item.text).filter(Boolean).join("\n")

    return NextResponse.json({ answer: answer || "I could not generate an answer from the current weather data." })
  } catch {
    return NextResponse.json({ error: "Unable to process the assistant request" }, { status: 500 })
  }
}
