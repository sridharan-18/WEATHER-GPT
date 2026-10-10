package com.agri.portal.service;

import com.agri.portal.dto.QueryLog;
import com.agri.portal.repository.QueryLogRepository;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.Arrays;
import java.util.List;

/** Calls the advisory microservice, logs history, and returns the response + sources. */
@Service
public class PortalService {

    private final QueryLogRepository repository;
    private final RestTemplate restTemplate = new RestTemplate();

    @Value("${advisory.base-url:http://localhost:8081/api/advisory/process}")
    private String advisoryUrl;

    public PortalService(QueryLogRepository repository) {
        this.repository = repository;
    }

    /** Save a query log entry to H2. */
    public void save(QueryLog log) {
        repository.save(log);
    }

    /** Return all stored query logs. */
    public List<QueryLog> findAll() {
        return repository.findAll();
    }

    /**
     * POST the farmer's question to Microservice 2 and return
     * [{aiResponse}, {sources}].
     */
    public String[] callAdvisory(String query, String district) {
        // Build a raw JSON payload and let the advisory service parse it.
        // No cross-module DTO dependency: we just send {query, district}.
        String json = String.format("{\"query\":\"%s\",\"district\":\"%s\"}", query, district);
        String response = restTemplate.postForObject(advisoryUrl, json, String.class);
        if (response == null || response.isBlank()) {
            return new String[] { "Advisory service did not respond. Is it running on port 8081?", "" };
        }
        // Minimal parse: { "detectedLanguage": "...", "answer": "...", "sources": [...] }
        String answer = extract(response, "answer");
        String sources = extract(response, "sources");
        // sources is JSON-encoded; collapse it to readable text
        if (sources != null && sources.startsWith("[") && sources.endsWith("]")) {
            sources = sources.substring(1, sources.length() - 1).replaceAll("\"", "").replaceAll("\\s+", " ");
        }
        return new String[] { answer, sources };
    }

    private String extract(String json, String key) {
        String search = "\"" + key + "\":";
        int idx = json.indexOf(search);
        if (idx == -1) {
            return "";
        }
        idx += search.length();
        if (json.charAt(idx) == '"') {
            int end = json.indexOf('"', idx + 1);
            return json.substring(idx + 1, end);
        }
        // Array: find the outer brackets and strip them, keep the raw elements
        if (json.charAt(idx) == '[') {
            int depth = 0;
            int end = idx;
            while (end < json.length()) {
                if (json.charAt(end) == '[') depth++;
                if (json.charAt(end) == ']') { depth--; if (depth == 0) break; }
                end++;
            }
            // return elements joined by a single space (already de-quoted by caller)
            return json.substring(idx + 1, end).replaceAll("\"", "").replaceAll("\\s+", " ");
        }
        int end = json.indexOf(",", idx);
        if (end == -1) {
            end = json.indexOf("}", idx);
        }
        return json.substring(idx, end).trim();
    }

    /** Language detection (reuses the same unicode-block logic as the advisory service). */
    public String detectLanguage(String text) {
        if (text == null || text.isBlank()) {
            return "EN";
        }
        String lower = text.toLowerCase();
        for (int i = 0; i < text.length(); ) {
            int cp = text.codePointAt(i);
            if (cp >= 0x0B80 && cp <= 0x0BFF) {
                return "TAMIL";
            }
            if (cp >= 0x0C00 && cp <= 0x0C7F) {
                return "TELUGU";
            }
            if (cp >= 0x0C80 && cp <= 0x0CFF) {
                return "KANNADA";
            }
            if (cp >= 0x0D00 && cp <= 0x0D7F) {
                return "MALAYALAM";
            }
            if (cp >= 0x0900 && cp <= 0x097F) {
                return detectHindiOrMarathi(lower);
            }
            i += Character.charCount(cp);
        }
        return "EN";
    }

    private String detectHindiOrMarathi(String lower) {
        String[] hindi = {"kheti", "ped", "haal", "beemaar", "tyohar", "paryavaran"};
        String[] marathi = {"bahet", "dyar", "kharel", "khared"};
        for (String h : hindi) { if (lower.contains(h)) return "HINDI"; }
        for (String m : marathi) { if (lower.contains(m)) return "MARATHI"; }
        return "HINDI";
    }
}
