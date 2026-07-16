package com.skillgraph.ai.controller;

import com.skillgraph.ai.dto.GoalRequest;
import com.skillgraph.ai.dto.ProfileResponse;
import com.skillgraph.ai.entity.User;
import com.skillgraph.ai.service.AuthService;
import com.skillgraph.ai.service.UserService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/api/user")
public class UserController {

    @Autowired
    private AuthService authService;

    @Autowired
    private UserService userService;

    @GetMapping("/profile")
    public ResponseEntity<?> getProfile(@RequestHeader("Authorization") String authHeader) {
        try {
            User user = validateHeaderAndGetUser(authHeader);
            return ResponseEntity.ok(new ProfileResponse(user.getEmail(), user.getFullName(), user.getCareerGoal()));
        } catch (Exception e) {
            return buildErrorResponse(e);
        }
    }

    @PutMapping("/profile")
    public ResponseEntity<?> updateProfile(@RequestHeader("Authorization") String authHeader,
                                           @Valid @RequestBody GoalRequest request) {
        try {
            User user = validateHeaderAndGetUser(authHeader);
            User updatedUser = userService.updateCareerGoal(user, request.getCareerGoal());
            return ResponseEntity.ok(new ProfileResponse(updatedUser.getEmail(), updatedUser.getFullName(), updatedUser.getCareerGoal()));
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
