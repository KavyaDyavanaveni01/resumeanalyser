package com.skillgraph.ai.service;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.skillgraph.ai.dto.AnalysisResponse;
import com.skillgraph.ai.dto.FlaskParseResponse;
import com.skillgraph.ai.entity.AnalysisResult;
import com.skillgraph.ai.entity.User;
import com.skillgraph.ai.repository.AnalysisResultRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.io.ByteArrayResource;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

@Service
public class ResumeService {

    @Autowired
    private AnalysisResultRepository analysisResultRepository;

    @Value("${app.ai-service-url}")
    private String flaskServiceUrl;

    private final ObjectMapper objectMapper = new ObjectMapper();
    private final RestTemplate restTemplate = new RestTemplate();

    @Transactional
    public AnalysisResponse uploadAndAnalyze(MultipartFile file, User user) throws IOException {
        String careerGoal = user.getCareerGoal();
        if (careerGoal == null || careerGoal.trim().isEmpty()) {
            throw new RuntimeException("Please select a career goal in your profile first");
        }

        // Call Flask Service for NLP Analysis
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.MULTIPART_FORM_DATA);

        MultiValueMap<String, Object> body = new LinkedMultiValueMap<>();
        ByteArrayResource fileResource = new ByteArrayResource(file.getBytes()) {
            @Override
            public String getFilename() {
                return file.getOriginalFilename();
            }
        };
        body.add("file", fileResource);
        body.add("career_goal", careerGoal);

        HttpEntity<MultiValueMap<String, Object>> requestEntity = new HttpEntity<>(body, headers);
        
        FlaskParseResponse flaskResponse;
        try {
            flaskResponse = restTemplate.postForObject(
                    flaskServiceUrl + "/api/parse",
                    requestEntity,
                    FlaskParseResponse.class
            );
        } catch (Exception e) {
            throw new RuntimeException("Failed to communicate with Python AI parsing service. Make sure the AI microservice is running: " + e.getMessage(), e);
        }

        if (flaskResponse == null) {
            throw new RuntimeException("Empty response from AI parsing service");
        }

        // Convert structures to JSON Strings for DB storage
        String extractedSkillsJson = objectMapper.writeValueAsString(flaskResponse.getExtracted_skills());
        String missingSkillsJson = objectMapper.writeValueAsString(flaskResponse.getMissing_skills());
        String roadmapJson = objectMapper.writeValueAsString(flaskResponse.getLearning_roadmap());
        String certsJson = objectMapper.writeValueAsString(flaskResponse.getCertifications());

        // Save Result in Database
        AnalysisResult result = new AnalysisResult(
                user,
                careerGoal,
                flaskResponse.getMatch_percentage(),
                flaskResponse.getParsed_text(),
                extractedSkillsJson,
                missingSkillsJson,
                roadmapJson,
                certsJson
        );

        analysisResultRepository.save(result);

        return mapToResponse(result);
    }

    @Transactional(readOnly = true)
    public Optional<AnalysisResponse> getLatestAnalysis(User user) {
        return analysisResultRepository.findFirstByUserOrderByCreatedAtDesc(user)
                .map(this::mapToResponse);
    }

    public byte[] generatePdfReport(User user) throws IOException {
        AnalysisResult result = analysisResultRepository.findFirstByUserOrderByCreatedAtDesc(user)
                .orElseThrow(() -> new RuntimeException("No analysis results found to generate a report. Please upload a resume first."));

        // Format Request for PDF Generator
        Map<String, Object> request = new HashMap<>();
        request.put("full_name", user.getFullName());
        request.put("email", user.getEmail());
        request.put("career_goal", result.getCareerGoal());
        request.put("match_percentage", result.getMatchPercentage());
        request.put("extracted_skills", objectMapper.readValue(result.getExtractedSkills(), new TypeReference<List<String>>() {}));
        request.put("missing_skills", objectMapper.readValue(result.getMissingSkills(), new TypeReference<List<String>>() {}));
        request.put("learning_roadmap", objectMapper.readValue(result.getLearningRoadmap(), new TypeReference<List<Map<String, Object>>>() {}));
        request.put("certifications", objectMapper.readValue(result.getCertifications(), new TypeReference<List<Map<String, Object>>>() {}));

        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);

        HttpEntity<Map<String, Object>> requestEntity = new HttpEntity<>(request, headers);

        try {
            ResponseEntity<byte[]> response = restTemplate.postForEntity(
                    flaskServiceUrl + "/api/generate-pdf",
                    requestEntity,
                    byte[].class
            );
            return response.getBody();
        } catch (Exception e) {
            throw new RuntimeException("Failed to generate PDF from Python AI service: " + e.getMessage(), e);
        }
    }

    private AnalysisResponse mapToResponse(AnalysisResult result) {
        try {
            List<String> extracted = objectMapper.readValue(result.getExtractedSkills(), new TypeReference<List<String>>() {});
            List<String> missing = objectMapper.readValue(result.getMissingSkills(), new TypeReference<List<String>>() {});
            List<Map<String, Object>> roadmap = objectMapper.readValue(result.getLearningRoadmap(), new TypeReference<List<Map<String, Object>>>() {});
            List<Map<String, Object>> certs = objectMapper.readValue(result.getCertifications(), new TypeReference<List<Map<String, Object>>>() {});

            return new AnalysisResponse(
                    result.getId(),
                    result.getCareerGoal(),
                    result.getMatchPercentage(),
                    result.getParsedText(),
                    extracted,
                    missing,
                    roadmap,
                    certs,
                    result.getCreatedAt()
            );
        } catch (IOException e) {
            throw new RuntimeException("Error parsing cached analysis JSON from database", e);
        }
    }
}
