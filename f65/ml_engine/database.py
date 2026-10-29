"""
Database Module for SQLite
Manages persistent storage for Student Profiles, Recommendation History,
and Learning Roadmap Progress. Auto-initializes on startup.
"""

import os
import sqlite3
import json
from datetime import datetime

# Resolve database directory and path relative to workspace
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_DIR = os.path.join(BASE_DIR, "database")
DB_PATH = os.path.join(DB_DIR, "career_system.db")


def get_db_connection():
    """Returns a SQLite connection with row factory configured."""
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """
    Initializes database tables if they do not exist.
    Handles empty data and ensures zero-downtime startup.
    """
    os.makedirs(DB_DIR, exist_ok=True)
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Students Profile Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT,
        education TEXT,
        skills TEXT,
        interests TEXT,
        preferred_role TEXT,
        experience_level TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 2. Recommendations History Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS recommendation_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        student_name TEXT,
        top_career TEXT NOT NULL,
        match_score REAL NOT NULL,
        matched_skills TEXT,
        missing_skills TEXT,
        all_recommendations_json TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (student_id) REFERENCES students (id)
    );
    """)

    # 3. Roadmap Progress Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS roadmap_progress (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        career_role TEXT NOT NULL,
        completed_task_ids TEXT,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    conn.commit()
    conn.close()


def save_student_profile(name, education, skills, interests="", preferred_role="", experience_level="Entry-Level", email=""):
    """
    Inserts or updates a student profile in the database.
    Returns the student_id.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO students (name, email, education, skills, interests, preferred_role, experience_level)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (name, email, education, skills, interests, preferred_role, experience_level))
    
    student_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return student_id


def get_student_profile(student_id):
    """Retrieves a single student profile by ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def get_latest_student_profile():
    """Retrieves the most recently created or updated student profile."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def get_all_students(limit=50):
    """Retrieves a list of recent student profiles."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students ORDER BY id DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def save_recommendation(student_id, student_name, top_career, match_score, matched_skills, missing_skills, all_recommendations):
    """
    Saves an ML recommendation result into recommendation_history.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    matched_str = ", ".join(matched_skills) if isinstance(matched_skills, list) else str(matched_skills)
    missing_str = ", ".join(missing_skills) if isinstance(missing_skills, list) else str(missing_skills)
    json_data = json.dumps(all_recommendations)

    cursor.execute("""
        INSERT INTO recommendation_history 
        (student_id, student_name, top_career, match_score, matched_skills, missing_skills, all_recommendations_json)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (student_id, student_name, top_career, match_score, matched_str, missing_str, json_data))

    rec_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return rec_id


def get_recommendation_history(limit=25):
    """Retrieves the history of generated recommendations."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, student_id, student_name, top_career, match_score, matched_skills, missing_skills, created_at
        FROM recommendation_history
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_recommendation_by_id(rec_id):
    """Retrieves a specific recommendation record with full JSON details."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM recommendation_history WHERE id = ?", (rec_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return None
    d = dict(row)
    if d.get("all_recommendations_json"):
        try:
            d["all_recommendations"] = json.loads(d["all_recommendations_json"])
        except Exception:
            d["all_recommendations"] = []
    return d


def save_roadmap_progress(student_id, career_role, completed_tasks):
    """Saves or updates completed task IDs for a career roadmap."""
    conn = get_db_connection()
    cursor = conn.cursor()
    tasks_str = ",".join(completed_tasks) if isinstance(completed_tasks, list) else str(completed_tasks)

    # Check if entry already exists
    cursor.execute("""
        SELECT id FROM roadmap_progress 
        WHERE student_id = ? AND career_role = ?
    """, (student_id, career_role))
    row = cursor.fetchone()

    if row:
        cursor.execute("""
            UPDATE roadmap_progress
            SET completed_task_ids = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (tasks_str, row["id"]))
    else:
        cursor.execute("""
            INSERT INTO roadmap_progress (student_id, career_role, completed_task_ids)
            VALUES (?, ?, ?)
        """, (student_id, career_role, tasks_str))

    conn.commit()
    conn.close()


def get_roadmap_progress(student_id, career_role):
    """Retrieves the list of completed task IDs for a roadmap."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT completed_task_ids FROM roadmap_progress
        WHERE student_id = ? AND career_role = ?
        ORDER BY id DESC LIMIT 1
    """, (student_id, career_role))
    row = cursor.fetchone()
    conn.close()
    if row and row["completed_task_ids"]:
        return [t.strip() for t in row["completed_task_ids"].split(",") if t.strip()]
    return []
