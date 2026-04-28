package com.samaira.resumeanalyzer.model;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;

@Entity
public class Resume {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private String fileName;
    private int matchPercentage;
    public Resume() {}

    public Resume(String fileName, int matchPercentage) {
        this.fileName = fileName;
        this.matchPercentage = matchPercentage;
    }
    public Long getId() { return id; }
    public String getFileName() { return fileName; }
    public int getMatchPercentage() { return matchPercentage; }
    public void setFileName(String fileName) { this.fileName = fileName; }
    public void setMatchPercentage(int matchPercentage) { this.matchPercentage = matchPercentage; }
}