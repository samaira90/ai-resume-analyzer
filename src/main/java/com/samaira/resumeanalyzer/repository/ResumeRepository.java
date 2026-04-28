package com.samaira.resumeanalyzer.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;

import com.samaira.resumeanalyzer.model.Resume;

public interface ResumeRepository extends JpaRepository<Resume, Long> {

    List<Resume> findAllByOrderByMatchPercentageDesc();
}