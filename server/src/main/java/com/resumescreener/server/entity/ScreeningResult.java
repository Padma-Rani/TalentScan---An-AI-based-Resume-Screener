package com.resumescreener.server.entity;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.Instant;
import java.util.List;

@Entity
@Table(name = "screening_results")
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ScreeningResult {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String candidateName;

    private double matchScore;

    private boolean eligible;

    @ElementCollection
    @CollectionTable(name = "screening_matched_skills", joinColumns = @JoinColumn(name = "screening_id"))
    @Column(name = "skill")
    private List<String> matchedSkills;

    @ElementCollection
    @CollectionTable(name = "screening_missing_skills", joinColumns = @JoinColumn(name = "screening_id"))
    @Column(name = "skill")
    private List<String> missingSkills;

    @Column(length = 2000)
    private String summary;

    @Column(nullable = false, updatable = false)
    private Instant createdAt;

    @PrePersist
    void onCreate() {
        this.createdAt = Instant.now();
    }
}