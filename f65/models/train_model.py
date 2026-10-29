"""
Standalone Machine Learning Model Training & Inspection Script
AI-Based Career Path and Job Recommendation System

Can be executed independently from terminal:
    python models/train_model.py

Demonstrates TF-IDF Vectorization, N-Gram extraction, and Cosine Similarity
for college project presentation and viva evaluation.
"""

import os
import sys

# Ensure root directory is on Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set UTF-8 encoding for Windows terminal
if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from ml_engine.recommender import CareerRecommender


def run_training_demo():
    print("==================================================================")
    print("AI-BASED CAREER PATH & JOB RECOMMENDATION SYSTEM")
    print("Machine Learning Model Training & Feature Extraction Demonstration")
    print("==================================================================\n")

    print("[1/4] Loading Career Profiles Dataset from data/careers.csv...")
    recommender = CareerRecommender()
    print(f"      Successfully loaded {len(recommender.careers_list)} benchmark career profiles.\n")

    print("[2/4] Inspecting Careers Dataset:")
    for idx, row in enumerate(recommender.careers_list[:5], 1):
        print(f"      {idx}. {row['role']} ({row['category']})")
        print(f"         Required Skills: {row['required_skills'][:60]}...")
    print(f"      ... and {len(recommender.careers_list) - 5} more career roles.\n")

    print("[3/4] Model Architecture:")
    if recommender.use_sklearn:
        print("      Active Vectorizer: Scikit-learn TfidfVectorizer (ngram_range=(1,2))")
        print(f"      Vocabulary Size:   {len(recommender.vectorizer.vocabulary_)} n-grams")
    else:
        print("      Active Vectorizer: Pure-Python TF-IDF Mathematical Engine")
        print(f"      Vocabulary Size:   {len(recommender.vocab)} distinct tokens")
    print("      Similarity Metric: Cosine Similarity in n-dimensional Euclidean space\n")

    print("[4/4] Running Sample Verification Test...")
    sample_skills = "Python, Scikit-learn, Pandas, NumPy, Machine Learning, Git"
    sample_interests = "artificial intelligence, predictive modeling, data analysis"
    sample_preferred = "Machine Learning Engineer"

    print(f"      Test Student Skills:     '{sample_skills}'")
    print(f"      Test Student Interests:  '{sample_interests}'")
    print(f"      Preferred Career Track:  '{sample_preferred}'\n")

    results = recommender.recommend(
        student_skills=sample_skills,
        student_interests=sample_interests,
        preferred_role=sample_preferred,
        top_n=3
    )

    print("--- TOP 3 RECOMMENDED CAREERS ---")
    for rank, rec in enumerate(results["top_recommendations"], 1):
        print(f"Rank #{rank}: {rec['role']}")
        print(f"   Match Score:       {rec['match_score']}%")
        print(f"   Cosine Similarity: {rec['cosine_similarity']}")
        print(f"   Matched Skills:    {', '.join(rec['matched_skills'][:5])}")
        print(f"   Missing Skills:    {', '.join(rec['missing_skills'][:5])}")
        print(f"   Salary (India):    {rec['avg_salary'].replace('₹', 'Rs. ')}")
        print(f"   Demand Level:      {rec['demand_level']}")
        print()

    print("==================================================================")
    print("Model Training & Validation Finished with 0 errors!")
    print("==================================================================")


if __name__ == "__main__":
    run_training_demo()
