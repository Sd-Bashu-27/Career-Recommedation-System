# AI-Based Career Path and Job Recommendation System 🚀
**Machine Learning Subject Major Project — B.Tech CSE (3rd Year)**

A full-stack, explainable Machine Learning web application that matches students and job seekers with the most suitable tech career paths and entry-level job opportunities. It extracts technical skills from PDF resumes using **PyPDF2**, performs **TF-IDF Feature Extraction** and **Cosine Similarity** matching using **Scikit-learn**, tracks progress with a 6-month interactive **Learning Roadmap**, and visualizes skill gaps using **Chart.js** and **SQLite**.

---

## 📑 Table of Contents
1. [Key Features](#-key-features)
2. [Technology Stack](#-technology-stack)
3. [Project Directory Structure](#-project-directory-structure)
4. [Windows Setup & Installation Guide](#-windows-setup--installation-guide)
5. [How to Run the Project](#-how-to-run-the-project)
6. [Feature Walkthrough](#-feature-walkthrough)
7. [How the Machine Learning Algorithm Works](#-how-the-machine-learning-algorithm-works)
8. [Automated Testing](#-automated-testing)
9. [Common Errors & Troubleshooting](#-common-errors--troubleshooting)
10. [College Viva & Presentation Tips](#-college-viva--presentation-tips)

---

## 🌟 Key Features

* **Modern Dashboard Home:** Professional blue and dark navy interface with key metrics, module cards, and project workflow.
* **Resume Text Extraction (PyPDF2):** Instant PDF resume upload that parses text, scans against an 80+ technical skill catalog, and auto-fills the profile.
* **Manual Skill Entry Fallback:** Type or click 20+ quick-add skill badges if you don't have a PDF resume ready.
* **Explainable Machine Learning Recommendations:**
  * Uses TF-IDF Vectorization and Cosine Similarity to compare candidate skills against curated career profiles.
  * Recommends Top 3 career paths with an affinity score (15% - 98%).
  * Lists exact **Matched Skills** (green) and **Skills to Bridge** (amber).
  * Natural language explanation explaining *why* this path was recommended.
  * Clear disclaimer that match scores measure profile alignment, not guaranteed hiring probability.
* **Demonstrative Job Portal:** 20+ entry-level jobs with filters by career role, job type, and keyword search, highlighting candidate-matching skills and a simulated application modal.
* **Step-by-Step Learning Roadmaps:** 3-phase progression (Beginner, Intermediate, Advanced) for 10 career paths, with project deliverables and an interactive milestone checklist that saves progress.
* **Career Analytics & Skill Gap Dashboard:** Chart.js radar charts for domain coverage, doughnut charts for acquired vs missing skills, and bar comparisons across all tech roles.
* **Persistent SQLite Database:** Automatically creates tables on first run (`database/career_system.db`) to record student submissions, recommendation history, and roadmap checkpoints.

---

## 🛠️ Technology Stack

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Frontend** | HTML5, CSS3, JavaScript (ES6+) | Modern, responsive dashboard design without heavy dependencies |
| **Styling** | Vanilla CSS Design System | Custom CSS variables, dark navy / professional blue palette |
| **Charts** | Chart.js (CDN v4) | Radar, doughnut, and bar visualizations |
| **Icons** | Font Awesome 6 (CDN) | Modern interface icons |
| **Backend** | Python Flask (v3.0+) | WSGI web framework, REST routes, request dispatching |
| **Machine Learning** | Scikit-learn (TF-IDF & Cosine Similarity) | Vector space feature representation and similarity calculation |
| **Resume Parsing** | PyPDF2 (v3.0+) | PDF document text extraction and regex pattern matching |
| **Database** | SQLite3 | Embedded persistent database requiring zero external configuration |

---

## 📂 Project Directory Structure

```text
f65/
│
├── app.py                      # Main Flask application and URL routes
├── requirements.txt            # Python package dependencies
├── README.md                   # Setup guide and instructions
├── PROJECT_REPORT.md           # College project documentation with diagrams
│
├── data/                       # Local datasets
│   ├── careers.csv             # Benchmark career profiles, required skills & salaries
│   ├── jobs.csv                # Sample demonstration job postings
│   └── roadmaps.json           # 3-phase curriculum, projects & practice tasks
│
├── ml_engine/                  # Core machine learning & backend modules
│   ├── __init__.py             # Python package marker
│   ├── recommender.py          # TF-IDF & Cosine Similarity recommendation engine
│   ├── resume_parser.py        # PyPDF2 resume extraction & skill identification
│   └── database.py             # SQLite helper functions & auto-initialization
│
├── models/
│   └── train_model.py          # Standalone training demo script for viva presentation
│
├── sample_resumes/
│   └── sample_student_resume.pdf # Sample student PDF resume for testing
│
├── static/                     # Web assets
│   ├── css/
│   │   └── style.css           # Modern professional dashboard design system
│   ├── js/
│   │   └── main.js            # Client-side mobile navigation & interactions
│   └── uploads/                # Temporary storage for uploaded resumes
│
├── templates/                  # Jinja2 HTML Templates
│   ├── base.html               # Shared layout, navbar, footer & CDN imports
│   ├── index.html              # Homepage dashboard & feature overview
│   ├── profile.html            # Profile creation form & PDF resume upload
│   ├── recommendations.html    # Top 3 career matches & comparison chart
│   ├── jobs.html               # Demonstrative job listings with search & filter
│   ├── roadmap.html            # Interactive 3-phase learning roadmap
│   ├── analytics.html          # Radar & Doughnut skill gap charts
│   ├── history.html            # Past student assessments from SQLite
│   └── about.html              # Academic ML documentation & viva talking points
│
└── tests/
    └── test_system.py          # Complete 10-test automated test suite
```

---

## 💻 Windows Setup & Installation Guide

Follow these commands in **Windows Command Prompt (`cmd.exe`)** or the **VS Code Terminal**.

### Step 1: Open Terminal in Project Folder
Open VS Code, press ``Ctrl + ` `` to open the terminal, or open Command Prompt and navigate to the folder:
```cmd
cd "c:\Users\Bashu\OneDrive\Videos\Captures\f65"
```

### Step 2: Verify Python Installation
Check that Python 3.9+ is installed:
```cmd
python --version
```

### Step 3: (Recommended) Create a Virtual Environment
```cmd
python -m venv venv
```

Activate the virtual environment:
```cmd
venv\Scripts\activate
```
*(When activated, you will see `(venv)` at the beginning of your command line.)*

### Step 4: Install Dependencies
```cmd
pip install -r requirements.txt
```
*Packages installed: `Flask`, `scikit-learn`, `PyPDF2`, `pandas`, `numpy`, `Werkzeug`.*

---

## 🚀 How to Run the Project

### Step 1: Start the Flask Application
Run the main app file:
```cmd
python app.py
```

You will see output similar to:
```text
==================================================================
AI-Based Career Path and Job Recommendation System
Running locally at: http://127.0.0.1:5000
Machine Learning Subject Project (B.Tech CSE 3rd Year)
==================================================================
 * Running on http://127.0.0.1:5000
```

### Step 2: Open in Your Web Browser
Open your browser (Google Chrome, Microsoft Edge, or Mozilla Firefox) and visit:
👉 **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## 🧭 Feature Walkthrough

### 1. Home Dashboard (`/`)
* Displays project title, statistics counters, core system modules, and step-by-step workflow.
* Click **"Upload Resume & Get Recommendations"** or **"Get Started"** to proceed.

### 2. Student Profile & Resume Parsing (`/profile`)
* **Option A: Upload Resume:** Click the upload box or drag-and-drop a PDF resume. Try `sample_resumes/sample_student_resume.pdf`. Click **"Extract Skills from Resume"**. The system detects skills (e.g. Python, SQL, React) and fills them in.
* **Option B: Manual Entry:** Type your name, education degree, technical skills, interests, and preferred career. Or click **"Fill Sample Student"** to instantly test with realistic demo data.
* Click **"Generate ML Recommendations 🚀"**.

### 3. Career Recommendations (`/recommendations`)
* Displays the **Top 3 Recommended Careers** ranked by affinity percentage.
* Shows **Matched Skills** (green badges) and **Skills to Learn** (amber badges).
* Provides a human-readable **Explanation** clarifying why this recommendation fits your profile.
* Interactive Chart.js bar chart displays the relative match scores across all 10 career paths.

### 4. Interactive Learning Roadmap (`/roadmap`)
* Shows a 3-phase curriculum (Weeks 1-6 Beginner, Weeks 7-14 Intermediate, Weeks 15-24 Advanced).
* Contains recommended hands-on portfolio projects and key theory concepts.
* Check off practice milestones. Notice the **Roadmap Completion progress bar** update dynamically!

### 5. Demonstrative Job Portal (`/jobs`)
* Displays curated entry-level jobs with salary packages in India, location, and requirements.
* Required skills matching your profile are highlighted in green.
* Filter by career track or job type, and test the **"Apply Demo"** simulated submission modal.

### 6. Career Analytics & Skill Gap (`/analytics`)
* **Doughnut Chart:** Proportion of acquired skills vs skills to learn.
* **Radar Chart:** Technical domain coverage across Web, AI/ML, Data, Cloud/DevOps, Security, and Mobile.
* **Bar Chart:** Career affinity ranking comparison.

### 7. Saved Recommendation History (`/history`)
* All evaluations are saved in SQLite (`database/career_system.db`).
* View past student assessments, dates, and click **"View Report"** to reload previous evaluations.

---

## 🧠 How the Machine Learning Algorithm Works

### 1. Content-Based Filtering
The recommendation system uses **Content-Based Filtering**. It builds a mathematical vector representation of the student profile and compares it against pre-computed career profiles.

### 2. TF-IDF (Term Frequency - Inverse Document Frequency)
Text features (required skills, category, role name, and interests) are vectorized using TF-IDF:
$$\text{TF}(t, d) = \frac{\text{Count of term } t \text{ in document } d}{\text{Total terms in } d}$$
$$\text{IDF}(t, D) = \log\left(\frac{1 + N}{1 + \text{count of docs with } t}\right) + 1$$
$$\text{TF-IDF}(t, d, D) = \text{TF}(t, d) \times \text{IDF}(t, D)$$
*Benefit:* Specialized technical skills (e.g. *Kubernetes, Scikit-learn, Wireshark*) are assigned high weights, while generic words are down-weighted.

### 3. Cosine Similarity Measurement
The cosine of the angle between the student feature vector $\mathbf{u}$ and career vector $\mathbf{v}$ is calculated:
$$\text{Cosine Similarity}(\mathbf{u}, \mathbf{v}) = \frac{\mathbf{u} \cdot \mathbf{v}}{\|\mathbf{u}\| \|\mathbf{v}\|} = \frac{\sum u_i v_i}{\sqrt{\sum u_i^2} \sqrt{\sum v_i^2}}$$
* Range: $0.0$ (no similarity) to $1.0$ (identical skill profile).

### 4. Composite Explainable Scoring Formula
$$\text{Final Score} = \left[ (\text{Cosine Sim} \times 0.65) + (\text{Skill Overlap Ratio} \times 0.35) + \text{Preference Boost} \right] \times 100$$
* Scaled between $15\%$ and $98\%$.
* *Academic Note:* Matching scores are algorithmic similarity estimates indicating technical alignment, not guaranteed hiring probabilities.

---

## 🧪 Automated Testing

To run the complete test suite verifying all 10 modules:
```cmd
python tests\test_system.py
```

Expected output:
```text
..........
----------------------------------------------------------------------
Ran 10 tests in 0.643s

OK
```

To run the standalone model training inspection script:
```cmd
python models\train_model.py
```

---

## ❓ Common Errors & Troubleshooting

| Error | Root Cause | Solution |
| :--- | :--- | :--- |
| `ModuleNotFoundError: No module named 'flask'` | Dependencies not installed in environment | Run `pip install -r requirements.txt` |
| `Address already in use (Port 5000)` | Another instance is already running | In cmd run: `netstat -ano \| findstr 5000` then `taskkill /F /PID <PID>` |
| `Resume extraction notice: scanned or empty` | PDF resume is an image scan without a text layer | Use a standard text-based PDF or enter skills manually in the form |
| `UnicodeEncodeError: 'charmap' codec` | Legacy Windows cmd code page | Handled automatically in code with UTF-8 encoding |

---

## 🎓 College Viva & Presentation Tips

1. **Why Flask instead of Django?**
   * *Answer:* Flask is lightweight, micro-framework oriented, easy to understand for presentation, and allows direct coupling with scikit-learn without heavy ORM overhead.
2. **Why TF-IDF + Cosine Similarity instead of Deep Learning / LLMs?**
   * *Answer:* It is 100% deterministic, explainable (you can prove why a career was recommended by looking at the dot product and matching skills), requires 0 GPU resources, has 0 external API cost, and directly fits the B.Tech Machine Learning syllabus.
3. **What happens if a student uploads an image-only resume?**
   * *Answer:* PyPDF2 detects the absence of extractable text and provides a graceful message alerting the user to use the manual entry fallback without crashing.
