package com.samaira.resumeanalyzer.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import com.samaira.resumeanalyzer.model.User;
import com.samaira.resumeanalyzer.repository.UserRepository;

@RestController
@CrossOrigin(origins = "http://localhost:3000", allowedHeaders = "*", allowCredentials = "true")
public class AuthController {

    @Autowired
    private UserRepository userRepository;

    @PostMapping("/signup")
    public ResponseEntity<String> signup(@RequestBody User user) {
        if (user.getEmail() == null || user.getPassword() == null) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body("Missing email or password");
        }
        userRepository.save(user);
        return ResponseEntity.status(HttpStatus.CREATED).body("User Registered");
    }

    @PostMapping("/login")
    public ResponseEntity<String> login(@RequestBody User user) {
        User existing = userRepository.findByEmail(user.getEmail());

        if (existing != null && existing.getPassword().equals(user.getPassword())) {
            return ResponseEntity.ok("Login Success");
        }
        return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body("Invalid Credentials");
    }
}