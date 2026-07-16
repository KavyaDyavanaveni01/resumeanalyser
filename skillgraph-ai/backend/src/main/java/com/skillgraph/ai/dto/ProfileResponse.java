package com.skillgraph.ai.dto;

public class ProfileResponse {
    private String email;
    private String fullName;
    private String careerGoal;

    public ProfileResponse(String email, String fullName, String careerGoal) {
        this.email = email;
        this.fullName = fullName;
        this.careerGoal = careerGoal;
    }

    // Getters and Setters
    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public String getFullName() {
        return fullName;
    }

    public void setFullName(String fullName) {
        this.fullName = fullName;
    }

    public String getCareerGoal() {
        return careerGoal;
    }

    public void setCareerGoal(String careerGoal) {
        this.careerGoal = careerGoal;
    }
}
