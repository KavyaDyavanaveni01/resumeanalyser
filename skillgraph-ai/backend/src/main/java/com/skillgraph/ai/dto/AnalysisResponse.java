package com.skillgraph.ai.dto;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Map;

public class AnalysisResponse {
    private Long id;
    private String careerGoal;
    private Double matchPercentage;
    private String parsedText;
    private List<String> extractedSkills;
    private List<String> missingSkills;
    private List<Map<String, Object>> learningRoadmap;
    private List<Map<String, Object>> certifications;
    private LocalDateTime createdAt;

    // Constructors
    public AnalysisResponse() {}

    public AnalysisResponse(Long id, String careerGoal, Double matchPercentage, String parsedText,
                            List<String> extractedSkills, List<String> missingSkills,
                            List<Map<String, Object>> learningRoadmap, List<Map<String, Object>> certifications,
                            LocalDateTime createdAt) {
        this.id = id;
        this.careerGoal = careerGoal;
        this.matchPercentage = matchPercentage;
        this.parsedText = parsedText;
        this.extractedSkills = extractedSkills;
        this.missingSkills = missingSkills;
        this.learningRoadmap = learningRoadmap;
        this.certifications = certifications;
        this.createdAt = createdAt;
    }

    // Getters and Setters
    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getCareerGoal() {
        return careerGoal;
    }

    public void setCareerGoal(String careerGoal) {
        this.careerGoal = careerGoal;
    }

    public Double getMatchPercentage() {
        return matchPercentage;
    }

    public void setMatchPercentage(Double matchPercentage) {
        this.matchPercentage = matchPercentage;
    }

    public String getParsedText() {
        return parsedText;
    }

    public void setParsedText(String parsedText) {
        this.parsedText = parsedText;
    }

    public List<String> getExtractedSkills() {
        return extractedSkills;
    }

    public void setExtractedSkills(List<String> extractedSkills) {
        this.extractedSkills = extractedSkills;
    }

    public List<String> getMissingSkills() {
        return missingSkills;
    }

    public void setMissingSkills(List<String> missingSkills) {
        this.missingSkills = missingSkills;
    }

    public List<Map<String, Object>> getLearningRoadmap() {
        return learningRoadmap;
    }

    public void setLearningRoadmap(List<Map<String, Object>> learningRoadmap) {
        this.learningRoadmap = learningRoadmap;
    }

    public List<Map<String, Object>> getCertifications() {
        return certifications;
    }

    public void setCertifications(List<Map<String, Object>> certifications) {
        this.certifications = certifications;
    }

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(LocalDateTime createdAt) {
        this.createdAt = createdAt;
    }
}
