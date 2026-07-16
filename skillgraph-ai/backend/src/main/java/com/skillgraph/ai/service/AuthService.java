package com.skillgraph.ai.service;

import com.skillgraph.ai.dto.LoginRequest;
import com.skillgraph.ai.dto.RegisterRequest;
import com.skillgraph.ai.entity.User;
import com.skillgraph.ai.entity.UserSession;
import com.skillgraph.ai.repository.UserRepository;
import com.skillgraph.ai.repository.UserSessionRepository;
import com.skillgraph.ai.util.PasswordUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.Optional;
import java.util.UUID;

@Service
public class AuthService {

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private UserSessionRepository userSessionRepository;

    @Transactional
    public User register(RegisterRequest request) {
        if (userRepository.findByEmail(request.getEmail()).isPresent()) {
            throw new RuntimeException("Email already in use");
        }

        String hashedPassword = PasswordUtil.hashPassword(request.getPassword());
        User user = new User(
                request.getEmail(),
                hashedPassword,
                request.getFullName(),
                request.getCareerGoal()
        );

        return userRepository.save(user);
    }

    @Transactional
    public String login(LoginRequest request) {
        User user = userRepository.findByEmail(request.getEmail())
                .orElseThrow(() -> new RuntimeException("Invalid email or password"));

        if (!PasswordUtil.checkPassword(request.getPassword(), user.getPassword())) {
            throw new RuntimeException("Invalid email or password");
        }

        // Generate session token
        String token = UUID.randomUUID().toString();
        UserSession session = new UserSession(
                token,
                user,
                LocalDateTime.now().plusHours(24) // 24-hour expiration
        );

        userSessionRepository.save(session);
        return token;
    }

    @Transactional(readOnly = true)
    public User validateToken(String token) {
        if (token == null || token.isEmpty()) {
            throw new RuntimeException("No session token provided");
        }

        UserSession session = userSessionRepository.findByToken(token)
                .orElseThrow(() -> new RuntimeException("Invalid session token"));

        if (session.isExpired()) {
            throw new RuntimeException("Session has expired");
        }

        return session.getUser();
    }

    @Transactional
    public void logout(String token) {
        if (token != null && !token.isEmpty()) {
            userSessionRepository.findByToken(token).ifPresent(session -> {
                userSessionRepository.delete(session);
            });
        }
    }
}
