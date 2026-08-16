package com.resumescreener.server.controller;

import com.resumescreener.server.dto.ScreeningResponse;
import com.resumescreener.server.service.ScreeningService;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

@RestController
@RequestMapping("/api/screening")
public class ScreeningController {

    private final ScreeningService screeningService;

    public ScreeningController(ScreeningService screeningService) {
        this.screeningService = screeningService;
    }

    @PostMapping(value = "/analyze", consumes = "multipart/form-data")
    public ResponseEntity<ScreeningResponse> analyze(
            @RequestPart("resume") MultipartFile resume,
            @RequestPart("jobDescription") String jobDescription) {
        ScreeningResponse response = screeningService.screenResume(resume, jobDescription);
        return ResponseEntity.status(HttpStatus.CREATED).body(response);
    }
}
