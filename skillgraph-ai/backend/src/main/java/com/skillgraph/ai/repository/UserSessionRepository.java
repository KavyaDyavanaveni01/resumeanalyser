package com.skillgraph.ai.repository;

import com.skillgraph.ai.entity.User;
import com.skillgraph.ai.entity.UserSession;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface UserSessionRepository extends JpaRepository<UserSession, Long> {
    Optional<UserSession> findByToken(String token);
    void deleteByToken(String token);
    void deleteByUser(User user);
}
