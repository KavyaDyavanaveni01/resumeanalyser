package com.skillgraph.ai.controller;

import com.skillgraph.ai.dto.AnalysisResponse;
import com.skillgraph.ai.entity.User;
import com.skillgraph.ai.service.AuthService;
import com.skillgraph.ai.service.ResumeService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.*;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.util.HashMap;
import java.util.Map;
import java.util.Optional;

@RestController
@RequestMapping("/api/resume")
public class ResumeController {

    @Autowired
    private AuthService authService;

    @Autowired
    private ResumeService resumeService;

    @PostMapping("/upload")
    public ResponseEntity<?> uploadResume(@RequestHeader("Authorization") String authHeader,
                                          @RequestParam("file") MultipartFile file) {
        try {
            User user = validateHeaderAndGetUser(authHeader);
            if (file.isEmpty()) {
                throw new RuntimeException("Please upload a file");
            }
            AnalysisResponse analysis = resumeService.uploadAndAnalyze(file, user);
            return ResponseEntity.ok(analysis);
        } catch (Exception e) {
            return buildErrorResponse(e);
        }
    }

    @GetMapping("/analysis")
    public ResponseEntity<?> getLatestAnalysis(@RequestHeader("Authorization") String authHeader) {
        try {
            User user = validateHeaderAndGetUser(authHeader);
            Optional<AnalysisResponse> analysis = resumeService.getLatestAnalysis(user);
            if (analysis.isPresent()) {
                return ResponseEntity.ok(analysis.get());
            } else {
                Map<String, String> response = new HashMap<>();
                response.put("message", "No resume analysis available. Please upload your resume.");
                return ResponseEntity.status(HttpStatus.NOT_FOUND).body(response);
            }
        } catch (Exception e) {
            return buildErrorResponse(e);
        }
    }

    @GetMapping("/report")
    public ResponseEntity<?> downloadReport(@RequestHeader("Authorization") String authHeader) {
        try {
            User user = validateHeaderAndGetUser(authHeader);
            byte[] pdfBytes = resumeService.generatePdfReport(user);

            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_PDF);
            headers.setContentDisposition(ContentDisposition.attachment().filename("SkillGraph_AI_Report.pdf").build());
            headers.setContentLength(pdfBytes.length);

            return new ResponseEntity<>(pdfBytes, headers, HttpStatus.OK);
        } catch (Exception e) {
            return buildErrorResponse(e);
        }
    }

    private User validateHeaderAndGetUser(String authHeader) {
        if (authHeader == null || !authHeader.startsWith("Bearer ")) {
            throw new RuntimeException("Missing or invalid Authorization header");
        }
        String token = authHeader.substring(7);
        return authService.validateToken(token);
    }

    private ResponseEntity<?> buildErrorResponse(Exception e) {
        Map<String, String> error = new HashMap<>();
        error.put("error", e.getMessage());
        if (e.getMessage().contains("token") || e.getMessage().contains("Session")) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(error);
        }
        return ResponseEntity.badRequest().body(error);
    }
}
