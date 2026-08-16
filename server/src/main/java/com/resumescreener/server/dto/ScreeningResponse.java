package com.resumescreener.server.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.Instant;
import java.util.List;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ScreeningResponse {

    private Long id;
    private String candidateName;
    private double matchScore;
    private boolean eligible;
    private List<String> matchedSkills;
    private List<String> missingSkills;
    private String summary;
    private Instant createdAt;
}
