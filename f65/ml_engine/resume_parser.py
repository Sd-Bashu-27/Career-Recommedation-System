"""
Resume Parser Module
Extracts textual content from PDF resumes using PyPDF2 and
identifies relevant technical skills, education keywords, and experience indicators.
Provides graceful fallbacks and error handling.
"""

import os
import re

# Comprehensive skill ontology for matching keywords accurately
SKILL_DICTIONARY = [
    # Programming Languages
    "Python", "Java", "C++", "C", "C#", "JavaScript", "TypeScript", "PHP", "Ruby",
    "Go", "Rust", "Kotlin", "Swift", "Dart", "SQL", "HTML", "CSS", "Bash", "R",
    
    # Web & Frontend / Backend Frameworks
    "React", "Node.js", "Express", "Flask", "Django", "FastAPI", "Spring Boot",
    "Angular", "Vue", "Bootstrap", "Tailwind CSS", "Next.js", "jQuery", "ASP.NET",
    
    # Data Science & Machine Learning
    "Machine Learning", "Deep Learning", "Scikit-learn", "TensorFlow", "PyTorch",
    "Pandas", "NumPy", "Keras", "OpenCV", "Matplotlib", "Seaborn", "Power BI",
    "Tableau", "Excel", "Apache Spark", "Hadoop", "Kafka", "ETL", "Statistics",
    "Data Analysis", "Data Visualization", "Natural Language Processing", "NLP",
    "Computer Vision", "Linear Algebra", "Data Mining",
    
    # Databases & Storage
    "MySQL", "PostgreSQL", "SQLite", "MongoDB", "Redis", "Firebase", "Oracle",
    "Cassandra", "Data Warehousing",
    
    # Cloud & DevOps
    "AWS", "Azure", "GCP", "Cloud Computing", "Docker", "Kubernetes", "Git",
    "GitHub", "CI/CD", "Jenkins", "Linux", "Terraform", "Ansible", "Nginx",
    
    # Cybersecurity & Networking
    "Network Security", "Ethical Hacking", "Cryptography", "Wireshark", "Nmap",
    "Metasploit", "Burp Suite", "Information Security", "Firewall", "Vulnerability Assessment",
    
    # Mobile & UI/UX
    "Flutter", "React Native", "Android", "iOS", "Figma", "Adobe XD",
    "Wireframing", "Prototyping", "User Research", "Mobile UI Design", "Responsive Web Design",
    
    # General Engineering & Concepts
    "REST API", "GraphQL", "Microservices", "Object Oriented Programming",
    "OOP", "Data Structures", "Algorithms", "Unit Testing", "System Design",
    "Agile", "Scrum"
]

EDUCATION_PATTERNS = [
    (r"\b(B\.Tech|BTech|Bachelor of Technology)\b", "B.Tech (Computer Science / IT)"),
    (r"\b(B\.E\.|B\.E|Bachelor of Engineering)\b", "B.E. (Computer Science / IT)"),
    (r"\b(BCA|Bachelor of Computer Applications)\b", "BCA (Computer Applications)"),
    (r"\b(MCA|Master of Computer Applications)\b", "MCA (Computer Applications)"),
    (r"\b(M\.Tech|MTech|Master of Technology)\b", "M.Tech (Computer Science)"),
    (r"\b(B\.Sc|BSc|Bachelor of Science)\b", "B.Sc (Computer Science / IT)"),
    (r"\b(M\.Sc|MSc|Master of Science)\b", "M.Sc (Computer Science / IT)"),
    (r"\b(Diploma in (CSE|Computer|IT))\b", "Diploma (Polytechnic CSE/IT)")
]


def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a given PDF file path using PyPDF2.
    Returns (success_boolean, extracted_text_or_error_message).
    """
    if not os.path.exists(pdf_path):
        return False, "File does not exist on the server."

    try:
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=DeprecationWarning)
            try:
                import pypdf as pdf_lib
            except ImportError:
                import PyPDF2 as pdf_lib
    except ImportError:
        return False, "PyPDF2 is not installed. Please enter skills manually."

    extracted_text = []
    try:
        with open(pdf_path, "rb") as file:
            reader = pdf_lib.PdfReader(file)
            num_pages = len(reader.pages)
            
            if num_pages == 0:
                return False, "Uploaded PDF file appears to be completely empty."
            
            for page_num in range(num_pages):
                page = reader.pages[page_num]
                page_text = page.extract_text()
                if page_text:
                    extracted_text.append(page_text)
                    
        full_text = "\n".join(extracted_text).strip()
        if not full_text or len(full_text) < 15:
            return False, "Could not extract readable text. The PDF might be scanned or image-only. Please enter skills manually."
            
        return True, full_text

    except Exception as e:
        return False, f"Failed to parse PDF: {str(e)}. Please enter skills manually."


def extract_skills_and_details(text):
    """
    Analyzes raw text to detect skills, educational degree, and basic statistics.
    Returns a dictionary of structured profile information.
    """
    if not text:
        return {
            "skills": [],
            "education": "",
            "word_count": 0,
            "detected_roles": []
        }

    # Normalize text for matching
    cleaned_text = " " + text.replace("\n", " ").replace("\r", " ") + " "
    
    detected_skills = set()
    
    for skill in SKILL_DICTIONARY:
        # Create regular expression with word boundaries where appropriate
        # Handle special characters like C++, C#, .NET
        escaped_skill = re.escape(skill)
        
        # Word boundary pattern that also respects symbols like C++ or Node.js
        pattern = rf"(?i)(?<=[\s,;:(/]){escaped_skill}(?=[\s,;:)/]|$)"
        if re.search(pattern, cleaned_text):
            detected_skills.add(skill)
        else:
            # Secondary check for exact word boundary
            word_pattern = rf"(?i)\b{escaped_skill}\b"
            if re.search(word_pattern, cleaned_text):
                detected_skills.add(skill)

    # Detect Education level
    detected_education = "B.Tech (Computer Science / IT)"  # reasonable student default
    for regex, degree_name in EDUCATION_PATTERNS:
        if re.search(regex, text, re.IGNORECASE):
            detected_education = degree_name
            break

    # Calculate word count
    words = [w for w in text.split() if len(w) > 1]
    word_count = len(words)

    # Sort detected skills alphabetically
    sorted_skills = sorted(list(detected_skills))

    return {
        "skills": sorted_skills,
        "education": detected_education,
        "word_count": word_count
    }


def parse_resume(file_path):
    """
    Master function: Reads PDF, extracts text, detects skills and metadata.
    Returns a comprehensive result dictionary.
    """
    success, result = extract_text_from_pdf(file_path)
    if not success:
        return {
            "success": False,
            "error": result,
            "skills": [],
            "education": "",
            "raw_text": "",
            "skills_count": 0
        }

    analysis = extract_skills_and_details(result)
    
    return {
        "success": True,
        "error": None,
        "skills": analysis["skills"],
        "education": analysis["education"],
        "word_count": analysis["word_count"],
        "skills_count": len(analysis["skills"]),
        "raw_text_snippet": result[:400] + ("..." if len(result) > 400 else "")
    }
