package com.agri.advisory.service;

import org.springframework.stereotype.Service;

/**
 * Language identification using Unicode block ranges (no heavy NLP lib).
 * Hardcoded as requested for the PoC, with a keyword fallback to separate
 * Hindi from Marathi inside the Devanagari block.
 */
@Service
public class LanguageDetector {

    // Unicode block ranges for the 7 supported languages
    private static final String TAMIL_RANGE = "TAMIL";
    private static final String TELUGU_RANGE = "TELUGU";
    private static final String KANNADA_RANGE = "KANNADA";
    private static final String MALAYALAM_RANGE = "MALAYALAM";
    private static final String DEVANAGARI_RANGE = "DEVANAGARI";

    /** Set of keyword hints inside Devanagari used to split Hindi / Marathi. */
    private static final String[] HINDI_HINTS = {"kheti", "ped", "haal", "beemaar", "tyohar", "paryavaran"};
    private static final String[] MARATHI_HINTS = {"kheti", "ped", "bahet", "kheti", "dyar", "kharel"};

    /**
     * Detect the language of the user query.
     * @return one of EN / TAMIL / TELUGU / KANNADA / MALAYALAM / HINDI / MARATHI
     */
    public String detectLanguage(String text) {
        if (text == null || text.isBlank()) {
            return "EN";
        }
        String lower = text.toLowerCase();

        // Scan by Unicode code point so supplementary characters are handled correctly
        for (int i = 0; i < text.length(); ) {
            int codePoint = text.codePointAt(i);
            if (isInRange(codePoint, 0x0B80, 0x0BFF)) {
                return TAMIL_RANGE;
            }
            if (isInRange(codePoint, 0x0C00, 0x0C7F)) {
                return TELUGU_RANGE;
            }
            if (isInRange(codePoint, 0x0C80, 0x0CFF)) {
                return KANNADA_RANGE;
            }
            if (isInRange(codePoint, 0x0D00, 0x0D7F)) {
                return MALAYALAM_RANGE;
            }
            if (isInRange(codePoint, 0x0900, 0x097F)) {
                return detectHindiOrMarathi(lower);
            }
            i += Character.charCount(codePoint);
        }
        return "EN";
    }

    private boolean isInRange(int cp, int lo, int hi) {
        return cp >= lo && cp <= hi;
    }

    /** Simple keyword fallback to distinguish Hindi from Marathi. */
    private String detectHindiOrMarathi(String lower) {
        for (String h : HINDI_HINTS) {
            if (lower.contains(h)) {
                return "HINDI";
            }
        }
        for (String m : MARATHI_HINTS) {
            if (lower.contains(m)) {
                return "MARATHI";
            }
        }
        // Without a hint we default to Hindi (Devanagari covers both)
        return "HINDI";
    }
}
