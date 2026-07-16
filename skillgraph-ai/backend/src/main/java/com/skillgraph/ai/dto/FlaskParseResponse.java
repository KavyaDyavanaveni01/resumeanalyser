package com.skillgraph.ai.dto;

import java.util.List;
import java.util.Map;

public class FlaskParseResponse {
    private Double match_percentage;
    private String parsed_text;
    private List<String> extracted_skills;
    private List<String> missing_skills;
    private List<Map<String, Object>> learning_roadmap;
    private List<Map<String, Object>> certifications;

    // Getters and Setters
    public Double getMatch_percentage() {
        return match_percentage;
    }

    public void setMatch_percentage(Double match_percentage) {
        this.match_percentage = match_percentage;
    }

    public String getParsed_text() {
        return parsed_text;
    }

    public void setParsed_text(String parsed_text) {
        this.parsed_text = parsed_text;
    }

    public List<String> getExtracted_skills() {
        return extracted_skills;
    }

    public void setExtracted_skills(List<String> extracted_skills) {
        this.extracted_skills = extracted_skills;
    }

    public List<String> getMissing_skills() {
        return missing_skills;
    }

    public void setMissing_skills(List<String> missing_skills) {
        this.missing_skills = missing_skills;
    }

    public List<Map<String, Object>> getLearning_roadmap() {
        return learning_roadmap;
    }

    public void setLearning_roadmap(List<Map<String, Object>> learning_roadmap) {
        this.learning_roadmap = learning_roadmap;
    }

    public List<Map<String, Object>> getCertifications() {
        return certifications;
    }

    public void setCertifications(List<Map<String, Object>> certifications) {
        this.certifications = certifications;
    }
}
