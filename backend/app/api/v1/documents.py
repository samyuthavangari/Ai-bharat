"""
JanSahay AI - Documents API Routes
Document requirement lookup and guidance.
"""

from fastapi import APIRouter
from typing import Optional
from app.schemas import APIResponse
from app.services.document_guidance import document_guidance
from app.seed.schemes_data import SCHEMES_SEED_DATA

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.get("/scheme/{scheme_code}", response_model=APIResponse)
async def get_scheme_documents(scheme_code: str, language: str = "en"):
    """Get required documents for a specific scheme with localized descriptions."""
    scheme = None
    for s in SCHEMES_SEED_DATA:
        if s["scheme_code"] == scheme_code:
            scheme = s
            break

    if not scheme:
        return APIResponse(success=False, message="Scheme not found")

    docs = document_guidance.get_scheme_documents(scheme, language)
    return APIResponse(
        success=True,
        message=f"Found {len(docs)} required documents",
        data={
            "scheme_code": scheme_code,
            "scheme_name": scheme.get(f"name_{language}") or scheme["name_en"],
            "documents": docs,
        },
    )


@router.get("/info/{document_id}", response_model=APIResponse)
async def get_document_info(document_id: str, language: str = "en"):
    """Get detailed info about a specific document type (e.g., aadhaar, ration_card)."""
    info = document_guidance.get_document_info(document_id, language)
    if not info:
        return APIResponse(success=False, message="Document not found")
    return APIResponse(success=True, message="Document info", data=info)


@router.get("/search", response_model=APIResponse)
async def search_documents(query: str, language: str = "en"):
    """Search document library by name."""
    results = document_guidance.search_documents(query, language)
    return APIResponse(
        success=True,
        message=f"Found {len(results)} documents",
        data=results,
    )
