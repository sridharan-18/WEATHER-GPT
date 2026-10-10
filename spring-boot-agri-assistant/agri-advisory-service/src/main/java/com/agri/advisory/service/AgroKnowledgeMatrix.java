package com.agri.advisory.service;

import com.agri.advisory.dto.AdvisoryResponse;
import org.springframework.stereotype.Service;

/**
 * In-memory "Agro Knowledge Matrix" used as Source 1 of the PoC.
 * Plain-text advisory rules per language, so the answer is grounded in
 * curated data rather than a free-form hallucination.
 */
@Service
public class AgroKnowledgeMatrix {

    // TODO: expand crop list for round 2 (add more crops + district coverage)
    // TODO: load a real agronomy PDF/CSV in a later round

    /** Map: crop -> advice text. */
    private static final String[][] CROPS = {
            {"rice", "Rice grows well in clay-rich soil with 100-150 cm of rainfall. Sow in the kharif season."},
            {"wheat", "Wheat needs cool weather and 50-75 cm of rain. Plant in the rabi season with well-drained soil."},
            {"cotton", "Cotton requires hot, dry days and 50-100 cm of rain. Plant in the kharif season."},
            {"sugarcane", "Sugarcane needs 150-250 cm of rain, deep soil, and warm temperatures."},
            {"maize", "Maize wants 50-100 cm of rain and a warm, frost-free period."},
            {"groundnut", "Groundnut grows best in light, sandy-loam soil with 40-60 cm of rain."},
            {"chilli", "Chilli needs warm weather, 70-100 cm of rain, and plenty of sun."}
    };

    /** Map: crop -> common pests and control. */
    private static final String[][] PESTS = {
            {"rice", "Rice stem borer -> use pheromone traps; leaf folder -> spray neem oil."},
            {"wheat", "Hessian fly -> grow resistant varieties; aphids -> use insecticidal soap."},
            {"cotton", "Bollworm -> apply Bt spray; aphids -> introduce ladybird beetles."},
            {"sugarcane", "Shot borer -> prune and destroy infested parts; red rot -> use certified setts."},
            {"maize", "Fall armyworm -> use pheromone traps; stem borer -> plough field after harvest."}
    };

    /** Map: crop -> seasonal advice. */
    private static final String[][] SEASONAL = {
            {"rice", "Kharif season - sow after the first pre-monsoon showers."},
            {"wheat", "Rabi season - sow in November-December for a March harvest."},
            {"cotton", "Kharif season - plant after the monsoon onset."},
            {"sugarcane", "Kharif season - plant setts in March-April."},
            {"groundnut", "Rabon/Kharif - sow after the initial rains."}
    };

    /** Look up an entry in a matrix (case-insensitive). */
    private String lookup(String[][] matrix, String key) {
        String k = key.toLowerCase();
        for (String[] row : matrix) {
            if (row[0].equalsIgnoreCase(k)) {
                return row[1];
            }
        }
        return null;
    }

    /** Simple advisory: crop + optional district/weather context. */
    public String getAdvice(String crop, String district, String language) {
        String advice = lookup(CROPS, crop);
        if (advice == null) {
            advice = "I don't have a specific advisory for '" + crop + "' yet. Try rice, wheat, cotton, sugarcane, maize, groundnut, or chilli.";
        }
        advice += " For " + (district != null && !district.isBlank() ? district : "the region") + ", check the hyperlocal weather and soil test before planting.";
        return adviseInLanguage(advice, language);
    }

    private String adviseInLanguage(String text, String language) {
        if ("TAMIL".equals(language)) {
            return "[தமிழில்] " + text;
        }
        if ("TELUGU".equals(language)) {
            return "[తెలుగులో] " + text;
        }
        if ("KANNADA".equals(language)) {
            return "[ಕನ್ನಡದಲ್ಲಿ] " + text;
        }
        if ("MALAYALAM".equals(language)) {
            return "[മലയാളത്തിൽ] " + text;
        }
        if ("MARATHI".equals(language)) {
            return "[मराठीत] " + text;
        }
        return text; // English
    }

    /** Return the source reference for the knowledge matrix. */
    public String getMatrixSource(String language) {
        if ("TAMIL".equals(language)) return "AgroMatrix (Tamil)";
        if ("TELUGU".equals(language)) return "AgroMatrix (Telugu)";
        if ("KANNADA".equals(language)) return "AgroMatrix (Kannada)";
        if ("MALAYALAM".equals(language)) return "AgroMatrix (Malayalam)";
        if ("MARATHI".equals(language)) return "AgroMatrix (Marathi)";
        return "AgroMatrix (crop advisory rules): ICAR crop practices";
    }
}
