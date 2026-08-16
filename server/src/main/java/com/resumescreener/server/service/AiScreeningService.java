package com.resumescreener.server.service;

import com.resumescreener.server.dto.AiAnalysisResult;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.core.io.ByteArrayResource;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.reactive.function.client.WebClient;
import org.springframework.web.reactive.function.client.WebClientResponseException;

import java.io.IOException;

@Service
public class AiScreeningService {

    private final WebClient aiServiceWebClient;

    public AiScreeningService(@Qualifier("aiServiceWebClient") WebClient aiServiceWebClient) {
        this.aiServiceWebClient = aiServiceWebClient;
    }

    /**
     * Forwards the resume file and job description to the FastAPI AI service
     * and returns its screening analysis.
     */
    public AiAnalysisResult analyze(MultipartFile resume, String jobDescription) {
        MultiValueMap<String, Object> body = new LinkedMultiValueMap<>();
        body.add("resume", toResource(resume));
        body.add("job_description", jobDescription);

        try {
            return aiServiceWebClient.post()
                    .uri("/api/analyze")
                    .contentType(MediaType.MULTIPART_FORM_DATA)
                    .bodyValue(body)
                    .retrieve()
                    .bodyToMono(AiAnalysisResult.class)
                    .block();
        } catch (WebClientResponseException ex) {
            throw new IllegalStateException("AI service returned an error: " + ex.getStatusCode(), ex);
        }
    }

    private ByteArrayResource toResource(MultipartFile file) {
        try {
            return new ByteArrayResource(file.getBytes()) {
                @Override
                public String getFilename() {
                    return file.getOriginalFilename();
                }
            };
        } catch (IOException e) {
            throw new IllegalStateException("Failed to read uploaded resume file.", e);
        }
    }
}
