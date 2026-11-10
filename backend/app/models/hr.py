"""
Human Resources (HR), Payroll, Trainer Commissions & Leave Models
"""
import uuid
from datetime import datetime, timezone, date
from sqlalchemy import Column, String, DateTime, ForeignKey, Numeric, Text, Date
from app.core.database import Base


def utc_now():
    return datetime.now(timezone.utc)


class Employee(Base):
    __tablename__ = "employees"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    organization_id = Column(String(36), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    branch_id = Column(String(36), ForeignKey("branches.id", ondelete="SET NULL"), nullable=True, index=True)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    
    designation = Column(String(100), nullable=False)  # General Manager, Trainer, Front Desk, Cleaner, Accountant
    department = Column(String(100), default="Fitness")
    hire_date = Column(Date, default=date.today, nullable=False)
    base_salary = Column(Numeric(12, 2), default=0.00, nullable=False)
    commission_rate_percentage = Column(Numeric(5, 2), default=0.00, nullable=False)
    bank_account_number = Column(String(100), nullable=True)
    bank_ifsc = Column(String(50), nullable=True)
    
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False)


class Payroll(Base):
    __tablename__ = "payrolls"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    organization_id = Column(String(36), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    branch_id = Column(String(36), ForeignKey("branches.id", ondelete="SET NULL"), nullable=True, index=True)
    employee_id = Column(String(36), ForeignKey("employees.id", ondelete="CASCADE"), nullable=False, index=True)
    
    pay_period_month = Column(String(20), nullable=False)  # e.g., "2026-11"
    base_salary = Column(Numeric(12, 2), nullable=False)
    commission_amount = Column(Numeric(12, 2), default=0.00, nullable=False)
    bonus_amount = Column(Numeric(12, 2), default=0.00, nullable=False)
    deductions = Column(Numeric(12, 2), default=0.00, nullable=False)
    net_salary = Column(Numeric(12, 2), nullable=False)
    status = Column(String(50), default="DRAFT", index=True)  # DRAFT, APPROVED, PAID
    payment_reference = Column(String(100), nullable=True)
    paid_at = Column(DateTime(timezone=True), nullable=True)
    
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)


class LeaveRequest(Base):
    __tablename__ = "leave_requests"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    organization_id = Column(String(36), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    branch_id = Column(String(36), ForeignKey("branches.id", ondelete="SET NULL"), nullable=True, index=True)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    leave_type = Column(String(50), default="CASUAL")  # CASUAL, SICK, ANNUAL, EMERGENCY
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    reason = Column(Text, nullable=False)
    status = Column(String(50), default="PENDING", index=True)  # PENDING, APPROVED, REJECTED
    reviewed_by_id = Column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    review_notes = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False)
