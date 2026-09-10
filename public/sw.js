self.addEventListener("push", (event) => {
  const data = event.data ? event.data.json() : { title: "WeatherGPT alert", body: "New weather risk detected." }
  event.waitUntil(self.registration.showNotification(data.title, {
    body: data.body,
    icon: "/icon.svg",
    badge: "/icon.svg",
    tag: data.tag || "weathergpt-alert",
  }))
})

self.addEventListener("notificationclick", (event) => {
  event.notification.close()
  event.waitUntil(clients.openWindow("/"))
})
