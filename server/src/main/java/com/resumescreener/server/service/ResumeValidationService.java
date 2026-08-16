package com.resumescreener.server.service;

import com.resumescreener.server.exception.InvalidResumeFileException;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.util.Set;

@Service
public class ResumeValidationService {

    private static final long MAX_FILE_SIZE_BYTES = 10L * 1024 * 1024; // 10 MB
    private static final Set<String> ALLOWED_CONTENT_TYPES = Set.of(
            "application/pdf",
            "image/jpeg",
            "image/png"
    );

    public void validate(MultipartFile file) {
        if (file == null || file.isEmpty()) {
            throw new InvalidResumeFileException("Please upload a resume file.");
        }

        if (file.getSize() > MAX_FILE_SIZE_BYTES) {
            throw new InvalidResumeFileException("Resume file must be under 10 MB.");
        }

        String contentType = file.getContentType();
        if (contentType == null || !ALLOWED_CONTENT_TYPES.contains(contentType.toLowerCase())) {
            throw new InvalidResumeFileException("Resume must be a PDF, JPEG, or PNG file.");
        }
    }
}
