"""
JanSahay AI - Analytics API Routes
Dashboard endpoints for government admins to track usage and impact.
"""

from fastapi import APIRouter, Depends
from app.schemas import APIResponse
from app.auth.rbac import require_gov_official
from app.models.user import User

router = APIRouter(prefix="/analytics", tags=["Analytics"])

# Mock analytics data (in production, query from AnalyticsEvent table)
MOCK_ANALYTICS = {
    "summary": {
        "total_users": 125430,
        "total_searches": 892340,
        "total_eligibility_checks": 456210,
        "total_voice_queries": 234560,
        "daily_active_users": 8230,
        "eligibility_success_rate": 0.67,
    },
    "most_searched_schemes": [
        {"scheme_code": "PM-KISAN", "name": "PM Kisan Samman Nidhi", "searches": 156000},
        {"scheme_code": "PM-JAY", "name": "Ayushman Bharat PM-JAY", "searches": 132000},
        {"scheme_code": "FREE-RATION", "name": "PM Garib Kalyan Anna Yojana", "searches": 128000},
        {"scheme_code": "PM-AWAS-GRAMIN", "name": "PM Awas Yojana Gramin", "searches": 98000},
        {"scheme_code": "MGNREGA", "name": "MGNREGA", "searches": 89000},
        {"scheme_code": "JAN-DHAN", "name": "PM Jan Dhan Yojana", "searches": 76000},
        {"scheme_code": "PM-UJJWALA", "name": "PM Ujjwala Yojana", "searches": 67000},
        {"scheme_code": "MUDRA", "name": "PM MUDRA Yojana", "searches": 54000},
        {"scheme_code": "KISAN-CREDIT", "name": "Kisan Credit Card", "searches": 45000},
        {"scheme_code": "LADLI-BEHNA", "name": "Ladli Behna Yojana", "searches": 43000},
    ],
    "language_distribution": {
        "hi": 42.5,
        "en": 23.1,
        "bn": 12.3,
        "ta": 8.4,
        "te": 7.2,
        "mr": 6.5,
    },
    "platform_distribution": {
        "web": 38.2,
        "mobile": 35.6,
        "whatsapp": 26.2,
    },
    "state_distribution": {
        "Uttar Pradesh": 18.5,
        "Bihar": 12.1,
        "Maharashtra": 10.4,
        "Madhya Pradesh": 9.2,
        "Rajasthan": 8.8,
        "West Bengal": 7.6,
        "Tamil Nadu": 6.5,
        "Karnataka": 5.4,
        "Odisha": 4.8,
        "Others": 16.7,
    },
    "daily_trends": [
        {"date": "2026-02-23", "searches": 12340, "eligibility_checks": 5430},
        {"date": "2026-02-24", "searches": 13200, "eligibility_checks": 5890},
        {"date": "2026-02-25", "searches": 11890, "eligibility_checks": 5120},
        {"date": "2026-02-26", "searches": 14560, "eligibility_checks": 6340},
        {"date": "2026-02-27", "searches": 15230, "eligibility_checks": 6780},
        {"date": "2026-02-28", "searches": 13450, "eligibility_checks": 6120},
        {"date": "2026-03-01", "searches": 16780, "eligibility_checks": 7230},
    ],
}


@router.get("/summary", response_model=APIResponse)
async def get_analytics_summary():
    """
    Get analytics summary dashboard data.
    Tracks most searched schemes, language usage, eligibility success rate.
    """
    return APIResponse(
        success=True,
        message="Analytics summary",
        data=MOCK_ANALYTICS["summary"],
    )


@router.get("/schemes/popular", response_model=APIResponse)
async def get_popular_schemes():
    """Get most searched/popular schemes."""
    return APIResponse(
        success=True,
        message="Popular schemes",
        data=MOCK_ANALYTICS["most_searched_schemes"],
    )


@router.get("/languages", response_model=APIResponse)
async def get_language_stats():
    """Get language usage distribution."""
    return APIResponse(
        success=True,
        message="Language distribution",
        data=MOCK_ANALYTICS["language_distribution"],
    )


@router.get("/platforms", response_model=APIResponse)
async def get_platform_stats():
    """Get platform usage distribution (web, mobile, whatsapp)."""
    return APIResponse(
        success=True,
        message="Platform distribution",
        data=MOCK_ANALYTICS["platform_distribution"],
    )


@router.get("/states", response_model=APIResponse)
async def get_state_stats():
    """Get state-wise usage distribution."""
    return APIResponse(
        success=True,
        message="State distribution",
        data=MOCK_ANALYTICS["state_distribution"],
    )


@router.get("/trends", response_model=APIResponse)
async def get_daily_trends():
    """Get daily usage trends for the last 7 days."""
    return APIResponse(
        success=True,
        message="Daily trends",
        data=MOCK_ANALYTICS["daily_trends"],
    )


@router.get("/dashboard", response_model=APIResponse)
async def get_full_dashboard():
    """Get complete dashboard data in one call (for admin panel)."""
    return APIResponse(
        success=True,
        message="Full dashboard data",
        data=MOCK_ANALYTICS,
    )
