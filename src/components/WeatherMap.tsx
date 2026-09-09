"use client"

import "leaflet/dist/leaflet.css"
import L from "leaflet"
import { useEffect } from "react"
import { Circle, MapContainer, Marker, Popup, TileLayer, useMap } from "react-leaflet"

interface WeatherMapProps {
  latitude: number
  longitude: number
  score: number
  label: string
}

function MapCenter({ latitude, longitude }: { latitude: number; longitude: number }) {
  const map = useMap()

  useEffect(() => {
    map.setView([latitude, longitude], 10)
  }, [latitude, longitude, map])

  return null
}

const markerIcon = L.divIcon({
  className: "weathergpt-marker",
  html: '<div style="width:18px;height:18px;border-radius:50%;background:#0284c7;border:3px solid white;box-shadow:0 2px 8px rgba(0,0,0,.35)"></div>',
  iconSize: [18, 18],
  iconAnchor: [9, 9],
})

export default function WeatherMap({ latitude, longitude, score, label }: WeatherMapProps) {
  const radius = Math.max(8000, Math.round((100 - score + 1) * 350))

  return (
    <div className="h-[420px] overflow-hidden rounded-xl">
      <MapContainer center={[latitude, longitude]} zoom={10} scrollWheelZoom className="h-full w-full">
        <TileLayer
          attribution='&copy; OpenStreetMap contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        <MapCenter latitude={latitude} longitude={longitude} />
        <Marker position={[latitude, longitude]} icon={markerIcon}>
          <Popup>
            <strong>{label}</strong>
            <br />Weather safety score: {score}/100
          </Popup>
        </Marker>
        <Circle
          center={[latitude, longitude]}
          radius={radius}
          pathOptions={{ color: score < 40 ? "#dc2626" : score < 60 ? "#f59e0b" : "#0284c7", fillOpacity: 0.12 }}
        />
      </MapContainer>
    </div>
  )
}
