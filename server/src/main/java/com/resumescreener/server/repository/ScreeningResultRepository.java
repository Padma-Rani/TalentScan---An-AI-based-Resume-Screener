package com.resumescreener.server.repository;

import com.resumescreener.server.entity.ScreeningResult;
import com.resumescreener.server.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface ScreeningResultRepository extends JpaRepository<ScreeningResult, Long> {

    List<ScreeningResult> findByUserOrderByCreatedAtDesc(User user);
}
