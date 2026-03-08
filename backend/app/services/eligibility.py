"""
JanSahay AI - Eligibility Engine
Rule-based + AI hybrid logic for checking scheme eligibility.
Returns detailed results with pass/fail reasons per criterion.
"""

from typing import Dict, List, Optional, Tuple


class EligibilityEngine:
    """
    Hybrid eligibility checker:
    1. Rule-based: exact matching against scheme eligibility criteria
    2. AI scoring: fuzzy matching for partial eligibility (e.g., borderline income)
    """

    def check_eligibility(
        self, user_profile: dict, scheme: dict
    ) -> dict:
        """
        Check if a user is eligible for a specific scheme.

        Returns:
            {
                "scheme_id": int,
                "scheme_name": str,
                "is_eligible": bool,
                "match_score": float,
                "reasons": ["Passed: Age requirement"],
                "missing_criteria": ["Failed: Income too high"]
            }
        """
        rules = scheme.get("eligibility_rules") or {}
        reasons: List[str] = []
        missing: List[str] = []
        criteria_count = 0
        passed_count = 0

        # --- Age Check ---
        if "min_age" in rules or "max_age" in rules:
            criteria_count += 1
            user_age = user_profile.get("age")
            min_age = rules.get("min_age", 0)
            max_age = rules.get("max_age", 150)

            if user_age is None:
                missing.append(f"Age information not provided (required: {min_age}-{max_age} years)")
            elif min_age <= user_age <= max_age:
                passed_count += 1
                reasons.append(f"✅ Age {user_age} is within {min_age}-{max_age} years")
            else:
                missing.append(f"❌ Age {user_age} not in range {min_age}-{max_age} years")

        # --- Income Check ---
        if "max_income" in rules:
            criteria_count += 1
            user_income = user_profile.get("annual_income")
            max_income = rules["max_income"]

            if user_income is None:
                missing.append(f"Income not provided (max allowed: ₹{max_income:,.0f})")
            elif user_income <= max_income:
                passed_count += 1
                reasons.append(f"✅ Income ₹{user_income:,.0f} ≤ ₹{max_income:,.0f}")
            else:
                missing.append(f"❌ Income ₹{user_income:,.0f} exceeds limit ₹{max_income:,.0f}")

        # --- Gender Check ---
        if "gender" in rules:
            criteria_count += 1
            user_gender = user_profile.get("gender")
            allowed = rules["gender"]

            if user_gender is None:
                missing.append(f"Gender not provided (eligible: {', '.join(allowed)})")
            elif user_gender.lower() in [g.lower() for g in allowed]:
                passed_count += 1
                reasons.append(f"✅ Gender '{user_gender}' matches requirement")
            else:
                missing.append(f"❌ Gender '{user_gender}' not eligible (need: {', '.join(allowed)})")

        # --- Caste Category Check ---
        if "caste_categories" in rules:
            criteria_count += 1
            user_caste = user_profile.get("caste_category")
            allowed = rules["caste_categories"]

            if user_caste is None:
                missing.append(f"Caste category not provided (eligible: {', '.join(allowed).upper()})")
            elif user_caste.lower() in [c.lower() for c in allowed]:
                passed_count += 1
                reasons.append(f"✅ Category '{user_caste.upper()}' is eligible")
            else:
                missing.append(f"❌ Category '{user_caste.upper()}' not eligible (need: {', '.join(allowed).upper()})")

        # --- State Check ---
        if "states" in rules:
            criteria_count += 1
            user_state = user_profile.get("state")
            allowed = rules["states"]

            if user_state is None:
                missing.append(f"State not provided (eligible: {', '.join(allowed)})")
            elif user_state.lower() in [s.lower() for s in allowed]:
                passed_count += 1
                reasons.append(f"✅ State '{user_state}' is eligible")
            else:
                missing.append(f"❌ State '{user_state}' not eligible for this scheme")

        # --- Occupation Check ---
        if "occupation" in rules:
            criteria_count += 1
            user_occ = user_profile.get("occupation", "")
            allowed = rules["occupation"]

            if not user_occ:
                missing.append(f"Occupation not provided (eligible: {', '.join(allowed)})")
            elif user_occ.lower() in [o.lower() for o in allowed]:
                passed_count += 1
                reasons.append(f"✅ Occupation '{user_occ}' matches")
            else:
                missing.append(f"❌ Occupation '{user_occ}' not eligible (need: {', '.join(allowed)})")

        # --- BPL Check ---
        if "is_bpl" in rules:
            criteria_count += 1
            user_bpl = user_profile.get("is_bpl")

            if user_bpl is None:
                missing.append("BPL status not provided")
            elif user_bpl == rules["is_bpl"]:
                passed_count += 1
                status = "BPL" if rules["is_bpl"] else "Non-BPL"
                reasons.append(f"✅ {status} status matches")
            else:
                status = "BPL" if rules["is_bpl"] else "Non-BPL"
                missing.append(f"❌ Must be {status}")

        # --- Rural Check ---
        if "is_rural" in rules:
            criteria_count += 1
            user_rural = user_profile.get("is_rural")

            if user_rural is None:
                missing.append("Rural/Urban status not provided")
            elif user_rural == rules["is_rural"]:
                passed_count += 1
                area = "rural" if rules["is_rural"] else "urban"
                reasons.append(f"✅ {area.title()} area matches")
            else:
                area = "rural" if rules["is_rural"] else "urban"
                missing.append(f"❌ Must be from {area} area")

        # --- Custom Rules ---
        custom_rules = rules.get("custom_rules", [])
        for cr in custom_rules:
            criteria_count += 1
            field = cr.get("field")
            operator = cr.get("operator")
            expected = cr.get("value")
            user_val = user_profile.get(field)

            if user_val is None:
                missing.append(f"{field.replace('_', ' ').title()} not provided")
                continue

            passed = False
            if operator == "eq":
                passed = user_val == expected
            elif operator == "neq":
                passed = user_val != expected
            elif operator == "gt":
                passed = user_val > expected
            elif operator == "gte":
                passed = user_val >= expected
            elif operator == "lt":
                passed = user_val < expected
            elif operator == "lte":
                passed = user_val <= expected

            if passed:
                passed_count += 1
                reasons.append(f"✅ {field.replace('_', ' ').title()}: {user_val} meets requirement")
            else:
                missing.append(f"❌ {field.replace('_', ' ').title()}: {user_val} does not meet requirement ({operator} {expected})")

        # --- Calculate Score ---
        if criteria_count == 0:
            match_score = 0.8  # No rules = likely eligible (general scheme)
            is_eligible = True
            reasons.append("✅ No specific eligibility criteria - likely open to all")
        else:
            match_score = passed_count / criteria_count
            is_eligible = len(missing) == 0

        return {
            "scheme_id": scheme.get("id", 0),
            "scheme_name": scheme.get("name_en", "Unknown Scheme"),
            "is_eligible": is_eligible,
            "match_score": round(match_score, 2),
            "reasons": reasons,
            "missing_criteria": missing,
        }

    def bulk_check(
        self, user_profile: dict, schemes: List[dict]
    ) -> dict:
        """
        Check eligibility across multiple schemes.

        Returns:
            {
                "eligible_schemes": [...],
                "partially_eligible": [...],
                "total_checked": int
            }
        """
        eligible = []
        partial = []

        for scheme in schemes:
            if not scheme.get("is_active", True):
                continue
            result = self.check_eligibility(user_profile, scheme)
            if result["is_eligible"]:
                eligible.append(result)
            elif result["match_score"] >= 0.5:
                partial.append(result)

        # Sort by score
        eligible.sort(key=lambda x: x["match_score"], reverse=True)
        partial.sort(key=lambda x: x["match_score"], reverse=True)

        return {
            "eligible_schemes": eligible,
            "partially_eligible": partial,
            "total_checked": len(schemes),
        }


# Singleton
eligibility_engine = EligibilityEngine()
