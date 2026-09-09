import { NextResponse } from "next/server"

interface AssistantRequest {
  message?: string
  weather?: {
    location?: string
    temperature?: number
    humidity?: number
    windSpeed?: number
    rainProbability?: number
    condition?: string
    riskScore?: number
    riskLevel?: string
  }
}

export async function POST(request: Request) {
  try {
    const body = (await request.json()) as AssistantRequest
    const message = body.message?.trim()

    if (!message) {
      return NextResponse.json({ error: "Message is required" }, { status: 400 })
    }

    const apiKey = process.env.OPENAI_API_KEY
    if (!apiKey) {
      return NextResponse.json(
        { error: "AI assistant is not configured. Add OPENAI_API_KEY to .env.local." },
        { status: 503 },
      )
    }

    const weather = body.weather ?? {}
    const context = JSON.stringify(weather)
    const systemPrompt = `You are WeatherGPT, a safety-focused weather decision assistant. Use the supplied live weather context to answer the user's question. Be concise, practical, and explain the main weather factor behind your advice. Never invent weather values. If the data is insufficient, say so. Do not present the app's safety score as an official government warning. Weather context: ${context}`

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
