package com.resumescreener.server.controller;

import com.resumescreener.server.dto.ScreeningResponse;
import com.resumescreener.server.service.ScreeningService;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api/history")
public class HistoryController {

    private final ScreeningService screeningService;

    public HistoryController(ScreeningService screeningService) {
        this.screeningService = screeningService;
    }

    @GetMapping
    public ResponseEntity<List<ScreeningResponse>> getHistory(Authentication authentication) {
        return ResponseEntity.ok(screeningService.getHistory(authentication.getName()));
    }
}
