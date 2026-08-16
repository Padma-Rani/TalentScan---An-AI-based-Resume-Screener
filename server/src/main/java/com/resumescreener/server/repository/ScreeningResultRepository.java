package com.resumescreener.server.repository;

import com.resumescreener.server.entity.ScreeningResult;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface ScreeningResultRepository extends JpaRepository<ScreeningResult, Long> {

    List<ScreeningResult> findAllByOrderByCreatedAtDesc();
}
