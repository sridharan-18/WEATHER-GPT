package com.agri.advisory.service;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.util.UriComponentsBuilder;

import java.net.URI;
import java.util.HashMap;
import java.util.Map;

/**
 * Source 2: Hyperlocal weather data.
 * Consumes the OpenWeatherMap /forecast endpoint by district name (English).
 * Falls back to a deterministic simulated response when no key is configured,
 * so the PoC still runs locally.
 */
@Service
public class WeatherService {

    @Value("${imd.base-url:https://api.openweathermap.org/data/2.5/forecast}")
    private String baseUrl;

    @Value("${imd.api-key:}")
    private String apiKey;

    private final RestTemplate restTemplate = new RestTemplate();

    /** Simulated "real-time" temperature / rain for demo districts (no key needed). */
    private static final Map<String, SimulatedWeather> SIMULATED = new HashMap<>();

    static {
        SIMULATED.put("mumbai", new SimulatedWeather(29.0, 0.0, "partly cloudy, 0 mm rainfall"));
        SIMULATED.put("delhi", new SimulatedWeather(31.0, 0.0, "sunny, 0 mm rainfall"));
        SIMULATED.put("bangalore", new SimulatedWeather(26.0, 0.0, "clear sky, 0 mm rainfall"));
        SIMULATED.put("hyderabad", new SimulatedWeather(30.5, 0.0, "partly cloudy, 0 mm rainfall"));
        SIMULATED.put("chennai", new SimulatedWeather(32.0, 1.2, "slight chance of noon showers"));
        SIMULATED.put("kolkata", new SimulatedWeather(28.0, 0.0, "humid, light winds"));
        SIMULATED.put("pune", new SimulatedWeather(27.0, 0.0, "dry, sunny"));
        SIMULATED.put("ahmedabad", new SimulatedWeather(33.0, 0.0, "hot and dry"));
    }

    /** Simple data class holding one simulated forecast. */
    private static class SimulatedWeather {
        final double tempCelsius;
        final double rainMm;
        final String sky;

        SimulatedWeather(double tempCelsius, double rainMm, String sky) {
            this.tempCelsius = tempCelsius;
            this.rainMm = rainMm;
            this.sky = sky;
        }
    }

    /** Look up a district's weather by name (English). */
    public Map<String, Object> getWeather(String district) {
        String key = district.trim().isEmpty() ? "" : district.trim().toLowerCase();

        // 1) Simulated response when no API key is present
        if (apiKey.isBlank()) {
            SimulatedWeather s = SIMULATED.get(key);
            if (s != null) {
                return weatherMap("simulated", s.tempCelsius, s.rainMm, s.sky, "IMD (simulated: no API key configured)");
            }
            return weatherMap("simulated", 28.0, 0.0, "largely dry", "IMD (simulated fallback for unknown district)");
        }

        // 2) Real IMD/OpenWeatherMap call when a key is present
        try {
            URI uri = UriComponentsBuilder.fromHttpUrl(baseUrl + "?q={q}&appid={key}&units=metric&cnt=5")
                    .build(key, apiKey);
            String json = restTemplate.getForObject(uri, String.class);
            return parseWeather(json, district);
        } catch (Exception e) {
            // Graceful degradation: simulated data if the real API fails
            SimulatedWeather s = SIMULATED.get(key);
            if (s != null) {
                return weatherMap("simulated", s.tempCelsius, s.rainMm, s.sky, "IMD (simulated after API error: " + e.getClass().getSimpleName() + ")");
            }
            return weatherMap("simulated", 28.0, 0.0, "largely dry", "IMD (simulated fallback after API error)");
        }
    }

    private Map<String, Object> parseWeather(String json, String district) {
        // The API returns a forecast; take the first entry's main.weather[0].
        // Keep this PoC-friendly: no external JSON parser dependency.
        String temp = extract(json, "main.temp");
        String humidity = extract(json, "main.humidity");
        String weather = extract(json, "weather[0].description");
        String rain = extract(json, "rain");

        Map<String, Object> m = new java.util.HashMap<>();
        m.put("district", district);
        m.put("temperature", temp);
        m.put("humidity", humidity);
        m.put("sky", weather);
        m.put("rain_mm", rain);
        m.put("source", "IMD OpenWeatherMap forecast API: " + district);
        return m;
    }

    private Map<String, Object> weatherMap(String src, double temp, double rain, String sky, String detail) {
        Map<String, Object> m = new java.util.HashMap<>();
        m.put("district", "unknown");
        m.put("temperature", String.format("%.1f C", temp));
        m.put("rainfall", rain + " mm");
        m.put("sky", sky);
        m.put("source", detail);
        return m;
    }

    /** Minimal helper to pull a dotted JSON path without a parser (PoC only). */
    private String extract(String json, String path) {
        if (json == null || !json.contains(path)) {
            return "n/a";
        }
        int start = json.indexOf(path) + path.length() + 2; // past the quoted key
        int end = json.indexOf("\"", start);
        return json.substring(start, end);
    }

    /** Whether the service is using simulated data (no real API key configured). */
    public boolean isSimulated() {
        return apiKey == null || apiKey.isBlank();
    }
}
