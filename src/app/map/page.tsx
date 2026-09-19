"use client"

import dynamic from "next/dynamic"
import Link from "next/link"
import { ArrowLeft } from "lucide-react"

const WeatherMap = dynamic(() => import("@/components/WeatherMap"), { ssr: false })

export default function MapPage() {
  return (
    <main className="min-h-screen bg-sky-50 p-6 md:p-10">
      <div className="max-w-6xl mx-auto">
        <Link href="/" className="inline-flex items-center gap-2 text-sky-700 hover:text-sky-900 mb-6">
          <ArrowLeft className="w-4 h-4" /> Back to WeatherGPT
        </Link>
        <div className="bg-white rounded-2xl shadow-lg p-6">
          <h1 className="text-3xl font-bold text-gray-900">Weather Hazard Map</h1>
          <p className="text-gray-600 mt-2 mb-6">Interactive map for the default Coimbatore location. The main dashboard will connect this map to its live location in the next UI integration commit.</p>
          <WeatherMap latitude={11.0168} longitude={76.9558} score={75} label="Coimbatore, India" />
        </div>
      </div>
    </main>
  )
}
