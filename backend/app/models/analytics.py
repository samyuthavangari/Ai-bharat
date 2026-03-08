"""
JanSahay AI - Analytics Event Model
Tracks scheme searches, eligibility checks, and language usage for admin dashboard.
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class AnalyticsEvent(Base):
    __tablename__ = "analytics_events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    event_type = Column(String(50), nullable=False, index=True)
    # Event types: scheme_search, scheme_view, eligibility_check,
    #              voice_query, language_switch, document_view,
    #              whatsapp_interaction, recommendation_click

    scheme_id = Column(Integer, ForeignKey("schemes.id"), nullable=True)
    language = Column(String(5), nullable=True)
    platform = Column(String(20), nullable=True)  # web, mobile, whatsapp
    query_text = Column(String(1000), nullable=True)
    intent_detected = Column(String(50), nullable=True)
    is_eligible = Column(String(10), nullable=True)  # yes, no, partial

    # Session tracking
    session_id = Column(String(100), nullable=True)

    # Response metrics
    response_time_ms = Column(Float, nullable=True)
    metadata = Column(JSON, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="analytics_events")
