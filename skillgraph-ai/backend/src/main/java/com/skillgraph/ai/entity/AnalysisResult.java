package com.skillgraph.ai.entity;

import jakarta.persistence.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "analysis_results")
public class AnalysisResult {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id", nullable = false)
    private User user;

    @Column(name = "career_goal", nullable = false)
    private String careerGoal;

    @Column(name = "match_percentage", nullable = false)
    private Double matchPercentage;

    @Lob
    @Column(name = "parsed_text")
    private String parsedText;

    @Lob
    @Column(name = "extracted_skills")
    private String extractedSkills; // Stored as JSON string

    @Lob
    @Column(name = "missing_skills")
    private String missingSkills; // Stored as JSON string

    @Lob
    @Column(name = "learning_roadmap")
    private String learningRoadmap; // Stored as JSON string

    @Lob
    @Column(name = "certifications")
    private String certifications; // Stored as JSON string

    @Column(name = "created_at")
    private LocalDateTime createdAt;

    @PrePersist
    protected void onCreate() {
        this.createdAt = LocalDateTime.now();
    }

    // Constructors
    public AnalysisResult() {}

    public AnalysisResult(User user, String careerGoal, Double matchPercentage, String parsedText,
                          String extractedSkills, String missingSkills, String learningRoadmap, String certifications) {
        this.user = user;
        this.careerGoal = careerGoal;
        this.matchPercentage = matchPercentage;
        this.parsedText = parsedText;
        this.extractedSkills = extractedSkills;
        this.missingSkills = missingSkills;
        this.learningRoadmap = learningRoadmap;
        this.certifications = certifications;
    }

    // Getters and Setters
    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public User getUser() {
        return user;
    }

    public void setUser(User user) {
        this.user = user;
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

    public String getExtractedSkills() {
        return extractedSkills;
    }

    public void setExtractedSkills(String extractedSkills) {
        this.extractedSkills = extractedSkills;
    }

    public String getMissingSkills() {
        return missingSkills;
    }

    public void setMissingSkills(String missingSkills) {
        this.missingSkills = missingSkills;
    }

    public String getLearningRoadmap() {
        return learningRoadmap;
    }

    public void setLearningRoadmap(String learningRoadmap) {
        this.learningRoadmap = learningRoadmap;
    }

    public String getCertifications() {
        return certifications;
    }

    public void setCertifications(String certifications) {
        this.certifications = certifications;
    }

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(LocalDateTime createdAt) {
        this.createdAt = createdAt;
    }
}
