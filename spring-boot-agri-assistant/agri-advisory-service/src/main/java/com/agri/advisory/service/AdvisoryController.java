package com.agri.advisory.service;

import com.agri.advisory.dto.AdvisoryRequest;
import com.agri.advisory.dto.AdvisoryResponse;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;

import java.util.Arrays;
import java.util.Map;

/** REST controller for the Agri Advisory Microservice (port 8081). */
@RestController
@RequestMapping("/api/advisory")
public class AdvisoryController {

    private final LanguageDetector languageDetector = new LanguageDetector();
    private final AgroKnowledgeMatrix knowledge = new AgroKnowledgeMatrix();
    private final WeatherService weather = new WeatherService();
    private final GeminiService gemini = new GeminiService();

    /** POST /api/advisory/process  { "query": "...", "district": "..." } */
    public AdvisoryResponse process(@RequestBody AdvisoryRequest req) {
        String query = req.getQuery();
        String district = req.getDistrict();

        // 1) Language identification
        String language = languageDetector.detectLanguage(query);

        // 2) Grounded knowledge retrieval (Source 1: Agro matrix)
        String cropHint = detectCropHint(query);
        String answer = knowledge.getAdvice(cropHint, district, language);

        // 3) Source 2: hyperlocal weather
        Map<String, Object> w = weather.getWeather(district);
        answer += " Latest weather for " + district + ": " + w.get("temperature")
                + ", " + w.get("rainfall") + ", " + w.get("sky") + ".";

        // 4) Gemini rewrite (only when a real key is configured)
        if (gemini.isConfigured()) {
            String prompt = "You are an agricultural assistant. The user's query was in "
                    + language + ". Here is what the knowledge base and hyperlocal weather say. "
                    + "Rewrite the answer in " + language + " so it is short, plain-language, and source-cited. "
                    + "Ground every claim in the provided facts and cite the sources.\n\n"
                    + "Facts from AgroMatrix: " + knowledge.getMatrixSource(language) + "\n"
                    + "Weather: " + w + "\n\nUser query: " + query + "\nAdvisor's draft answer: " + answer;
            answer = gemini.askGemini(prompt);
        }

        String[] sources = new String[] {
                knowledge.getMatrixSource(language),
                "IMD/OpenWeatherMap forecast for " + district
        };

        return new AdvisoryResponse(language, answer, sources);
    }

    /** Simple crop hint extraction from the free-text query. */
    private String detectCropHint(String query) {
        String q = query.toLowerCase();
        String[] crops = {"rice", "wheat", "cotton", "sugarcane", "maize", "groundnut", "chilli", "paddy", "jowar", "bajra"};
        for (String c : crops) {
            if (q.contains(c)) {
                return c;
            }
        }
        return "rice"; // default fallback
    }

    /** Re-evaluate: this is where the (currently absent) real key path would go. */
    @PostMapping("/health")
    public ResponseEntity<Map<String, Object>> health() {
        Map<String, Object> m = new java.util.HashMap<>();
        m.put("service", "agri-advisory");
        m.put("languageDetection", "native unicode-block detector");
        m.put("sources", 2);
        m.put("geminiConfigured", gemini.isConfigured());
        m.put("weatherFallback", weather.isSimulated());
        return ResponseEntity.ok(m);
    }
}
