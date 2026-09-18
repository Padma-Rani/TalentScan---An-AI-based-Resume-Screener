package com.resumescreener.server.service;

import com.resumescreener.server.dto.AiAnalysisResult;
import com.resumescreener.server.dto.ScreeningResponse;
import com.resumescreener.server.entity.ScreeningResult;
import com.resumescreener.server.entity.User;
import com.resumescreener.server.exception.InvalidCredentialsException;
import com.resumescreener.server.repository.ScreeningResultRepository;
import com.resumescreener.server.repository.UserRepository;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.util.List;

@Service
public class ScreeningService {

    private final ResumeValidationService resumeValidationService;
    private final AiScreeningService aiScreeningService;
    private final ScreeningResultRepository screeningResultRepository;
    private final UserRepository userRepository;

    public ScreeningService(ResumeValidationService resumeValidationService,
                             AiScreeningService aiScreeningService,
                             ScreeningResultRepository screeningResultRepository,
                             UserRepository userRepository) {
        this.resumeValidationService = resumeValidationService;
        this.aiScreeningService = aiScreeningService;
        this.screeningResultRepository = screeningResultRepository;
        this.userRepository = userRepository;
    }

    public ScreeningResponse screenResume(MultipartFile resume, String jobDescription, String userEmail) {
        resumeValidationService.validate(resume);

        AiAnalysisResult analysis = aiScreeningService.analyze(resume, jobDescription);
        User user = getUser(userEmail);

        ScreeningResult saved = screeningResultRepository.save(ScreeningResult.builder()
                .user(user)
                .candidateName(analysis.getCandidateName())
                .matchScore(analysis.getMatchScore())
                .eligible(analysis.isEligible())
                .matchedSkills(analysis.getMatchedSkills())
                .missingSkills(analysis.getMissingSkills())
                .summary(analysis.getSummary())
                .build());

        return toResponse(saved);
    }

    public List<ScreeningResponse> getHistory(String userEmail) {
        User user = getUser(userEmail);
        return screeningResultRepository.findByUserOrderByCreatedAtDesc(user)
                .stream()
                .map(this::toResponse)
                .toList();
    }

    private User getUser(String email) {
        return userRepository.findByEmail(email)
                .orElseThrow(() -> new InvalidCredentialsException("User not found."));
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
