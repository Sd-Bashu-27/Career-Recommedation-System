"""
Machine Learning Recommender Engine
Uses Scikit-learn's TfidfVectorizer and Cosine Similarity to recommend
optimal career paths based on user skills, interests, and profile data.
Also calculates skill overlap, skill gaps, and provides transparent explanations.
"""

import os
import re
import math
try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False
    import csv


class CareerRecommender:
    def __init__(self, data_path=None):
        """
        Initializes the career recommender system with the careers dataset.
        """
        if data_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            data_path = os.path.join(base_dir, "data", "careers.csv")
            
        self.data_path = data_path
        self.careers_df = None
        self.careers_list = []
        self.vectorizer = None
        self.career_vectors = None
        self.use_sklearn = True
        
        self.load_dataset()
        self.train_model()

    def load_dataset(self):
        """Loads and cleans the career dataset from CSV."""
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"Careers dataset not found at: {self.data_path}")
            
        if HAS_PANDAS:
            self.careers_df = pd.read_csv(self.data_path)
            self.careers_df["combined_features"] = self.careers_df.apply(
                lambda row: (
                    f"{str(row['required_skills'])} "
                    f"{str(row['required_skills'])} "
                    f"{str(row['interests'])} "
                    f"{str(row['role'])} "
                    f"{str(row['category'])} "
                    f"{str(row['description'])}"
                ).lower(),
                axis=1
            )
            self.careers_list = self.careers_df.to_dict(orient="records")
        else:
            self.careers_list = []
            with open(self.data_path, mode="r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    row["combined_features"] = (
                        f"{str(row.get('required_skills', ''))} "
                        f"{str(row.get('required_skills', ''))} "
                        f"{str(row.get('interests', ''))} "
                        f"{str(row.get('role', ''))} "
                        f"{str(row.get('category', ''))} "
                        f"{str(row.get('description', ''))}"
                    ).lower()
                    self.careers_list.append(row)


    def train_model(self):
        """
        Initializes and fits the TF-IDF Vectorizer on all career feature documents.
        """
        try:
            from sklearn.feature_extraction.text import TfidfVectorizer
            from sklearn.metrics.pairwise import cosine_similarity
            
            self.use_sklearn = True
            # Regex pattern preserves C++, C#, .NET, Node.js etc.
            token_pattern = r"(?u)\b[a-zA-Z0-9_+#\.]+\b"
            self.vectorizer = TfidfVectorizer(
                token_pattern=token_pattern,
                ngram_range=(1, 2),
                stop_words="english"
            )
            features = [r["combined_features"] for r in self.careers_list]
            self.career_vectors = self.vectorizer.fit_transform(features)
            self.cosine_similarity_fn = cosine_similarity
        except Exception:
            # Fallback to pure-Python TF-IDF vectorizer if scikit-learn is unavailable
            self.use_sklearn = False
            self._fit_custom_tfidf()

    def _fit_custom_tfidf(self):
        """
        Pure-Python fallback implementation of TF-IDF and Cosine Similarity
        for mathematical transparency and zero-dependency resilience.
        """
        corpus = [r["combined_features"] for r in self.careers_list]
        self.doc_tokens = []
        self.vocab = set()
        
        for doc in corpus:
            tokens = re.findall(r"[a-zA-Z0-9_+#\.]+", doc.lower())
            self.doc_tokens.append(tokens)
            self.vocab.update(tokens)
            
        self.vocab = sorted(list(self.vocab))
        self.vocab_index = {word: i for i, word in enumerate(self.vocab)}
        
        # Compute Document Frequencies (DF)
        N = len(corpus)
        self.idf = {}
        for word in self.vocab:
            df = sum(1 for tokens in self.doc_tokens if word in tokens)
            self.idf[word] = math.log((1 + N) / (1 + df)) + 1.0

        # Vectorize career documents
        self.career_vectors = []
        for tokens in self.doc_tokens:
            vec = self._vectorize_tokens(tokens)
            self.career_vectors.append(vec)

    def _vectorize_tokens(self, tokens):
        """Transforms tokens into a normalized TF-IDF vector."""
        tf = {}
        for token in tokens:
            tf[token] = tf.get(token, 0) + 1
            
        total_tokens = len(tokens) if tokens else 1
        vec = {}
        norm_sq = 0.0
        for token, count in tf.items():
            if token in self.idf:
                weight = (count / total_tokens) * self.idf[token]
                vec[token] = weight
                norm_sq += weight * weight
                
        norm = math.sqrt(norm_sq) if norm_sq > 0 else 1.0
        return {token: w / norm for token, w in vec.items()}

    def _custom_cosine_similarity(self, user_vec, career_vec):
        """Computes cosine similarity between two normalized sparse vectors."""
        dot_product = sum(user_vec[t] * career_vec[t] for t in user_vec if t in career_vec)
        return max(0.0, min(1.0, dot_product))

    def _parse_skills_list(self, skills_string):
        """Converts comma/newline separated skills string into a cleaned set of skills."""
        if not skills_string:
            return set()
        parts = re.split(r"[,;\n\r]+", skills_string)
        cleaned = set()
        for p in parts:
            p_strip = p.strip()
            if p_strip:
                cleaned.add(p_strip)
        return cleaned

    def recommend(self, student_skills, student_interests="", preferred_role="", top_n=3):
        """
        Generates ML career recommendations using TF-IDF and Cosine Similarity.
        
        Returns:
            list of dicts containing top recommended careers, matching scores,
            matched skills, missing skills, and detailed explanations.
        """
        # Parse student inputs
        student_skills_set = self._parse_skills_list(student_skills)
        student_interests_set = self._parse_skills_list(student_interests)
        
        # Build student feature string
        # Emphasize skills by duplicating
        student_features = (
            f"{student_skills} {student_skills} "
            f"{student_interests} "
            f"{preferred_role}"
        ).lower().strip()

        if not student_features:
            student_features = "programming computer science software"

        # Calculate cosine similarity scores
        if self.use_sklearn:
            user_vector = self.vectorizer.transform([student_features])
            sim_scores = self.cosine_similarity_fn(user_vector, self.career_vectors).flatten()
        else:
            tokens = re.findall(r"[a-zA-Z0-9_+#\.]+", student_features)
            user_vec = self._vectorize_tokens(tokens)
            sim_scores = [self._custom_cosine_similarity(user_vec, c_vec) for c_vec in self.career_vectors]

        recommendations = []
        
        for idx, row in enumerate(self.careers_list):
            cosine_score = float(sim_scores[idx])
            career_skills = self._parse_skills_list(row["required_skills"])
            
            # Find matched skills (case-insensitive comparison)
            student_skills_lower = {s.lower(): s for s in student_skills_set}
            career_skills_lower = {s.lower(): s for s in career_skills}
            
            matched = []
            missing = []
            
            for c_lower, c_orig in career_skills_lower.items():
                # Check for direct match or substring match (e.g. "React" in "React.js")
                match_found = False
                for u_lower, u_orig in student_skills_lower.items():
                    if u_lower == c_lower or u_lower in c_lower or c_lower in u_lower:
                        matched.append(c_orig)
                        match_found = True
                        break
                if not match_found:
                    missing.append(c_orig)

            # Skill coverage percentage
            coverage_ratio = len(matched) / len(career_skills) if career_skills else 0.0
            
            # Blend: 65% ML Cosine Similarity + 35% Direct Skill Coverage
            # Give a slight boost if the user explicitly chose this as their preferred role
            preference_boost = 0.08 if (preferred_role and preferred_role.lower() in row["role"].lower()) else 0.0
            
            raw_score = (cosine_score * 0.65) + (coverage_ratio * 0.35) + preference_boost
            
            # Scale to percentage between 15% and 98% for realistic display
            # (100% is reserved to emphasize that match score is not guaranteed hiring probability)
            final_percentage = min(98.0, max(15.0, raw_score * 100))
            final_score = round(final_percentage, 1)

            # Generate natural language explanation for College presentation
            explanation = self._generate_explanation(
                role=row["role"],
                score=final_score,
                matched=matched,
                missing=missing,
                interests=student_interests_set
            )

            recommendations.append({
                "career_id": int(row["career_id"]),
                "role": row["role"],
                "category": row["category"],
                "match_score": final_score,
                "cosine_similarity": round(cosine_score, 3),
                "matched_skills": sorted(matched),
                "missing_skills": sorted(missing),
                "required_skills": sorted(list(career_skills)),
                "matched_count": len(matched),
                "required_count": len(career_skills),
                "avg_salary": row["avg_salary_inr"],
                "demand_level": row["demand_level"],
                "description": row["description"],
                "top_companies": row["top_companies"],
                "tools": row["tools"],
                "explanation": explanation
            })

        # Sort descending by match_score
        recommendations.sort(key=lambda x: x["match_score"], reverse=True)
        
        # Return top N recommendations plus complete rankings for charts
        return {
            "top_recommendations": recommendations[:top_n],
            "all_rankings": recommendations
        }

    def _generate_explanation(self, role, score, matched, missing, interests):
        """Generates clear, explainable reasoning for the recommendation."""
        matched_str = ", ".join(matched[:3]) if matched else "foundational engineering aptitude"
        missing_count = len(missing)
        
        if score >= 75:
            fit_text = "Strong Profile Alignment"
            reason = f"Your demonstrated proficiency in {matched_str} closely aligns with the technical demands of a {role}."
        elif score >= 50:
            fit_text = "Moderate Profile Fit"
            reason = f"You hold a solid baseline with skills like {matched_str}. Gaining familiarity with {missing_count} core tools will rapidly elevate your job readiness."
        else:
            fit_text = "Emerging Potential"
            reason = f"This path introduces new opportunities. Bridging {missing_count} essential skill gaps will position you strongly for entry-level roles."

        explanation = (
            f"**{fit_text} ({score}% Match):** {reason} "
            f"Key next steps: Focus on mastering {', '.join(missing[:3]) if missing else 'advanced concepts'} to complete your preparation."
        )
        return explanation
