"""
JanSahay AI - Scheme Model
Government scheme database with eligibility rules, documents, and multilingual metadata.
"""

from sqlalchemy import Column, Integer, String, Float, Text, Boolean, DateTime, JSON
from sqlalchemy.sql import func
from app.database import Base


class Scheme(Base):
    __tablename__ = "schemes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    scheme_code = Column(String(50), unique=True, index=True, nullable=False)
    name_en = Column(String(500), nullable=False)
    name_hi = Column(String(500), nullable=True)
    name_bn = Column(String(500), nullable=True)
    name_ta = Column(String(500), nullable=True)
    name_te = Column(String(500), nullable=True)
    name_mr = Column(String(500), nullable=True)

    description_en = Column(Text, nullable=False)
    description_hi = Column(Text, nullable=True)
    description_bn = Column(Text, nullable=True)
    description_ta = Column(Text, nullable=True)
    description_te = Column(Text, nullable=True)
    description_mr = Column(Text, nullable=True)

    # Scheme details
    ministry = Column(String(255), nullable=True)
    department = Column(String(255), nullable=True)
    scheme_type = Column(String(50), nullable=True)  # central, state, both
    target_state = Column(String(100), nullable=True)  # null = all India
    benefit_type = Column(String(100), nullable=True)  # cash, subsidy, service, insurance
    benefit_amount = Column(String(255), nullable=True)
    application_url = Column(String(500), nullable=True)
    helpline_number = Column(String(50), nullable=True)

    # Eligibility criteria (JSON rules)
    eligibility_rules = Column(JSON, nullable=True)
    """
    Format:
    {
        "min_age": 18, "max_age": 59,
        "gender": ["female"],
        "max_income": 200000,
        "caste_categories": ["sc", "st", "obc"],
        "states": ["UP", "MP"],
        "occupation": ["farmer"],
        "is_bpl": true,
        "is_rural": true,
        "custom_rules": [
            {"field": "has_land", "operator": "eq", "value": true},
            {"field": "land_acres", "operator": "lte", "value": 5}
        ]
    }
    """

    # Required documents (JSON list)
    required_documents = Column(JSON, nullable=True)
    """
    Format:
    [
        {
            "name_en": "Aadhaar Card",
            "name_hi": "आधार कार्ड",
            "description_en": "12-digit unique ID issued by UIDAI",
            "how_to_obtain_en": "Visit nearest Aadhaar Seva Kendra or apply at uidai.gov.in",
            "is_mandatory": true
        }
    ]
    """

    # Application steps (JSON list)
    application_steps = Column(JSON, nullable=True)

    # Keywords for search (JSON list)
    search_keywords = Column(JSON, nullable=True)

    # Status
    is_active = Column(Boolean, default=True)
    launch_date = Column(DateTime(timezone=True), nullable=True)

    # Metadata
    popularity_score = Column(Float, default=0.0)
    total_searches = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
