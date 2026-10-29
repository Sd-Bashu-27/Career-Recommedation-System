# AI-Based Career Path and Job Recommendation System
## Major Project Report
**Bachelor of Technology (B.Tech) in Computer Science and Engineering**  
**Subject:** Machine Learning  
**Academic Year:** 3rd Year B.Tech CSE  

---

## 1. Abstract
The rapid evolution of modern software engineering and data technologies has created an overwhelming array of career specializations for computer science students. Due to a lack of personalized guidance, undergraduate students frequently struggle to identify which tech roles align with their current technical skill sets and which specific skill gaps must be bridged to secure employment.

This project, titled **“AI-Based Career Path and Job Recommendation System,”** presents an explainable, content-based machine learning solution developed with Python Flask, Scikit-learn, SQLite, and Chart.js. The system allows students to either upload a PDF resume or enter their profile manually. A text extraction pipeline built on `PyPDF2` identifies verified technical skills against a comprehensive domain skill dictionary. A Machine Learning recommendation engine leverages **TF-IDF Vectorization** and **Cosine Similarity** to map candidate profiles against curated industry benchmark career paths, returning the Top 3 recommended careers alongside match percentages, matching skills, missing skills, and human-readable reasoning. Furthermore, the system provides an interactive 6-month **Learning Roadmap**, visual **Skill Gap Analytics** using Chart.js radar and doughnut charts, and a **Demonstrative Job Portal**. All profile submissions and recommendation histories are persistently archived in an embedded SQLite database.

---

## 2. Introduction
In standard academic curricula, engineering students acquire foundational theoretical knowledge in data structures, programming languages, database systems, and networking. However, translating this broad foundation into specialized industry roles such as Full Stack Developer, Machine Learning Engineer, Cloud Engineer, or Cybersecurity Analyst requires continuous self-assessment.

Traditional career counseling is often manual, qualitative, and subjective. On the other hand, commercial recruitment platforms cater primarily to experienced professionals with deep work histories, leaving college undergraduates with generic search results.

This project bridges this critical gap by providing an automated, mathematical, and transparent self-assessment platform. Built specifically as a Machine Learning subject project, it demonstrates the practical application of Natural Language Processing (NLP) techniques, vector space modeling, and web framework engineering to solve a real-world problem.

---

## 3. Problem Statement
Undergraduate engineering students frequently face the following challenges:
1. **Uncertainty in Career Specialization:** Difficulty evaluating which sub-field of Computer Science best fits their individual skill set and interests.
2. **Lack of Skill Gap Clarity:** Inability to pinpoint the exact technical tools and frameworks missing from their resumes for targeted job roles.
3. **Absence of Actionable Roadmaps:** Generic advice without structured, phase-by-phase learning plans or realistic portfolio project ideas.
4. **Opacity in Algorithmic Matching:** Many automated matching tools act as opaque "black boxes" without explaining the mathematical rationale behind their recommendations.

---

## 4. Objectives
The core objectives of the system are:
1. **Automated Resume Ingestion:** Extract clean textual data from candidate PDF resumes and accurately recognize 80+ core computer science skills using `PyPDF2`.
2. **Transparent ML Recommendation:** Implement an explainable machine learning recommendation model using **TF-IDF Vectorization** and **Cosine Similarity** in Scikit-learn.
3. **Skill Gap Diagnostics:** Compute set intersections to categorize candidate skills into *Acquired Skills* and *Skills to Bridge*.
4. **Structured Progression Roadmaps:** Generate 3-phase curriculum roadmaps (Beginner, Intermediate, Advanced) with project deliverables and interactive completion trackers.
5. **Interactive Data Visualization:** Utilize Chart.js to render multi-dimensional radar charts, doughnut gap charts, and career affinity bar charts.
6. **Demonstration Job Matching:** Present sample entry-level job vacancies aligned with the recommended careers, clearly identified as academic demo data.
7. **Local Persistence:** Provide automatic table creation and data storage using SQLite without external database servers.

---

## 5. Existing System vs. Proposed System

| Parameter | Existing System | Proposed System |
| :--- | :--- | :--- |
| **Methodology** | Manual counseling or rule-based keyword searches | Mathematical vector space modeling using TF-IDF & Cosine Similarity |
| **Transparency** | Low / Black-box neural models | High / Fully explainable with feature overlap and mathematical metrics |
| **Resume Handling** | Manual copy-pasting | Automated PDF extraction with PyPDF2 and manual entry fallback |
| **Skill Gap Analysis**| Absent or unstructured text | Explicitly computed sets of matched vs missing skills with visual charts |
| **Roadmap Guidance** | Static generic links | 3-phase structured roadmaps with interactive progress tracking |
| **Cost & Latency** | Expensive third-party API keys or GPU requirements | 100% free, local, lightweight, runs instantly on standard laptops |

---

## 6. Software and Hardware Requirements

### Software Requirements
* **Operating System:** Windows 10 / 11, macOS, or Linux
* **Programming Language:** Python 3.9 or higher (tested on Python 3.14)
* **Web Framework:** Python Flask 3.0+
* **Machine Learning Library:** Scikit-learn 1.3+
* **Data Processing:** Pandas 2.0+, NumPy 1.24+
* **PDF Parsing:** PyPDF2 3.0+
* **Database:** SQLite3 (standard library)
* **Frontend Technologies:** HTML5, Vanilla CSS3, JavaScript (ES6+)
* **Charting Library:** Chart.js 4.4+ (CDN)
* **Icons:** Font Awesome 6.5+ (CDN)
* **Code Editor:** Visual Studio Code (VS Code)

### Hardware Requirements
* **Processor:** Intel Core i3 / AMD Ryzen 3 or higher
* **RAM:** 4 GB minimum (8 GB recommended)
* **Disk Space:** 500 MB free space
* **Display Resolution:** 1280 x 720 minimum (Responsive on all screen sizes)

---

## 7. System Architecture

```text
+-----------------------------------------------------------------------------------+
|                                 CLIENT TIER                                       |
|  +--------------------+   +---------------------+   +--------------------------+  |
|  | Modern Dashboard   |   | Student Profile Form|   | PDF Resume Upload Zone   |  |
|  | (HTML5 / CSS3)     |   | (Pill Selectors)    |   | (PyPDF2 Text Ingestion)  |  |
|  +--------------------+   +---------------------+   +--------------------------+  |
|           |                         |                            |                |
|           v                         v                            v                |
|  +-----------------------------------------------------------------------------+  |
|  |                     Client Interactions & Chart.js Visuals                  |  |
|  |           (Radar Chart, Doughnut Gap Chart, Dynamic Progress Bar)           |  |
|  +-----------------------------------------------------------------------------+  |
+------------------------------------------|----------------------------------------+
                                           | HTTP Requests (REST / Jinja2)
                                           v
+-----------------------------------------------------------------------------------+
|                               APPLICATION TIER (Flask)                            |
|  +-----------------------------------------------------------------------------+  |
|  | Flask Routing Controller (app.py)                                           |  |
|  | - Session Management, Request Validation, Error Handlers                    |  |
|  +-----------------------------------------------------------------------------+  |
|           |                                                      |                |
|           v                                                      v                |
|  +----------------------------------+          +-------------------------------+  |
|  | PyPDF2 Resume Parser             |          | ML Recommender Engine         |  |
|  | - PDF Stream Extraction          |          | - TF-IDF Vectorizer           |  |
|  | - Skill Ontology Dictionary      |          | - Cosine Similarity Metric    |  |
|  | - Degree Pattern Regex           |          | - Skill Gap Categorization    |  |
|  +----------------------------------+          +-------------------------------+  |
+------------------------------------------|-----------------------|----------------+
                                           |                       |
                                           v                       v
+-----------------------------------------------------------------------------------+
|                                  DATA TIER                                        |
|  +-----------------------+   +----------------------+   +----------------------+  |
|  | data/careers.csv      |   | data/jobs.csv        |   | data/roadmaps.json   |  |
|  | (Career Benchmarks)   |   | (Sample Job Data)    |   | (Curriculum Stages)  |  |
|  +-----------------------+   +----------------------+   +----------------------+  |
|                                           |                                       |
|                                           v                                       |
|  +-----------------------------------------------------------------------------+  |
|  | SQLite Database (database/career_system.db)                                 |  |
|  | - students table, recommendation_history table, roadmap_progress table      |  |
|  +-----------------------------------------------------------------------------+  |
+-----------------------------------------------------------------------------------+
```

---

## 8. Data Flow Diagram (DFD Level 1)

```text
                         [ Student User ]
                                |
             +------------------+------------------+
             |                                     |
   1. Uploads PDF Resume                  2. Enters Profile Manually
             |                                     |
             v                                     v
     [ PyPDF2 Parser ]                     [ Profile Form ]
             |                                     |
             +------------------+------------------+
                                |
                                v
                   ( Extract & Clean Skills )
                                |
                                v
               [ TF-IDF Vectorizer (Scikit-Learn) ] <--- Reads data/careers.csv
                                |
                                v
                   ( Generate Feature Vectors )
                                |
                                v
                [ Cosine Similarity Calculator ]
                                |
                                v
                    ( Rank Career Matches )
                                |
             +------------------+------------------+
             |                                     |
             v                                     v
     [ SQLite Database ]                 [ Jinja2 Template View ]
 (Store Profile & History)               (Render Top 3 Matches)
                                                   |
                                                   v
                                         [ Chart.js Dashboards ]
                                     (Radar, Doughnut, Roadmaps)
```

---

## 9. Dataset Description

The system utilizes three curated local datasets located in the `data/` directory:

### A. `careers.csv` (Career Benchmark Profiles)
Contains 10 primary technology career paths:
1. Full Stack Developer (Web Development)
2. Data Analyst (Data & Analytics)
3. Machine Learning Engineer (AI & Machine Learning)
4. Python Developer (Software Engineering)
5. Cybersecurity Analyst (Security)
6. Cloud Engineer (Cloud & Infrastructure)
7. DevOps Engineer (DevOps & Site Reliability)
8. Mobile App Developer (Mobile Engineering)
9. UI/UX Designer & Frontend Engineer (Product & Design)
10. Data Engineer (Data Architecture)

Each row includes: `career_id`, `role`, `category`, `description`, `required_skills`, `interests`, `experience_level`, `avg_salary_inr`, `demand_level`, `top_companies`, `certifications`, and `tools`.

### B. `jobs.csv` (Demonstrative Job Listings)
Contains 20 realistic entry-level job postings across India (Bengaluru, Hyderabad, Pune, Remote, Noida, Chennai, Gurugram) with company names (e.g. TechCorp, CloudScale, DataCraft), required skill tags, salary ranges, and job types (Full-time, Internship, Hybrid).

### C. `roadmaps.json` (Curriculum Milestones)
Contains structured 3-phase roadmaps for each role with timeframe (Weeks 1-6, Weeks 7-14, Weeks 15-24), skills to master, core conceptual theory topics, recommended hands-on portfolio projects, and interactive checklist milestone tasks.

---

## 10. Machine Learning Algorithm Formulation

The recommendation engine employs **Content-Based Filtering** based on Vector Space Modeling.

### Step 1: Text Feature Preprocessing
For each career $C_j$, a combined document $D_j$ is formed:
$$D_j = \text{Role}_j + 2 \times \text{RequiredSkills}_j + \text{Interests}_j + \text{Category}_j + \text{Description}_j$$
For candidate $S$, the profile query $Q$ is formed:
$$Q = 2 \times \text{Skills}_S + \text{Interests}_S + \text{PreferredRole}_S$$
*(Skills are repeated to assign double weighting relative to peripheral metadata.)*

### Step 2: TF-IDF Calculation
$$\text{TF}(t, d) = \frac{f_{t,d}}{\sum_{t' \in d} f_{t',d}}$$
$$\text{IDF}(t, D) = \log\left(\frac{1 + N}{1 + |\{d \in D : t \in d\}|}\right) + 1$$
$$\mathbf{w}_{t,d} = \text{TF}(t, d) \times \text{IDF}(t, D)$$
The vectorizer produces normalized vectors $\mathbf{u}_S$ for the candidate and $\mathbf{v}_j$ for each career profile.

### Step 3: Cosine Similarity
$$\text{Sim}_{\text{cosine}}(\mathbf{u}_S, \mathbf{v}_j) = \frac{\mathbf{u}_S \cdot \mathbf{v}_j}{\|\mathbf{u}_S\| \|\mathbf{v}_j\|} = \frac{\sum_{i=1}^n u_i v_i}{\sqrt{\sum_{i=1}^n u_i^2} \sqrt{\sum_{i=1}^n v_i^2}}$$

### Step 4: Skill Overlap & Composite Scoring
Direct skill overlap is calculated:
$$\text{Overlap}(S, C_j) = \frac{|\text{Skills}_S \cap \text{Skills}_{C_j}|}{|\text{Skills}_{C_j}|}$$
The final explainable match score is computed as:
$$\text{Score} = \min\left(98.0, \max\left(15.0, \left[ 0.65 \times \text{Sim}_{\text{cosine}} + 0.35 \times \text{Overlap} + \text{Boost}_{\text{pref}} \right] \times 100\right)\right)$$

---

## 11. Implementation Highlights

1. **Zero-Downtime Database Auto-Initialization:** `ml_engine/database.py` automatically initializes `students`, `recommendation_history`, and `roadmap_progress` tables upon application boot, removing manual SQL setup.
2. **PyPDF2 Robust Exception Guarding:** `ml_engine/resume_parser.py` safely intercepts scanned images or corrupted PDFs, alerting the user to utilize manual entry without crashing the server.
3. **Session Cookie Optimization:** Rather than storing multi-kilobyte JSON objects in client cookies (which triggers browser cookie overflow warnings), the system stores lightweight record IDs and caches full reports in SQLite.
4. **Standalone Training Script:** `models/train_model.py` provides an isolated CLI demonstration to showcase model vocabulary, IDF weights, and test predictions during college evaluation.

---

## 12. Testing and Verification

The system was validated using the `unittest` framework in `tests/test_system.py`:

| Test ID | Test Case | Target Component | Status |
| :--- | :--- | :--- | :--- |
| `test_01` | Home Dashboard Route | `GET /` | **PASSED** (HTTP 200) |
| `test_02` | Profile Form Load | `GET /profile` | **PASSED** (HTTP 200) |
| `test_03` | Recommender Accuracy | `CareerRecommender.recommend()` | **PASSED** (Expected roles ranked #1) |
| `test_04` | Profile Submission & DB | `POST /process_recommendations` | **PASSED** (DB record persisted) |
| `test_05` | Job Portal & Filtering | `GET /jobs?role=...` | **PASSED** (Filtered subset rendered) |
| `test_06` | Roadmap & Progress API | `POST /api/save_roadmap_progress` | **PASSED** (Milestones saved) |
| `test_07` | Analytics Visuals | `GET /analytics` | **PASSED** (Chart JSON payloads valid) |
| `test_08` | SQLite History View | `GET /history` | **PASSED** (History table rendered) |
| `test_09` | About & ML Documentation | `GET /about` | **PASSED** (Documentation rendered) |
| `test_10` | PDF Resume Upload | `POST /upload_resume` | **PASSED** (15 skills detected from PDF) |

**Result:** `Ran 10 tests in 0.643s. OK (100% Passed)`.

---

## 13. Presentation & Screenshots Checklist

When presenting this project to examiners, demonstrate the following screens:
- [x] **Home Dashboard:** Showcase the clean blue and dark navy theme, stats counters, and feature cards.
- [x] **Resume Ingestion:** Upload `sample_resumes/sample_student_resume.pdf` to show real-time PyPDF2 text extraction.
- [x] **Top 3 Recommendations:** Show how match scores, green matched skill badges, and amber missing skill badges render.
- [x] **ML Explainability Box:** Explain the natural language text explaining *why* the career was recommended.
- [x] **Interactive Roadmap:** Check off 2 or 3 tasks to demonstrate the dynamic JavaScript progress bar updating in real time.
- [x] **Job Portal:** Demonstrate filtering by career track and triggering the "Apply Demo" modal.
- [x] **Career Analytics Dashboard:** Explain the multi-axis Radar chart and the Doughnut skills gap chart.
- [x] **SQLite History:** Show that past candidate profiles persist across restarts.
- [x] **CLI Script:** Run `python models/train_model.py` in the terminal to show the vocabulary size and algorithm mechanics.

---

## 14. Advantages and Limitations

### Advantages
1. **Explainable & Deterministic:** Provides direct mathematical and keyword justification for every recommendation.
2. **Zero Operating Cost:** Operates 100% locally with open-source Python libraries without requiring paid external APIs.
3. **Low Latency:** Recommendations are computed in under 15 milliseconds.
4. **Complete End-to-End System:** Spans resume parsing, machine learning, career matching, learning roadmaps, jobs, and database history.

### Limitations
1. **Scanned PDFs:** Pure image-only PDF resumes without text layers cannot be parsed by PyPDF2 (mitigated by manual entry fallback).
2. **Cold Start for New Terms:** Brand new technical buzzwords not present in the career vocabulary require retraining or dataset updates.

---

## 15. Future Enhancements
1. **Optical Character Recognition (OCR):** Integrate `pytesseract` to extract text from scanned paper resumes.
2. **Collaborative Filtering:** Incorporate peer feedback from students who successfully transitioned into recommended jobs.
3. **Automated GitHub Analysis:** Analyze public student GitHub repositories via GitHub's API to verify skill claims automatically.
4. **Quiz & Skill Validation Assessments:** Add short MCQ self-assessments to verify skill proficiency directly on the platform.

---

## 16. Conclusion
The **AI-Based Career Path and Job Recommendation System** provides an effective, explainable, and production-ready solution to assist undergraduate engineering students in mapping their current technical competencies to industry careers. By synthesizing PyPDF2 resume parsing, Scikit-learn TF-IDF vectorization, Cosine Similarity scoring, interactive 3-phase roadmaps, Chart.js analytics, and SQLite persistence into an intuitive web interface, the project fulfills all objectives of the 3rd Year B.Tech Machine Learning project curriculum.

---

## 17. References
1. Salton, G., & Buckley, C. (1988). *Term-weighting approaches in automatic text retrieval*. Information Processing & Management, 24(5), 513-523.
2. Pedregosa, F., et al. (2011). *Scikit-learn: Machine Learning in Python*. Journal of Machine Learning Research, 12, 2825-2830.
3. Grinberg, M. (2018). *Flask Web Development: Developing Web Applications with Python*. O'Reilly Media.
4. Chart.js Documentation: *Open source HTML5 Charts for modern web applications*. https://www.chartjs.org
5. PyPDF2 Documentation: *A Pure-Python PDF Library*. https://pypdf2.readthedocs.io
