package com.skillgraph.ai.service;

import com.skillgraph.ai.entity.User;
import com.skillgraph.ai.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class UserService {

    @Autowired
    private UserRepository userRepository;

    @Transactional
    public User updateCareerGoal(User user, String careerGoal) {
        User existingUser = userRepository.findById(user.getId())
                .orElseThrow(() -> new RuntimeException("User not found"));
        existingUser.setCareerGoal(careerGoal);
        return userRepository.save(existingUser);
    }
}
