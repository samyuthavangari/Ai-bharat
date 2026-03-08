"""
JanSahay AI - Eligibility API Routes
Check eligibility for specific schemes or bulk check across all schemes.
"""

from fastapi import APIRouter, Depends
from typing import Optional
from app.schemas import APIResponse, EligibilityRequest
from app.services.eligibility import eligibility_engine
from app.services.language_service import get_response
from app.seed.schemes_data import SCHEMES_SEED_DATA

router = APIRouter(prefix="/eligibility", tags=["Eligibility"])


@router.post("/check", response_model=APIResponse)
async def check_eligibility(data: EligibilityRequest, language: str = "en"):
    """
    Check eligibility for a specific scheme.
    Returns detailed pass/fail reasons per criterion.
    """
    # Find scheme
    scheme = None
    for s in SCHEMES_SEED_DATA:
        if data.scheme_code and s["scheme_code"] == data.scheme_code:
            scheme = s
            break
        elif data.scheme_id and SCHEMES_SEED_DATA.index(s) + 1 == data.scheme_id:
            scheme = s
            break

    if not scheme:
        return APIResponse(success=False, message="Scheme not found")

    profile = {
        "age": data.age,
        "gender": data.gender,
        "state": data.state,
        "caste_category": data.caste_category,
        "annual_income": data.annual_income,
        "occupation": data.occupation,
        "is_rural": data.is_rural,
        "is_bpl": data.is_bpl,
        "is_farmer": data.is_farmer,
        "has_land": data.has_land,
        "land_acres": data.land_acres,
    }

    result = eligibility_engine.check_eligibility(profile, scheme)

    msg_key = "eligible" if result["is_eligible"] else "not_eligible"
    return APIResponse(
        success=True,
        message=get_response(msg_key, language),
        data=result,
    )


@router.post("/bulk-check", response_model=APIResponse)
async def bulk_check_eligibility(data: EligibilityRequest, language: str = "en"):
    """
    Check eligibility across ALL schemes.
    Returns categorized results: eligible, partially eligible.
    """
    profile = {
        "age": data.age,
        "gender": data.gender,
        "state": data.state,
        "caste_category": data.caste_category,
        "annual_income": data.annual_income,
        "occupation": data.occupation,
        "is_rural": data.is_rural,
        "is_bpl": data.is_bpl,
        "is_farmer": data.is_farmer,
        "has_land": data.has_land,
        "land_acres": data.land_acres,
    }

    results = eligibility_engine.bulk_check(profile, SCHEMES_SEED_DATA)

    return APIResponse(
        success=True,
        message=f"Checked {results['total_checked']} schemes. "
                f"Eligible: {len(results['eligible_schemes'])}, "
                f"Partially eligible: {len(results['partially_eligible'])}",
        data=results,
    )
