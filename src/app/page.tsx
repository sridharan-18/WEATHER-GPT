"use client"

import { useState, useEffect } from "react"
import { Cloud, Thermometer, Wind, Droplets, AlertTriangle, Shield, TrendingUp } from "lucide-react"

interface WeatherData {
  temp: number
  humidity: number
  windSpeed: number
  visibility: number
  condition: string
  safetyScore: number
  riskLevel: string
  hazards: string[]
  forecast: Array<{
    time: string
    score: number
    risk: string
  }>
}

export default function Home() {
  const [weatherData, setWeatherData] = useState<WeatherData | null>(null)
  const [loading, setLoading] = useState(true)
  const [location, setLocation] = useState("San Francisco, CA")

  useEffect(() => {
    // Simulate weather data (replace with actual API call)
    const mockData: WeatherData = {
      temp: 72,
      humidity: 65,
      windSpeed: 12,
      visibility: 10,
      condition: "Partly Cloudy",
      safetyScore: 78,
      riskLevel: "Low Risk",
      hazards: ["Moderate UV Index", "Light Wind"],
      forecast: [
        { time: "Now", score: 78, risk: "Low" },
        { time: "+2h", score: 75, risk: "Low" },
        { time: "+4h", score: 70, risk: "Moderate" },
        { time: "+6h", score: 65, risk: "Moderate" },
        { time: "+8h", score: 60, risk: "Moderate" },
        { time: "+10h", score: 55, risk: "High" },
        { time: "+12h", score: 50, risk: "High" },
      ]
    }
    
    setTimeout(() => {
      setWeatherData(mockData)
      setLoading(false)
    }, 1000)
  }, [])

  const getScoreColor = (score: number) => {
    if (score >= 80) return "text-green-500"
    if (score >= 60) return "text-yellow-500"
    if (score >= 40) return "text-orange-500"
    return "text-red-500"
  }

  const getRiskColor = (risk: string) => {
    if (risk === "Low") return "bg-green-100 text-green-800"
    if (risk === "Moderate") return "bg-yellow-100 text-yellow-800"
    if (risk === "High") return "bg-orange-100 text-orange-800"
    return "bg-red-100 text-red-800"
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100">
        <div className="text-center">
          <Cloud className="w-16 h-16 mx-auto mb-4 text-blue-500 animate-pulse" />
          <p className="text-gray-600">Loading weather data...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4 md:p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-2">
            WeatherGPT
          </h1>
          <p className="text-gray-600 text-lg">Hyperlocal Weather Risk Intelligence</p>
          <div className="mt-4 flex items-center gap-2 text-sm text-gray-500">
            <Cloud className="w-4 h-4" />
            <span>{location}</span>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Weather Safety Score */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-2xl shadow-lg p-6">
              <div className="flex items-center gap-2 mb-4">
                <Shield className="w-6 h-6 text-blue-500" />
                <h2 className="text-xl font-semibold text-gray-900">Weather Safety Score</h2>
              </div>
              
              <div className="text-center py-8">
                <div className={`text-7xl font-bold ${getScoreColor(weatherData!.safetyScore)}`}>
                  {weatherData!.safetyScore}
                </div>
                <div className="text-2xl font-semibold text-gray-700 mt-2">
                  {weatherData!.riskLevel}
                </div>
                <div className="text-sm text-gray-500 mt-1">out of 100</div>
              </div>

              <div className="mt-6">
                <div className="h-3 bg-gray-200 rounded-full overflow-hidden">
                  <div 
                    className={`h-full transition-all duration-500 ${
                      weatherData!.safetyScore >= 80 ? 'bg-green-500' :
                      weatherData!.safetyScore >= 60 ? 'bg-yellow-500' :
                      weatherData!.safetyScore >= 40 ? 'bg-orange-500' : 'bg-red-500'
                    }`}
                    style={{ width: `${weatherData!.safetyScore}%` }}
                  />
                </div>
              </div>
            </div>
          </div>

          {/* Live Conditions */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-2xl shadow-lg p-6 h-full">
              <div className="flex items-center gap-2 mb-4">
                <Cloud className="w-6 h-6 text-blue-500" />
                <h2 className="text-xl font-semibold text-gray-900">Live Conditions</h2>
              </div>
              
              <div className="space-y-4">
                <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div className="flex items-center gap-3">
                    <Thermometer className="w-5 h-5 text-red-500" />
                    <span className="text-gray-700">Temperature</span>
                  </div>
                  <span className="font-semibold text-gray-900">{weatherData!.temp}°F</span>
                </div>
                
                <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div className="flex items-center gap-3">
                    <Droplets className="w-5 h-5 text-blue-500" />
                    <span className="text-gray-700">Humidity</span>
                  </div>
                  <span className="font-semibold text-gray-900">{weatherData!.humidity}%</span>
                </div>
                
                <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div className="flex items-center gap-3">
                    <Wind className="w-5 h-5 text-gray-500" />
                    <span className="text-gray-700">Wind Speed</span>
                  </div>
                  <span className="font-semibold text-gray-900">{weatherData!.windSpeed} mph</span>
                </div>
                
                <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div className="flex items-center gap-3">
                    <Cloud className="w-5 h-5 text-blue-500" />
                    <span className="text-gray-700">Condition</span>
                  </div>
                  <span className="font-semibold text-gray-900">{weatherData!.condition}</span>
                </div>
                
                <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div className="flex items-center gap-3">
                    <TrendingUp className="w-5 h-5 text-green-500" />
                    <span className="text-gray-700">Visibility</span>
                  </div>
                  <span className="font-semibold text-gray-900">{weatherData!.visibility} mi</span>
                </div>
              </div>
            </div>
          </div>

          {/* 12-Hour Risk Forecast */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-2xl shadow-lg p-6 h-full">
              <div className="flex items-center gap-2 mb-4">
                <TrendingUp className="w-6 h-6 text-blue-500" />
                <h2 className="text-xl font-semibold text-gray-900">12-Hour Risk Forecast</h2>
              </div>
              
              <div className="space-y-3">
                {weatherData!.forecast.map((item, index) => (
                  <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                    <span className="text-gray-700 font-medium">{item.time}</span>
                    <div className="flex items-center gap-3">
                      <span className={`font-semibold ${getScoreColor(item.score)}`}>
                        {item.score}
                      </span>
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${getRiskColor(item.risk)}`}>
                        {item.risk}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Hazard Breakdown */}
        <div className="mt-6">
          <div className="bg-white rounded-2xl shadow-lg p-6">
            <div className="flex items-center gap-2 mb-4">
              <AlertTriangle className="w-6 h-6 text-orange-500" />
              <h2 className="text-xl font-semibold text-gray-900">Hazard Breakdown</h2>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              {weatherData!.hazards.map((hazard, index) => (
                <div key={index} className="p-4 bg-orange-50 border border-orange-200 rounded-lg">
                  <div className="flex items-center gap-2 mb-2">
                    <AlertTriangle className="w-5 h-5 text-orange-500" />
                    <span className="font-semibold text-gray-900">Hazard {index + 1}</span>
                  </div>
                  <p className="text-gray-700">{hazard}</p>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Actions for Farmer */}
        <div className="mt-6">
          <div className="bg-white rounded-2xl shadow-lg p-6">
            <div className="flex items-center gap-2 mb-4">
              <Shield className="w-6 h-6 text-green-500" />
              <h2 className="text-xl font-semibold text-gray-900">Actions for Farmer</h2>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              <div className="p-4 bg-green-50 border border-green-200 rounded-lg">
                <h3 className="font-semibold text-gray-900 mb-2">Irrigation</h3>
                <p className="text-gray-700 text-sm">Optimal conditions for irrigation today. Moderate humidity levels support efficient water absorption.</p>
              </div>
              
              <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
                <h3 className="font-semibold text-gray-900 mb-2">Crop Protection</h3>
                <p className="text-gray-700 text-sm">Light winds expected. No immediate threat to crops. Monitor for changes in +8 hours.</p>
              </div>
              
              <div className="p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
                <h3 className="font-semibold text-gray-900 mb-2">Field Work</h3>
                <p className="text-gray-700 text-sm">Good conditions for field work in the next 6 hours. Plan activities accordingly.</p>
              </div>
            </div>
          </div>
        </div>

        {/* Hazard Map Placeholder */}
        <div className="mt-6">
          <div className="bg-white rounded-2xl shadow-lg p-6">
            <div className="flex items-center gap-2 mb-4">
              <Cloud className="w-6 h-6 text-blue-500" />
              <h2 className="text-xl font-semibold text-gray-900">Hazard Map</h2>
            </div>
            
            <div className="bg-gray-100 rounded-lg p-12 text-center">
              <Cloud className="w-16 h-16 mx-auto mb-4 text-gray-400" />
              <p className="text-gray-600 mb-2">Interactive Leaflet tiles arrive in Phase 2</p>
              <p className="text-sm text-gray-500">Real-time hazard mapping coming soon</p>
            </div>
          </div>
        </div>

        {/* WeatherGPT Assistant Placeholder */}
        <div className="mt-6 mb-8">
          <div className="bg-white rounded-2xl shadow-lg p-6">
            <div className="flex items-center gap-2 mb-4">
              <Shield className="w-6 h-6 text-purple-500" />
              <h2 className="text-xl font-semibold text-gray-900">WeatherGPT Assistant</h2>
            </div>
            
            <div className="bg-gray-100 rounded-lg p-12 text-center">
              <Shield className="w-16 h-16 mx-auto mb-4 text-gray-400" />
              <p className="text-gray-600 mb-2">Conversational intent parsing and explanations connect in Phase 2</p>
              <p className="text-sm text-gray-500">AI-powered weather insights coming soon</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
