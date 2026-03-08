"""
JanSahay AI - User Model
Stores citizen profiles with demographic data for scheme matching.
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum


class UserRole(str, enum.Enum):
    CITIZEN = "citizen"
    ADMIN = "admin"
    GOV_OFFICIAL = "gov_official"


class Gender(str, enum.Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class CasteCategory(str, enum.Enum):
    GENERAL = "general"
    OBC = "obc"
    SC = "sc"
    ST = "st"
    EWS = "ews"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    phone_number = Column(String(15), unique=True, index=True, nullable=True)
    email = Column(String(255), unique=True, index=True, nullable=True)
    full_name = Column(String(255), nullable=True)
    password_hash = Column(String(255), nullable=True)

    # Demographics for scheme matching
    age = Column(Integer, nullable=True)
    gender = Column(SQLEnum(Gender), nullable=True)
    state = Column(String(100), nullable=True)
    district = Column(String(100), nullable=True)
    caste_category = Column(SQLEnum(CasteCategory), nullable=True)
    annual_income = Column(Float, nullable=True)
    occupation = Column(String(100), nullable=True)
    is_rural = Column(Boolean, default=True)
    is_bpl = Column(Boolean, default=False)
    has_land = Column(Boolean, nullable=True)
    land_acres = Column(Float, nullable=True)
    is_farmer = Column(Boolean, default=False)
    is_student = Column(Boolean, default=False)
    is_differently_abled = Column(Boolean, default=False)
    is_widow = Column(Boolean, default=False)
    is_senior_citizen = Column(Boolean, default=False)
    num_children = Column(Integer, nullable=True)

    # Auth & preferences
    role = Column(SQLEnum(UserRole), default=UserRole.CITIZEN)
    preferred_language = Column(String(5), default="hi")
    is_active = Column(Boolean, default=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    analytics_events = relationship("AnalyticsEvent", back_populates="user")
