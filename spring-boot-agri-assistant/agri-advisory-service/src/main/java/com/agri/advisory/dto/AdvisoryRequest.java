package com.agri.advisory.dto;

/** Input payload for POST /api/advisory/process. */
public class AdvisoryRequest {

    private String query;
    private String district;

    public AdvisoryRequest() {
    }

    public AdvisoryRequest(String query, String district) {
        this.query = query;
        this.district = district;
    }

    public String getQuery() {
        return query;
    }

    public void setQuery(String query) {
        this.query = query;
    }

    public String getDistrict() {
        return district;
    }

    public void setDistrict(String district) {
        this.district = district;
    }
}
