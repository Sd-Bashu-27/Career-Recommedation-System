"""
AI-Based Career Path and Job Recommendation System
Main Flask Application

A Machine Learning project using Scikit-Learn (TF-IDF & Cosine Similarity),
Flask, SQLite, PyPDF2, and Chart.js.
Designed for 3rd Year B.Tech Computer Science & Engineering.
"""

import os
import csv
import json
from datetime import datetime
from flask import (
    Flask, render_template, request, redirect,
    url_for, flash, session, jsonify
)
from werkzeug.utils import secure_filename

# Import custom ML Engine modules
from ml_engine.recommender import CareerRecommender
from ml_engine.resume_parser import parse_resume
from ml_engine.database import (
    init_db, save_student_profile, get_student_profile,
    get_latest_student_profile, get_all_students, save_recommendation,
    get_recommendation_history, get_recommendation_by_id,
    save_roadmap_progress, get_roadmap_progress
)

# Initialize Flask application
app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "btech-ml-career-recommender-key-2026")
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024  # Max 5MB upload limit

# Resolve paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")
DATA_DIR = os.path.join(BASE_DIR, "data")
JOBS_CSV_PATH = os.path.join(DATA_DIR, "jobs.csv")
ROADMAPS_JSON_PATH = os.path.join(DATA_DIR, "roadmaps.json")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Automatically initialize SQLite Database tables on startup
init_db()

# Initialize ML Recommender instance (loads dataset & trains TF-IDF vectorizer)
recommender = CareerRecommender()


# Helper function to load demo jobs from CSV
def load_all_jobs():
    jobs = []
    if os.path.exists(JOBS_CSV_PATH):
        with open(JOBS_CSV_PATH, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Split skills into a list for easy badge rendering
                skills_raw = row.get("required_skills", "")
                row["skills_list"] = [s.strip() for s in skills_raw.split(",") if s.strip()]
                jobs.append(row)
    return jobs


# Helper function to load roadmaps from JSON
def load_roadmaps():
    if os.path.exists(ROADMAPS_JSON_PATH):
        with open(ROADMAPS_JSON_PATH, mode="r", encoding="utf-8") as f:
            return json.load(f)
    return {}


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    """Renders the Modern Dashboard Home Page."""
    return render_template("index.html")


@app.route("/profile")
def profile():
    """
    Renders the Student Profile and Resume Upload page.
    Pre-populates fields if a resume was just parsed or session exists.
    """
    profile_data = session.get("current_profile", {})
    detected_resume = session.get("detected_resume", None)
    return render_template("profile.html", profile_data=profile_data, detected_resume=detected_resume)


@app.route("/upload_resume", methods=["POST"])
def upload_resume():
    """
    Handles PDF resume uploads, extracts text using PyPDF2,
    and identifies matching technical skills.
    """
    if "resume_file" not in request.files:
        flash("No file was selected for upload.", "warning")
        return redirect(url_for("profile"))

    file = request.files["resume_file"]
    if file.filename == "":
        flash("No file was selected. Please choose a PDF file.", "warning")
        return redirect(url_for("profile"))

    if not file.filename.lower().endswith(".pdf"):
        flash("Invalid file format. Please upload a valid .PDF resume document.", "danger")
        return redirect(url_for("profile"))

    # Secure filename and save to static/uploads
    filename = secure_filename(file.filename)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    saved_filename = f"{timestamp}_{filename}"
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], saved_filename)
    
    try:
        file.save(file_path)
    except Exception as e:
        flash(f"Error saving upload: {str(e)}", "danger")
        return redirect(url_for("profile"))

    # Parse resume with PyPDF2
    parse_result = parse_resume(file_path)

    if not parse_result["success"]:
        flash(f"Resume text extraction notice: {parse_result['error']}", "warning")
        return redirect(url_for("profile"))

    # Populate session with extracted details
    skills_joined = ", ".join(parse_result["skills"])
    existing_profile = session.get("current_profile", {})
    existing_profile["skills"] = skills_joined
    if parse_result.get("education"):
        existing_profile["education"] = parse_result["education"]

    session["current_profile"] = existing_profile
    session["detected_resume"] = parse_result

    flash(
        f"Resume parsed successfully! Detected {parse_result['skills_count']} technical skills from your resume.",
        "success"
    )
    return redirect(url_for("profile"))


@app.route("/process_recommendations", methods=["POST"])
def process_recommendations():
    """
    Receives student profile form data, executes the Scikit-learn ML
    recommender, saves to SQLite, and redirects to the recommendations view.
    """
    name = request.form.get("name", "").strip()
    education = request.form.get("education", "").strip()
    skills = request.form.get("skills", "").strip()
    interests = request.form.get("interests", "").strip()
    preferred_role = request.form.get("preferred_role", "").strip()
    experience_level = request.form.get("experience_level", "Entry-Level / Fresher (0-1 Years)")

    if not name or not skills:
        flash("Please enter both your Name and at least one Technical Skill.", "danger")
        return redirect(url_for("profile"))

    # Save to SQLite Database
    try:
        student_id = save_student_profile(
            name=name,
            education=education,
            skills=skills,
            interests=interests,
            preferred_role=preferred_role,
            experience_level=experience_level
        )
    except Exception as e:
        student_id = 0

    # Run Machine Learning Recommender (TF-IDF + Cosine Similarity)
    ml_results = recommender.recommend(
        student_skills=skills,
        student_interests=interests,
        preferred_role=preferred_role,
        top_n=3
    )

    top_recs = ml_results["top_recommendations"]
    all_recs = ml_results["all_rankings"]

    top_role = top_recs[0]["role"] if top_recs else "Full Stack Developer"
    top_score = top_recs[0]["match_score"] if top_recs else 50.0
    matched_skills = top_recs[0]["matched_skills"] if top_recs else []
    missing_skills = top_recs[0]["missing_skills"] if top_recs else []

    # Save Recommendation to SQLite History
    rec_id = 0
    try:
        rec_id = save_recommendation(
            student_id=student_id,
            student_name=name,
            top_career=top_role,
            match_score=top_score,
            matched_skills=matched_skills,
            missing_skills=missing_skills,
            all_recommendations=all_recs
        )
    except Exception:
        pass

    # Store lightweight references in session
    session["active_rec_id"] = rec_id
    session["current_profile"] = {
        "id": student_id,
        "name": name,
        "education": education,
        "skills": skills,
        "interests": interests,
        "preferred_role": preferred_role,
        "experience_level": experience_level
    }

    flash(f"Career recommendations generated successfully for {name}!", "success")
    return redirect(url_for("recommendations"))


def get_active_recommendation():
    """
    Retrieves recommendation data for the active session without
    bloating client session cookies. Reads from SQLite or recomputes cleanly.
    """
    rec_id = session.get("active_rec_id")
    if rec_id:
        record = get_recommendation_by_id(rec_id)
        if record and record.get("all_recommendations"):
            return {
                "student_name": record.get("student_name", "Student"),
                "top_recommendations": record["all_recommendations"][:3],
                "all_rankings": record["all_recommendations"]
            }

    # Fallback to current profile or latest profile
    profile = session.get("current_profile") or get_latest_student_profile()
    if profile:
        name = profile.get("name", "Student")
        skills = profile.get("skills", "Python, SQL, HTML, CSS, JavaScript, React")
        interests = profile.get("interests", "")
        pref = profile.get("preferred_role", "")
    else:
        name = "Demo Student"
        skills = "Python, SQL, HTML, CSS, JavaScript, React, Machine Learning, Git"
        interests = "artificial intelligence, web applications, predictive models"
        pref = "Machine Learning Engineer"

    ml_results = recommender.recommend(skills, interests, pref, top_n=3)
    return {
        "student_name": name,
        "top_recommendations": ml_results["top_recommendations"],
        "all_rankings": ml_results["all_rankings"]
    }


@app.route("/recommendations")
def recommendations():
    """
    Displays the Top 3 ML Recommended Careers, matching scores,
    skill gap analysis, explanations, and Chart.js comparison graph.
    """
    rec_data = get_active_recommendation()

    # Prepare labels and values for Chart.js
    chart_labels = [r["role"] for r in rec_data["all_rankings"]]
    chart_scores = [r["match_score"] for r in rec_data["all_rankings"]]

    return render_template(
        "recommendations.html",
        student_name=rec_data["student_name"],
        top_recommendations=rec_data["top_recommendations"],
        all_rankings=rec_data["all_rankings"],
        chart_labels=chart_labels,
        chart_scores=chart_scores
    )


@app.route("/jobs")
def jobs():
    """
    Demonstrative Job Opportunities Portal.
    Allows filtering by career role, job type, and keyword search.
    """
    all_jobs = load_all_jobs()
    
    # Query parameters
    filter_role = request.args.get("role", "").strip()
    filter_type = request.args.get("type", "").strip()
    search_query = request.args.get("q", "").strip().lower()

    # Get student's current skills for matching highlights
    current_profile = session.get("current_profile", {})
    user_skills_raw = current_profile.get("skills", "")
    user_skills_lower = [s.strip().lower() for s in user_skills_raw.split(",") if s.strip()]

    filtered_jobs = []
    for j in all_jobs:
        # Filter by role
        if filter_role and j.get("career_role", "").lower() != filter_role.lower():
            continue
        # Filter by type
        if filter_type and filter_type.lower() not in j.get("job_type", "").lower():
            continue
        # Filter by keyword
        if search_query:
            combined_search_text = (
                f"{j.get('title','')} {j.get('company','')} {j.get('location','')} "
                f"{j.get('career_role','')} {j.get('required_skills','')}"
            ).lower()
            if search_query not in combined_search_text:
                continue
        filtered_jobs.append(j)

    # Distinct career roles for filter dropdown
    available_roles = sorted(list(set(j["career_role"] for j in all_jobs if j.get("career_role"))))

    return render_template(
        "jobs.html",
        jobs=filtered_jobs,
        available_roles=available_roles,
        selected_role=filter_role,
        selected_type=filter_type,
        query_search=request.args.get("q", ""),
        user_skills=user_skills_raw,
        user_skills_lower=user_skills_lower
    )


@app.route("/roadmap")
def roadmap():
    """
    Interactive Step-by-Step Learning Roadmap.
    Displays 3-phase curriculum with project ideas and progress checklist.
    """
    roadmaps_data = load_roadmaps()
    available_roles = list(roadmaps_data.keys())

    # Selected role: query param > top recommendation > first available
    role = request.args.get("role")
    if not role or role not in roadmaps_data:
        rec_data = session.get("recommendation_data")
        if rec_data and rec_data.get("top_recommendations"):
            candidate_role = rec_data["top_recommendations"][0]["role"]
            role = candidate_role if candidate_role in roadmaps_data else available_roles[0]
        else:
            role = available_roles[0] if available_roles else "Full Stack Developer"

    current_roadmap = roadmaps_data.get(role, {})

    # Calculate total milestones for progress tracker
    total_tasks = 0
    for stage in current_roadmap.get("stages", []):
        total_tasks += len(stage.get("tasks", []))

    # Retrieve completed tasks from database
    student_profile = session.get("current_profile", {})
    student_id = student_profile.get("id", 0)
    completed_tasks = get_roadmap_progress(student_id, role)

    return render_template(
        "roadmap.html",
        roadmap=current_roadmap,
        available_roles=available_roles,
        current_role=role,
        total_tasks=total_tasks,
        student_id=student_id,
        completed_tasks=completed_tasks
    )


@app.route("/api/save_roadmap_progress", methods=["POST"])
def save_roadmap_progress_api():
    """API endpoint to persist checked roadmap milestones in SQLite."""
    data = request.get_json() or {}
    role = data.get("role")
    completed_tasks = data.get("completed_tasks", [])

    student_profile = session.get("current_profile", {})
    student_id = student_profile.get("id", 0)

    if role:
        save_roadmap_progress(student_id, role, completed_tasks)
        return jsonify({"success": True, "count": len(completed_tasks)})
    return jsonify({"success": False, "error": "Missing role"}), 400


@app.route("/analytics")
def analytics():
    """
    Dedicated Career Analytics & Visual Skill Gap Dashboard.
    Generates data for Chart.js radar, doughnut, and bar charts.
    """
    rec_data = get_active_recommendation()
    top_recs = rec_data.get("top_recommendations", [])
    top_rec = top_recs[0] if top_recs else {}
    matched_skills = top_rec.get("matched_skills", [])
    missing_skills = top_rec.get("missing_skills", [])

    # Compute Domain Coverage for Radar Chart
    categories = [
        "Web Development", "AI / Machine Learning", "Data & Analytics",
        "Cloud & DevOps", "Cybersecurity", "Mobile & UI/UX"
    ]
    
    # Calculate candidate affinity for each domain based on matched skills
    user_skills_str = session.get("current_profile", {}).get("skills", "").lower()
    
    domain_weights = {
        "Web Development": ["html", "css", "javascript", "react", "node", "express", "sql"],
        "AI / Machine Learning": ["python", "machine learning", "scikit-learn", "pandas", "numpy", "deep learning"],
        "Data & Analytics": ["sql", "excel", "power bi", "tableau", "statistics", "pandas"],
        "Cloud & DevOps": ["aws", "azure", "docker", "kubernetes", "linux", "git", "ci/cd"],
        "Cybersecurity": ["network security", "linux", "wireshark", "ethical hacking", "cryptography"],
        "Mobile & UI/UX": ["flutter", "react native", "figma", "mobile ui", "dart", "kotlin"]
    }

    radar_values = []
    for cat in categories:
        keywords = domain_weights[cat]
        matches = sum(1 for kw in keywords if kw in user_skills_str)
        score = min(100, int((matches / len(keywords)) * 100) + 15)  # baseline 15%
        radar_values.append(score)

    all_rankings = rec_data.get("all_rankings", [])
    rank_labels = [r.get("role", "") for r in all_rankings]
    rank_scores = [r.get("match_score", 0) for r in all_rankings]

    return render_template(
        "analytics.html",
        student_name=rec_data.get("student_name", "Student"),
        top_role=top_rec.get("role", "Full Stack Developer"),
        top_score=top_rec.get("match_score", 50.0),
        user_skills_count=len(matched_skills),
        missing_count=len(missing_skills),
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        radar_categories=categories,
        radar_values=radar_values,
        rank_labels=rank_labels,
        rank_scores=rank_scores
    )


@app.route("/history")
def history():
    """Displays past student evaluations stored in SQLite."""
    records = get_recommendation_history()
    return render_template("history.html", history_records=records)


@app.route("/history/<int:record_id>")
def view_history_item(record_id):
    """Restores a past evaluation from SQLite into the active session."""
    record = get_recommendation_by_id(record_id)
    if not record:
        flash("Record not found in database.", "warning")
        return redirect(url_for("history"))

    session["active_rec_id"] = record_id
    flash(f"Loaded assessment report for {record.get('student_name')}.", "info")
    return redirect(url_for("recommendations"))


@app.route("/about")
def about():
    """Renders the Academic Documentation and ML Methodology Guide."""
    return render_template("about.html")


# Error Handlers
@app.errorhandler(404)
def not_found(e):
    return render_template("index.html"), 404


@app.errorhandler(500)
def server_error(e):
    flash("An unexpected server error occurred. Please try again.", "danger")
    return redirect(url_for("index"))


# ---------------------------------------------------------------------------
# Application Entrypoint
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Support dynamic PORT and HOST provided by cloud platforms like Render
    port = int(os.environ.get("PORT", 5000))
    host = os.environ.get("HOST", "0.0.0.0")
    debug_mode = os.environ.get("FLASK_DEBUG", "False").lower() in ("true", "1", "t")

    print("==================================================================")
    print("AI-Based Career Path and Job Recommendation System")
    print(f"Running at: http://{host}:{port}")
    print("Machine Learning Subject Project (B.Tech CSE 3rd Year)")
    print("==================================================================")
    app.run(host=host, port=port, debug=debug_mode)
