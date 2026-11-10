"""
CRM Models: Leads, Feedback & Complaints
"""
import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, ForeignKey, Text
from app.core.database import Base


def utc_now():
    return datetime.now(timezone.utc)


class Lead(Base):
    __tablename__ = "leads"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    organization_id = Column(String(36), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    branch_id = Column(String(36), ForeignKey("branches.id", ondelete="SET NULL"), nullable=True, index=True)
    
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=False, index=True)
    source = Column(String(100), default="Walk-in")  # Walk-in, Website, Referral, Social Media
    status = Column(String(50), default="NEW", index=True)  # NEW, CONTACTED, INTERESTED, TRIAL, CONVERTED, LOST
    notes = Column(Text, nullable=True)
    trial_date = Column(DateTime(timezone=True), nullable=True)
    assigned_to_user_id = Column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False)


class CustomerFeedback(Base):
    __tablename__ = "customer_feedbacks"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    organization_id = Column(String(36), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    branch_id = Column(String(36), ForeignKey("branches.id", ondelete="SET NULL"), nullable=True, index=True)
    client_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    category = Column(String(100), default="General")  # Cleanliness, Equipment, Trainer, Facility, Staff
    rating = Column(String(10), nullable=True)  # 1 to 5
    message = Column(Text, nullable=False)
    status = Column(String(50), default="OPEN")  # OPEN, IN_REVIEW, RESOLVED
    resolution_notes = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False)
