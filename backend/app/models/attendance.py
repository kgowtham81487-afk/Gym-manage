"""
Attendance Tracking Models with Duplicate Prevention
"""
import uuid
from datetime import datetime, timezone, date
from sqlalchemy import Column, String, DateTime, ForeignKey, Date, UniqueConstraint
from app.core.database import Base


def utc_now():
    return datetime.now(timezone.utc)


class Attendance(Base):
    __tablename__ = "attendance"
    __table_args__ = (
        UniqueConstraint("user_id", "attendance_date", "session_type", name="uq_user_attendance_date_session"),
    )

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    organization_id = Column(String(36), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    branch_id = Column(String(36), ForeignKey("branches.id", ondelete="SET NULL"), nullable=True, index=True)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    attendance_date = Column(Date, default=date.today, nullable=False, index=True)
    check_in_time = Column(DateTime(timezone=True), default=utc_now, nullable=False)
    check_out_time = Column(DateTime(timezone=True), nullable=True)
    
    method = Column(String(50), default="MANUAL")  # QR, MANUAL, BIOMETRIC, RFID
    user_role = Column(String(50), default="CLIENT")  # CLIENT, TRAINER, EMPLOYEE
    session_type = Column(String(50), default="GENERAL")  # GENERAL, PT, SHIFT
    
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)
