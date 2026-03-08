"""
JanSahay AI - ML-Based Recommendation Engine
Recommends government schemes based on user profile, location, and socio-economic factors.
Uses TF-IDF + cosine similarity for text matching and weighted scoring for profile matching.
"""

import math
import re
from typing import Dict, List, Optional, Tuple
from collections import Counter


class SchemeRecommender:
    """
    Hybrid recommendation engine combining:
    1. Profile-based scoring (demographic matching)
    2. Content-based filtering (TF-IDF text similarity)
    3. Popularity-based boosting
    """

    # Weights for different matching dimensions
    WEIGHTS = {
        "state_match": 0.15,
        "age_match": 0.12,
        "income_match": 0.15,
        "gender_match": 0.10,
        "caste_match": 0.12,
        "occupation_match": 0.10,
        "rural_match": 0.08,
        "bpl_match": 0.08,
        "text_similarity": 0.05,
        "popularity": 0.05,
    }

    def __init__(self):
        self._idf_cache: Dict[str, float] = {}
        self._total_docs = 0

    def recommend(
        self,
        user_profile: dict,
        schemes: List[dict],
        query_text: Optional[str] = None,
        top_k: int = 10,
    ) -> List[dict]:
        """
        Recommend top-K schemes for a user.

        Args:
            user_profile: User demographic data
            schemes: List of scheme dicts with eligibility_rules
            query_text: Optional search query for text matching
            top_k: Number of recommendations to return

        Returns:
            Ranked list of scheme dicts with match_score
        """
        scored_schemes = []

        # Build IDF from scheme descriptions if query provided
        if query_text:
            self._build_idf([s.get("description_en", "") for s in schemes])

        for scheme in schemes:
            if not scheme.get("is_active", True):
                continue

            score = self._calculate_match_score(user_profile, scheme, query_text)
            scored_schemes.append({
                **scheme,
                "match_score": round(score, 4),
            })

        # Sort by score descending
        scored_schemes.sort(key=lambda x: x["match_score"], reverse=True)
        return scored_schemes[:top_k]

    def _calculate_match_score(
        self, profile: dict, scheme: dict, query_text: Optional[str]
    ) -> float:
        """Calculate composite match score between user profile and scheme."""
        rules = scheme.get("eligibility_rules") or {}
        score = 0.0

        # --- State Match ---
        target_state = scheme.get("target_state")
        user_state = profile.get("state", "")
        if target_state is None:
            # All-India scheme gets full points
            score += self.WEIGHTS["state_match"]
        elif user_state and user_state.lower() == target_state.lower():
            score += self.WEIGHTS["state_match"]
        elif user_state and target_state:
            # State mismatch for state-specific scheme
            score -= self.WEIGHTS["state_match"] * 0.5

        # --- Age Match ---
        user_age = profile.get("age")
        if user_age is not None:
            min_age = rules.get("min_age", 0)
            max_age = rules.get("max_age", 150)
            if min_age <= user_age <= max_age:
                score += self.WEIGHTS["age_match"]
            else:
                # Partial credit if close
                distance = min(abs(user_age - min_age), abs(user_age - max_age))
                if distance <= 5:
                    score += self.WEIGHTS["age_match"] * 0.5
        else:
            score += self.WEIGHTS["age_match"] * 0.3  # Unknown = partial credit

        # --- Income Match ---
        user_income = profile.get("annual_income")
        if user_income is not None:
            max_income = rules.get("max_income")
            if max_income is None:
                score += self.WEIGHTS["income_match"]
            elif user_income <= max_income:
                score += self.WEIGHTS["income_match"]
            else:
                # Gradual penalty
                over_ratio = user_income / max_income
                if over_ratio < 1.5:
                    score += self.WEIGHTS["income_match"] * 0.3
        else:
            score += self.WEIGHTS["income_match"] * 0.3

        # --- Gender Match ---
        user_gender = profile.get("gender")
        allowed_genders = rules.get("gender")
        if allowed_genders is None:
            score += self.WEIGHTS["gender_match"]
        elif user_gender and user_gender.lower() in [g.lower() for g in allowed_genders]:
            score += self.WEIGHTS["gender_match"]
        elif user_gender is None:
            score += self.WEIGHTS["gender_match"] * 0.3

        # --- Caste Category Match ---
        user_caste = profile.get("caste_category")
        allowed_castes = rules.get("caste_categories")
        if allowed_castes is None:
            score += self.WEIGHTS["caste_match"]
        elif user_caste and user_caste.lower() in [c.lower() for c in allowed_castes]:
            score += self.WEIGHTS["caste_match"]
        elif user_caste is None:
            score += self.WEIGHTS["caste_match"] * 0.3

        # --- Occupation Match ---
        user_occ = profile.get("occupation", "")
        allowed_occs = rules.get("occupation")
        if allowed_occs is None:
            score += self.WEIGHTS["occupation_match"]
        elif user_occ and user_occ.lower() in [o.lower() for o in allowed_occs]:
            score += self.WEIGHTS["occupation_match"]
        elif user_occ is None:
            score += self.WEIGHTS["occupation_match"] * 0.3

        # --- Rural Match ---
        is_rural = profile.get("is_rural")
        requires_rural = rules.get("is_rural")
        if requires_rural is None:
            score += self.WEIGHTS["rural_match"]
        elif is_rural == requires_rural:
            score += self.WEIGHTS["rural_match"]
        elif is_rural is None:
            score += self.WEIGHTS["rural_match"] * 0.3

        # --- BPL Match ---
        is_bpl = profile.get("is_bpl")
        requires_bpl = rules.get("is_bpl")
        if requires_bpl is None:
            score += self.WEIGHTS["bpl_match"]
        elif is_bpl == requires_bpl:
            score += self.WEIGHTS["bpl_match"]
        elif is_bpl is None:
            score += self.WEIGHTS["bpl_match"] * 0.3

        # --- Text Similarity ---
        if query_text:
            desc = scheme.get("description_en", "") + " " + scheme.get("name_en", "")
            keywords = scheme.get("search_keywords", []) or []
            desc += " " + " ".join(keywords)
            sim = self._tfidf_similarity(query_text, desc)
            score += self.WEIGHTS["text_similarity"] * sim

        # --- Popularity Boost ---
        pop = min(scheme.get("popularity_score", 0) / 100.0, 1.0)
        score += self.WEIGHTS["popularity"] * pop

        return score

    # =========================================================================
    # TF-IDF Text Similarity
    # =========================================================================

    def _tokenize(self, text: str) -> List[str]:
        """Simple whitespace + punctuation tokenizer."""
        return re.findall(r'\b\w+\b', text.lower())

    def _build_idf(self, documents: List[str]):
        """Build IDF scores from document collection."""
        self._total_docs = len(documents)
        doc_freq: Counter = Counter()
        for doc in documents:
            tokens = set(self._tokenize(doc))
            for token in tokens:
                doc_freq[token] += 1
        self._idf_cache = {
            token: math.log((self._total_docs + 1) / (freq + 1))
            for token, freq in doc_freq.items()
        }

    def _tfidf_vector(self, text: str) -> Dict[str, float]:
        """Compute TF-IDF vector for a document."""
        tokens = self._tokenize(text)
        tf = Counter(tokens)
        total = len(tokens) or 1
        return {
            token: (count / total) * self._idf_cache.get(token, 1.0)
            for token, count in tf.items()
        }

    def _tfidf_similarity(self, text1: str, text2: str) -> float:
        """Cosine similarity between two texts using TF-IDF."""
        vec1 = self._tfidf_vector(text1)
        vec2 = self._tfidf_vector(text2)

        if not vec1 or not vec2:
            return 0.0

        # Cosine similarity
        common = set(vec1.keys()) & set(vec2.keys())
        dot_product = sum(vec1[k] * vec2[k] for k in common)
        norm1 = math.sqrt(sum(v ** 2 for v in vec1.values()))
        norm2 = math.sqrt(sum(v ** 2 for v in vec2.values()))

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return dot_product / (norm1 * norm2)


# Singleton
scheme_recommender = SchemeRecommender()
