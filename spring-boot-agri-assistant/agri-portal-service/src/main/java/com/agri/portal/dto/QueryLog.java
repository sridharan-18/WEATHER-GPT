package com.agri.portal.dto;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import java.time.LocalDateTime;

/** JPA entity: one row per farmer question logged in H2. */
@Entity
public class QueryLog {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private String userQuery;
    private String district;
    private String detectedLanguage;
    private String aiResponse;
    private String[] sources;
    private LocalDateTime createdTime;

    /** Default constructor (required by JPA). */
    public QueryLog() {
    }

    /** Parameterized constructor. */
    public QueryLog(String userQuery, String district, String detectedLanguage,
                    String aiResponse, String[] sources) {
        this.userQuery = userQuery;
        this.district = district;
        this.detectedLanguage = detectedLanguage;
        this.aiResponse = aiResponse;
        this.sources = sources;
        this.createdTime = LocalDateTime.now();
    }

    // --- getters & setters ---

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getUserQuery() {
        return userQuery;
    }

    public void setUserQuery(String userQuery) {
        this.userQuery = userQuery;
    }

    public String getDistrict() {
        return district;
    }

    public void setDistrict(String district) {
        this.district = district;
    }

    public String getDetectedLanguage() {
        return detectedLanguage;
    }

    public void setDetectedLanguage(String detectedLanguage) {
        this.detectedLanguage = detectedLanguage;
    }

    public String getAiResponse() {
        return aiResponse;
    }

    public void setAiResponse(String aiResponse) {
        this.aiResponse = aiResponse;
    }

    public String[] getSources() {
        return sources;
    }

    public void setSources(String[] sources) {
        this.sources = sources;
    }

    public LocalDateTime getCreatedTime() {
        return createdTime;
    }

    public void setCreatedTime(LocalDateTime createdTime) {
        this.createdTime = createdTime;
    }
}
