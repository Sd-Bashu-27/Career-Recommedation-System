"""
Automated Test Suite for AI-Based Career Path and Job Recommendation System
Validates all Flask endpoints, ML Recommendation Engine, SQLite Operations,
and PyPDF2 text extraction.
"""

import os
import sys
import unittest

# Ensure root directory is on Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app
from ml_engine.recommender import CareerRecommender
from ml_engine.database import init_db, get_recommendation_history, get_latest_student_profile


class TestCareerRecommendationSystem(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        init_db()
        cls.client = app.test_client()
        cls.recommender = CareerRecommender()

    def test_01_home_page(self):
        """Test home dashboard route loads properly."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"CareerAI Navigator", response.data)
        self.assertIn(b"AI-Based Career Path", response.data)

    def test_02_profile_page(self):
        """Test student profile & resume upload page loads."""
        response = self.client.get("/profile")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Student Profile", response.data)
        self.assertIn(b"Technical Skills", response.data)

    def test_03_recommender_algorithm(self):
        """Test the ML recommender with varying skill inputs."""
        # 1. Full Stack Developer profile
        result_fs = self.recommender.recommend(
            student_skills="HTML, CSS, JavaScript, React, Node.js, SQL, Git",
            student_interests="web development, building full-stack apps",
            preferred_role="Full Stack Developer"
        )
        self.assertTrue(len(result_fs["top_recommendations"]) >= 3)
        self.assertEqual(result_fs["top_recommendations"][0]["role"], "Full Stack Developer")
        self.assertTrue(result_fs["top_recommendations"][0]["match_score"] > 60)

        # 2. Machine Learning Engineer profile
        result_ml = self.recommender.recommend(
            student_skills="Python, Scikit-learn, Pandas, NumPy, Machine Learning, Linear Algebra",
            student_interests="artificial intelligence, predictive modeling",
            preferred_role="Machine Learning Engineer"
        )
        self.assertEqual(result_ml["top_recommendations"][0]["role"], "Machine Learning Engineer")
        self.assertTrue(result_ml["top_recommendations"][0]["match_score"] > 60)

        # 3. Cybersecurity profile
        result_sec = self.recommender.recommend(
            student_skills="Network Security, Linux, Wireshark, Ethical Hacking, Cryptography",
            student_interests="cybersecurity, network defense",
            preferred_role="Cybersecurity Analyst"
        )
        self.assertEqual(result_sec["top_recommendations"][0]["role"], "Cybersecurity Analyst")

    def test_04_form_submission_and_recommendations(self):
        """Test form submission creates database record and redirects to recommendations."""
        form_data = {
            "name": "Test Student Rahul",
            "education": "B.Tech (Computer Science / IT)",
            "skills": "Python, SQL, Pandas, NumPy, Scikit-learn, Git",
            "interests": "data analysis, machine learning",
            "preferred_role": "Data Analyst",
            "experience_level": "Entry-Level / Fresher (0-1 Years)"
        }
        post_resp = self.client.post("/process_recommendations", data=form_data, follow_redirects=True)
        self.assertEqual(post_resp.status_code, 200)
        self.assertIn(b"ML Career Recommendations", post_resp.data)
        self.assertIn(b"Test Student Rahul", post_resp.data)

    def test_05_jobs_portal(self):
        """Test jobs portal with filtering."""
        resp = self.client.get("/jobs")
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"Demonstrative Job Opportunities", resp.data)

        # Filter by specific role
        resp_filtered = self.client.get("/jobs?role=Full+Stack+Developer")
        self.assertEqual(resp_filtered.status_code, 200)
        self.assertIn(b"Full Stack", resp_filtered.data)

    def test_06_roadmap(self):
        """Test roadmap view for roles."""
        resp = self.client.get("/roadmap?role=Full+Stack+Developer")
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"Full Stack Developer", resp.data)
        self.assertIn(b"Phase 1", resp.data)

        # Test roadmap progress API
        api_resp = self.client.post("/api/save_roadmap_progress", json={
            "role": "Full Stack Developer",
            "completed_tasks": ["fs_task1", "fs_task2"]
        })
        self.assertEqual(api_resp.status_code, 200)
        data = api_resp.get_json()
        self.assertTrue(data["success"])
        self.assertEqual(data["count"], 2)

    def test_07_analytics_page(self):
        """Test analytics page renders charts data."""
        resp = self.client.get("/analytics")
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"Career Analytics", resp.data)
        self.assertIn(b"skillsGapChart", resp.data)
        self.assertIn(b"domainRadarChart", resp.data)

    def test_08_history_page(self):
        """Test history logs past submissions in SQLite."""
        resp = self.client.get("/history")
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"Saved Recommendation History", resp.data)
        self.assertIn(b"Test Student Rahul", resp.data)

    def test_09_about_page(self):
        """Test about and academic documentation page."""
        resp = self.client.get("/about")
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"Project Abstract", resp.data)
        self.assertIn(b"TF-IDF Feature Representation", resp.data)

    def test_10_resume_upload(self):
        """Test PDF resume upload route and parsing."""
        sample_pdf_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sample_resumes", "sample_student_resume.pdf")
        if os.path.exists(sample_pdf_path):
            with open(sample_pdf_path, "rb") as pdf_file:
                resp = self.client.post("/upload_resume", data={
                    "resume_file": (pdf_file, "sample_student_resume.pdf")
                }, follow_redirects=True)
                self.assertEqual(resp.status_code, 200)
                self.assertIn(b"Resume parsed successfully", resp.data)


if __name__ == "__main__":
    unittest.main()

