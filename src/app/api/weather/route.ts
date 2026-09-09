import { NextRequest, NextResponse } from "next/server"

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url)
  const latitude = searchParams.get("latitude")
  const longitude = searchParams.get("longitude")
  if (!latitude || !longitude) return NextResponse.json({ error: "latitude and longitude are required" }, { status: 400 })

  const params = new URLSearchParams({
    latitude,
    longitude,
    timezone: "auto",
    forecast_days: "7",
    current: "temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,pressure_msl,wind_speed_10m,wind_gusts_10m,visibility,uv_index,weather_code",
    hourly: "temperature_2m,precipitation_probability,precipitation,wind_speed_10m,visibility,weather_code",
    daily: "temperature_2m_max,temperature_2m_min,precipitation_probability_max,precipitation_sum,wind_speed_10m_max,weather_code",
  })
  const response = await fetch(`https://api.open-meteo.com/v1/forecast?${params}`, { next: { revalidate: 300 } })
  if (!response.ok) return NextResponse.json({ error: "Weather provider unavailable" }, { status: 502 })
  return NextResponse.json(await response.json())
}
