# ATS Resume Analyzer

An AI-powered ATS (Applicant Tracking System) Resume Analyzer built using Streamlit, Gemini AI, and Semantic Skill Matching.

The application helps candidates evaluate how well their resume matches a job description, identify missing skills, receive AI-powered feedback, generate learning roadmaps, and download detailed ATS reports.

---

## Features

### Resume Parsing
- Upload resumes in PDF format
- Extract resume text automatically
- Detect technical skills from resume content

### Job Description Analysis
- Extract required skills from job descriptions
- Compare resume skills against job requirements

### Semantic Skill Matching
- Uses Sentence Transformers and RapidFuzz
- Detects related skills even when exact keywords differ
- Improves ATS score accuracy compared to keyword-only matching

### ATS Score Calculation
- Calculates resume-job compatibility score
- Visual progress indicator
- Skill match statistics dashboard

### AI-Powered Resume Review
Using Google Gemini AI:
- Strengths Analysis
- Weaknesses Analysis
- Improvement Suggestions

### AI Learning Roadmap
Generates personalized learning plans for missing skills:
- Skill Overview
- Importance
- Key Topics
- Mini Project Ideas

### Resume Rewrite Suggestions
- ATS-friendly bullet points
- Missing skill integration
- Professional resume enhancement suggestions

### PDF Report Generation
Download a complete ATS analysis report including:
- ATS Score
- Matched Skills
- Missing Skills
- AI Review
- Learning Roadmap
- Resume Suggestions

---

## Tech Stack

- Python
- Streamlit
- Pandas
- PDFPlumber
- Google Gemini API
- Sentence Transformers
- RapidFuzz
- Matplotlib
- ReportLab

---

## Project Structure

```text
ATS-Resume-Analyzer/
│
├── app.py
├── smart_match.py
├── gemini_helper.py
├── report_generator.py
├── config.py
├── skills.csv
├── requirements.txt
├── .gitignore
└── README.md