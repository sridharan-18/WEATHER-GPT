"use client"

import { Bell, BellRing, Moon, Sun } from "lucide-react"
import { useEffect, useState } from "react"
import type { HazardScore } from "@/lib/risk"

interface WeatherControlsProps {
  hazards?: HazardScore[]
  location?: string
}

export default function WeatherControls({ hazards = [], location = "your location" }: WeatherControlsProps) {
  const [dark, setDark] = useState(false)
  const [permission, setPermission] = useState<NotificationPermission | "unsupported">("default")

  useEffect(() => {
    const saved = window.localStorage.getItem("weathergpt-theme")
    const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches
    const enabled = saved ? saved === "dark" : prefersDark
    document.documentElement.classList.toggle("dark", enabled)
    setDark(enabled)
    setPermission("Notification" in window ? Notification.permission : "unsupported")
    if ("serviceWorker" in navigator) void navigator.serviceWorker.register("/sw.js")
  }, [])

  useEffect(() => {
    if (permission !== "granted") return
    const urgent = hazards.find((hazard) => hazard.score >= 75)
    if (!urgent) return
    const key = `weathergpt-alert:${location}:${urgent.key}:${urgent.score}`
    if (window.sessionStorage.getItem(key)) return
    window.sessionStorage.setItem(key, "sent")
    new Notification(`WeatherGPT: ${urgent.label} risk`, {
      body: `${urgent.detail}. ${urgent.action}`,
      tag: `weathergpt-${urgent.key}`,
      icon: "/icon.svg",
    })
  }, [hazards, location, permission])

  function toggleTheme() {
    const next = !dark
    document.documentElement.classList.toggle("dark", next)
    window.localStorage.setItem("weathergpt-theme", next ? "dark" : "light")
    setDark(next)
  }

  async function enableAlerts() {
    if (!("Notification" in window)) {
      setPermission("unsupported")
      return
    }
    const next = await Notification.requestPermission()
    setPermission(next)
  }

  return (
    <div className="flex items-center gap-2">
      <button onClick={toggleTheme} className="control-button" title={dark ? "Use light mode" : "Use dark mode"} aria-label={dark ? "Use light mode" : "Use dark mode"}>
        {dark ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
      </button>
      <button onClick={() => void enableAlerts()} className={`control-button ${permission === "granted" ? "control-button-active" : ""}`} title={permission === "granted" ? "Weather alerts enabled" : "Enable weather alerts"} aria-label="Enable weather alerts">
        {permission === "granted" ? <BellRing className="w-4 h-4" /> : <Bell className="w-4 h-4" />}
      </button>
    </div>
  )
}
