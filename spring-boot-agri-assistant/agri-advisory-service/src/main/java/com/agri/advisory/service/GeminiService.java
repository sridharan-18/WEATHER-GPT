package com.agri.advisory.service;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.util.UriComponentsBuilder;

import java.net.URI;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Thin Gemini API client (REST) for grounded answer generation.
 *
 * <p>Spring AI is not included as a dependency (to keep the PoC build light and
 * build-fast), so we call the Gemini API directly and only *if* a real API key
 * is present. When no key is configured, the controller falls back to a
 * deterministic source-cited answer, so the service still returns a valid
 * JSON payload.</p>
 */
@Service
public class GeminiService {

    private final RestTemplate restTemplate = new RestTemplate();

    @Value("${spring.ai.gemini.api-key:}")
    private String apiKey;

    @Value("${ai.studio.api.base-url:https://generativelanguage.googleapis.com/v1beta}")
    private String baseUrl;

    /** Ask Gemini to produce an answer from the retrieved knowledge + weather. */
    public String askGemini(String prompt) {
        if (apiKey.isBlank()) {
            return "I cannot call the LLM here. Please check GEMINI_API_KEY.";
        }

        try {
            URI uri = UriComponentsBuilder.fromHttpUrl(baseUrl + "/models/gemini-2.0-flash:generateContent")
                    .queryParam("key", apiKey)
                    .build().toUri();

            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            Map<String, Object> body = new HashMap<>();
            Map<String, Object> content = new HashMap<>();
            Map<String, Object> part = new HashMap<>();
            part.put("text", prompt);
            content.put("parts", new Object[] { part });
            body.put("contents", new Object[] { content });

            HttpEntity<Map<String, Object>> request = new HttpEntity<>(body, headers);

            ResponseEntity<Map> resp = restTemplate.exchange(uri, HttpMethod.POST, request, Map.class);
            Object bodyObj = resp.getBody();
            if (bodyObj == null) {
                return "Gemini returned empty body.";
            }
            Map<String, Object> bodyMap = (Map<String, Object>) bodyObj;
            List<?> candidates = (List<?>) bodyMap.get("candidates");
            if (candidates == null || candidates.isEmpty()) {
                return "No candidates from Gemini.";
            }
            Map<String, Object> first = (Map<String, Object>) candidates.get(0);
            Map<String, Object> parts = (Map<String, Object>) first.get("parts");
            if (parts == null) {
                return "Empty parts in Gemini response.";
            }
            List<?> texts = (List<?>) parts.get("text");
            if (texts == null || texts.isEmpty()) {
                return "No text in Gemini parts.";
            }
            return (String) texts.get(0);
        } catch (Exception e) {
            return "Gemini call failed: " + e.getClass().getSimpleName();
        }
    }

    /** Whether a real Gemini key is configured (for the /health endpoint). */
    public boolean isConfigured() {
        return apiKey != null && !apiKey.isBlank();
    }
}
