package com.samaira.resumeanalyzer.controller;

import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.text.PDFTextStripper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

import com.samaira.resumeanalyzer.model.Resume;
import com.samaira.resumeanalyzer.repository.ResumeRepository;

@RestController
@CrossOrigin(origins = "http://localhost:3000")
public class ResumeController {

    @Autowired
    private ResumeRepository resumeRepository;

    @PostMapping("/upload")
    public String uploadResume(
            @RequestParam("file") MultipartFile file,
            @RequestParam("jobDescription") String jobDescription
    ) {

        try (PDDocument document = PDDocument.load(file.getInputStream())) {

            String text = new PDFTextStripper().getText(document).toLowerCase();

            String cleanResume = text.replaceAll("[^a-zA-Z0-9 ]", " ");
            String cleanJD = jobDescription.toLowerCase().replaceAll("[^a-zA-Z0-9 ]", " ");

            List<String> resumeWords = Arrays.asList(cleanResume.split("\\s+"));
            List<String> jdWords = Arrays.asList(cleanJD.split("\\s+"));

            Set<String> stopWords = new HashSet<>(Arrays.asList(
                    "and","or","the","is","are","a","an","to","for","of","in","on","with","by"
            ));

            Set<String> jdKeywords = new HashSet<>();
            for (String word : jdWords) {
                if (!stopWords.contains(word) && word.length() > 2) {
                    jdKeywords.add(word);
                }
            }

            Set<String> resumeKeywords = new HashSet<>();
            for (String word : resumeWords) {
                if (!stopWords.contains(word) && word.length() > 2) {
                    resumeKeywords.add(word);
                }
            }

            Set<String> matched = new HashSet<>(jdKeywords);
            matched.retainAll(resumeKeywords);

            Set<String> missing = new HashSet<>(jdKeywords);
            missing.removeAll(resumeKeywords);

            int matchPercentage = jdKeywords.size() == 0 ? 0 :
                    (int)((matched.size() * 100.0) / jdKeywords.size());

            Resume resume = new Resume(file.getOriginalFilename(), matchPercentage);
            resumeRepository.save(resume);

            String feedback = matchPercentage >= 80 ? "Excellent 🔥"
                    : matchPercentage >= 50 ? "Good 👍"
                    : "Needs Improvement ⚠️";

            return "JD Keywords: " + jdKeywords +
                    "\n\nMatched Keywords: " + matched +
                    "\n\nMissing Keywords: " + missing +
                    "\n\nMatch Percentage: " + matchPercentage + "%" +
                    "\n\nFeedback: " + feedback;

        } catch (Exception e) {
            return "Error processing resume";
        }
    }

    @GetMapping("/dashboard")
    public List<Resume> getRanking() {
        return resumeRepository.findAllByOrderByMatchPercentageDesc();
    }
}