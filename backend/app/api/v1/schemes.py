"""
JanSahay AI - Schemes API Routes
Search, list, and view government schemes.
"""

from fastapi import APIRouter, Depends, Query
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas import APIResponse, SchemeSearchQuery
from app.services.recommendation import scheme_recommender
from app.services.language_service import get_response
from app.redis_client import cache_get, cache_set
from app.seed.schemes_data import SCHEMES_SEED_DATA

router = APIRouter(prefix="/schemes", tags=["Schemes"])


@router.get("/", response_model=APIResponse)
async def list_schemes(
    query: Optional[str] = None,
    state: Optional[str] = None,
    category: Optional[str] = None,
    benefit_type: Optional[str] = None,
    language: str = "en",
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):
    """
    Search and list government schemes.
    Supports filtering by state, category, benefit type, and free text search.
    Results are cached for low-bandwidth optimization.
    """
    cache_key = f"schemes:{query}:{state}:{category}:{benefit_type}:{page}:{page_size}"
    cached = await cache_get(cache_key)
    if cached:
        return APIResponse(success=True, message="Schemes retrieved (cached)", data=cached)

    schemes = SCHEMES_SEED_DATA.copy()

    # Filter by state
    if state:
        schemes = [
            s for s in schemes
            if s.get("target_state") is None
            or state.lower() in (s.get("target_state", "").lower())
        ]

    # Filter by benefit type
    if benefit_type:
        schemes = [s for s in schemes if s.get("benefit_type") == benefit_type]

    # Search by query text
    if query:
        query_lower = query.lower()
        scored = []
        for s in schemes:
            score = 0
            searchable = (
                s.get("name_en", "").lower() + " " +
                s.get("description_en", "").lower() + " " +
                " ".join(s.get("search_keywords", []))
            )
            if query_lower in searchable:
                score += 10
            for word in query_lower.split():
                if word in searchable:
                    score += 1
            if score > 0:
                scored.append((score, s))
        scored.sort(key=lambda x: x[0], reverse=True)
        schemes = [s for _, s in scored]

    # Localize names
    lang_key = f"name_{language}"
    desc_key = f"description_{language}"
    results = []
    for s in schemes:
        results.append({
            "id": SCHEMES_SEED_DATA.index(s) + 1,
            "scheme_code": s["scheme_code"],
            "name": s.get(lang_key) or s["name_en"],
            "description": (s.get(desc_key) or s["description_en"])[:200] + "...",
            "ministry": s.get("ministry"),
            "benefit_type": s.get("benefit_type"),
            "benefit_amount": s.get("benefit_amount"),
            "popularity_score": s.get("popularity_score", 0),
        })

    # Pagination
    total = len(results)
    start = (page - 1) * page_size
    end = start + page_size
    paginated = results[start:end]

    response_data = {
        "schemes": paginated,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size,
    }

    await cache_set(cache_key, response_data, ttl=1800)
    return APIResponse(success=True, message=f"Found {total} schemes", data=response_data)


@router.get("/{scheme_code}", response_model=APIResponse)
async def get_scheme_detail(scheme_code: str, language: str = "en"):
    """Get detailed information about a specific scheme."""
    cache_key = f"scheme_detail:{scheme_code}:{language}"
    cached = await cache_get(cache_key)
    if cached:
        return APIResponse(success=True, message="Scheme details (cached)", data=cached)

    scheme = None
    for s in SCHEMES_SEED_DATA:
        if s["scheme_code"] == scheme_code:
            scheme = s
            break

    if not scheme:
        return APIResponse(success=False, message="Scheme not found", data=None)

    lang_key = f"name_{language}"
    desc_key = f"description_{language}"

    detail = {
        "scheme_code": scheme["scheme_code"],
        "name": scheme.get(lang_key) or scheme["name_en"],
        "description": scheme.get(desc_key) or scheme["description_en"],
        "ministry": scheme.get("ministry"),
        "department": scheme.get("department"),
        "scheme_type": scheme.get("scheme_type"),
        "target_state": scheme.get("target_state"),
        "benefit_type": scheme.get("benefit_type"),
        "benefit_amount": scheme.get("benefit_amount"),
        "application_url": scheme.get("application_url"),
        "helpline_number": scheme.get("helpline_number"),
        "eligibility_rules": scheme.get("eligibility_rules"),
        "required_documents": scheme.get("required_documents"),
        "application_steps": scheme.get("application_steps"),
    }

    await cache_set(cache_key, detail, ttl=3600)
    return APIResponse(success=True, message="Scheme details retrieved", data=detail)


@router.get("/recommend/for-me", response_model=APIResponse)
async def recommend_schemes(
    age: Optional[int] = None,
    gender: Optional[str] = None,
    state: Optional[str] = None,
    income: Optional[float] = None,
    occupation: Optional[str] = None,
    caste_category: Optional[str] = None,
    is_rural: Optional[bool] = None,
    is_bpl: Optional[bool] = None,
    language: str = "en",
):
    """
    AI-powered scheme recommendations based on user profile.
    Uses ML scoring model to rank schemes by relevance.
    """
    profile = {
        "age": age,
        "gender": gender,
        "state": state,
        "annual_income": income,
        "occupation": occupation,
        "caste_category": caste_category,
        "is_rural": is_rural,
        "is_bpl": is_bpl,
    }

    recommendations = scheme_recommender.recommend(
        user_profile=profile,
        schemes=SCHEMES_SEED_DATA,
        top_k=10,
    )

    lang_key = f"name_{language}"
    results = []
    for r in recommendations:
        results.append({
            "scheme_code": r["scheme_code"],
            "name": r.get(lang_key) or r["name_en"],
            "description": (r.get(f"description_{language}") or r["description_en"])[:150] + "...",
            "benefit_amount": r.get("benefit_amount"),
            "match_score": r["match_score"],
        })

    return APIResponse(
        success=True,
        message=get_response("scheme_found", language, count=len(results)),
        data=results,
    )
