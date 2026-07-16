package com.skillgraph.ai.dto;

import jakarta.validation.constraints.NotBlank;

public class GoalRequest {

    @NotBlank(message = "Career goal is required")
    private String careerGoal;

    // Getters and Setters
    public String getCareerGoal() {
        return careerGoal;
    }

    public void setCareerGoal(String careerGoal) {
        this.careerGoal = careerGoal;
    }
}
