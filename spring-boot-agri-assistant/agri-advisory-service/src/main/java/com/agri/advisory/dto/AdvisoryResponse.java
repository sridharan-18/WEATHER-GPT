package com.agri.advisory.dto;

import com.fasterxml.jackson.annotation.JsonProperty;

/** Structured JSON payload returned by POST /api/advisory/process. */
public class AdvisoryResponse {

    private String detectedLanguage;
    private String answer;
    private String[] sources;

    private AdvisoryResponse() {
    }

    public AdvisoryResponse(String detectedLanguage, String answer, String... sources) {
        this.detectedLanguage = detectedLanguage;
        this.answer = answer;
        this.sources = sources;
    }

    @JsonProperty("detectedLanguage")
    public String getDetectedLanguage() {
        return detectedLanguage;
    }

    public void setDetectedLanguage(String detectedLanguage) {
        this.detectedLanguage = detectedLanguage;
    }

    @JsonProperty("answer")
    public String getAnswer() {
        return answer;
    }

    public void setAnswer(String answer) {
        this.answer = answer;
    }

    @JsonProperty("sources")
    public String[] getSources() {
        return sources;
    }

    public void setSources(String[] sources) {
        this.sources = sources;
    }
}
