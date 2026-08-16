package com.resumescreener.server.service;

import com.resumescreener.server.dto.AiAnalysisResult;
import com.resumescreener.server.dto.ScreeningResponse;
import com.resumescreener.server.entity.ScreeningResult;
import com.resumescreener.server.repository.ScreeningResultRepository;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.util.List;

@Service
public class ScreeningService {

    private final ResumeValidationService resumeValidationService;
    private final AiScreeningService aiScreeningService;
    private final ScreeningResultRepository screeningResultRepository;

    public ScreeningService(ResumeValidationService resumeValidationService,
                             AiScreeningService aiScreeningService,
                             ScreeningResultRepository screeningResultRepository) {
        this.resumeValidationService = resumeValidationService;
        this.aiScreeningService = aiScreeningService;
        this.screeningResultRepository = screeningResultRepository;
    }

    public ScreeningResponse screenResume(MultipartFile resume, String jobDescription) {
        resumeValidationService.validate(resume);

        AiAnalysisResult analysis = aiScreeningService.analyze(resume, jobDescription);

        ScreeningResult saved = screeningResultRepository.save(ScreeningResult.builder()
                .candidateName(analysis.getCandidateName())
                .matchScore(analysis.getMatchScore())
                .eligible(analysis.isEligible())
                .matchedSkills(analysis.getMatchedSkills())
                .missingSkills(analysis.getMissingSkills())
                .summary(analysis.getSummary())
                .build());

        return toResponse(saved);
    }

    public List<ScreeningResponse> getHistory() {
        return screeningResultRepository.findAllByOrderByCreatedAtDesc()
                .stream()
                .map(this::toResponse)
                .toList();
    }

    private ScreeningResponse toResponse(ScreeningResult result) {
        return ScreeningResponse.builder()
                .id(result.getId())
                .candidateName(result.getCandidateName())
                .matchScore(result.getMatchScore())
                .eligible(result.isEligible())
                .matchedSkills(result.getMatchedSkills())
                .missingSkills(result.getMissingSkills())
                .summary(result.getSummary())
                .createdAt(result.getCreatedAt())
                .build();
    }
}
