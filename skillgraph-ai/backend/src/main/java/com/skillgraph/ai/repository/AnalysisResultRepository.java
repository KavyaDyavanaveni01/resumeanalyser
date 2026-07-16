package com.skillgraph.ai.repository;

import com.skillgraph.ai.entity.AnalysisResult;
import com.skillgraph.ai.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface AnalysisResultRepository extends JpaRepository<AnalysisResult, Long> {
    Optional<AnalysisResult> findFirstByUserOrderByCreatedAtDesc(User user);
}
