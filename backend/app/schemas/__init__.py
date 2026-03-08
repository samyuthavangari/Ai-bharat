"""
JanSahay AI - Pydantic Schemas
Request/response models for all API endpoints.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Any
from datetime import datetime
from enum import Enum


# --- Enums ---
class LanguageCode(str, Enum):
    EN = "en"
    HI = "hi"
    BN = "bn"
    TA = "ta"
    TE = "te"
    MR = "mr"


class IntentType(str, Enum):
    SCHEME_DISCOVERY = "scheme_discovery"
    ELIGIBILITY_CHECK = "eligibility_check"
    DOCUMENT_REQUIREMENT = "document_requirement"
    APPLICATION_GUIDANCE = "application_guidance"
    GENERAL_QUERY = "general_query"
    GREETING = "greeting"


class Platform(str, Enum):
    WEB = "web"
    MOBILE = "mobile"
    WHATSAPP = "whatsapp"


# --- Auth Schemas ---
class UserRegister(BaseModel):
    phone_number: Optional[str] = None
    email: Optional[str] = None
    password: str = Field(min_length=6)
    full_name: Optional[str] = None
    preferred_language: str = "hi"


class UserLogin(BaseModel):
    username: str  # phone or email
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class UserProfile(BaseModel):
    id: int
    phone_number: Optional[str] = None
    email: Optional[str] = None
    full_name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    state: Optional[str] = None
    district: Optional[str] = None
    caste_category: Optional[str] = None
    annual_income: Optional[float] = None
    occupation: Optional[str] = None
    is_rural: bool = True
    is_bpl: bool = False
    is_farmer: bool = False
    preferred_language: str = "hi"
    role: str = "citizen"

    class Config:
        from_attributes = True


class UserProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    state: Optional[str] = None
    district: Optional[str] = None
    caste_category: Optional[str] = None
    annual_income: Optional[float] = None
    occupation: Optional[str] = None
    is_rural: Optional[bool] = None
    is_bpl: Optional[bool] = None
    is_farmer: Optional[bool] = None
    has_land: Optional[bool] = None
    land_acres: Optional[float] = None
    is_student: Optional[bool] = None
    is_differently_abled: Optional[bool] = None
    is_widow: Optional[bool] = None
    is_senior_citizen: Optional[bool] = None
    num_children: Optional[int] = None
    preferred_language: Optional[str] = None


# --- Chat / NLP Schemas ---
class ChatMessage(BaseModel):
    text: str
    language: Optional[str] = None
    session_id: Optional[str] = None
    platform: Platform = Platform.WEB


class NLPResult(BaseModel):
    intent: IntentType
    confidence: float
    entities: dict = {}
    language_detected: str = "en"


class ChatResponse(BaseModel):
    reply_text: str
    intent: IntentType
    entities: dict = {}
    schemes: Optional[List[dict]] = None
    documents: Optional[List[dict]] = None
    eligibility: Optional[dict] = None
    language: str = "en"
    session_id: str


# --- Voice Schemas ---
class VoiceInput(BaseModel):
    audio_base64: str
    language: Optional[str] = None
    format: str = "wav"
    session_id: Optional[str] = None


class VoiceResponse(BaseModel):
    transcribed_text: str
    reply_text: str
    reply_audio_base64: Optional[str] = None
    language: str
    intent: IntentType
    session_id: str


# --- Scheme Schemas ---
class SchemeListItem(BaseModel):
    id: int
    scheme_code: str
    name: str
    description: str
    ministry: Optional[str] = None
    benefit_type: Optional[str] = None
    benefit_amount: Optional[str] = None
    popularity_score: float = 0.0

    class Config:
        from_attributes = True


class SchemeDetail(BaseModel):
    id: int
    scheme_code: str
    name: str
    description: str
    ministry: Optional[str] = None
    department: Optional[str] = None
    scheme_type: Optional[str] = None
    benefit_type: Optional[str] = None
    benefit_amount: Optional[str] = None
    application_url: Optional[str] = None
    helpline_number: Optional[str] = None
    required_documents: Optional[List[dict]] = None
    application_steps: Optional[List[dict]] = None
    eligibility_rules: Optional[dict] = None

    class Config:
        from_attributes = True


class SchemeSearchQuery(BaseModel):
    query: Optional[str] = None
    state: Optional[str] = None
    category: Optional[str] = None
    benefit_type: Optional[str] = None
    language: str = "en"
    page: int = 1
    page_size: int = 20


# --- Eligibility Schemas ---
class EligibilityRequest(BaseModel):
    scheme_id: Optional[int] = None
    scheme_code: Optional[str] = None
    # User profile fields (override stored profile)
    age: Optional[int] = None
    gender: Optional[str] = None
    state: Optional[str] = None
    caste_category: Optional[str] = None
    annual_income: Optional[float] = None
    occupation: Optional[str] = None
    is_rural: Optional[bool] = None
    is_bpl: Optional[bool] = None
    is_farmer: Optional[bool] = None
    has_land: Optional[bool] = None
    land_acres: Optional[float] = None


class EligibilityResult(BaseModel):
    scheme_id: int
    scheme_name: str
    is_eligible: bool
    match_score: float  # 0.0 to 1.0
    reasons: List[str] = []
    missing_criteria: List[str] = []


class BulkEligibilityResponse(BaseModel):
    eligible_schemes: List[EligibilityResult]
    partially_eligible: List[EligibilityResult]
    total_checked: int


# --- Document Schemas ---
class DocumentInfo(BaseModel):
    name: str
    description: str
    how_to_obtain: str
    is_mandatory: bool = True


class DocumentGuidanceResponse(BaseModel):
    scheme_name: str
    documents: List[DocumentInfo]
    language: str = "en"


# --- Analytics Schemas ---
class AnalyticsSummary(BaseModel):
    total_searches: int
    total_eligibility_checks: int
    total_voice_queries: int
    most_searched_schemes: List[dict]
    language_distribution: dict
    platform_distribution: dict
    eligibility_success_rate: float
    daily_active_users: int


class AnalyticsTimeRange(BaseModel):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    granularity: str = "day"  # day, week, month


# --- WhatsApp Schemas ---
class WhatsAppIncoming(BaseModel):
    From: str = Field(alias="from_number")
    Body: str
    MessageSid: Optional[str] = None


class WhatsAppOutgoing(BaseModel):
    to: str
    message: str


# --- Generic ---
class HealthResponse(BaseModel):
    status: str
    version: str
    services: dict


class APIResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None
