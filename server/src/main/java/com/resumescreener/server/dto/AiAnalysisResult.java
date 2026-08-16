package com.resumescreener.server.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

/**
 * Mirrors the JSON payload returned by the FastAPI AI service.
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
public class AiAnalysisResult {
    private String candidateName;
    private double matchScore;
    private boolean eligible;
    private List<String> matchedSkills;
    private List<String> missingSkills;
    private String summary;
}
