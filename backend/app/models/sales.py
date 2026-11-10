"""
POS, Sales, Razorpay Payments, Invoices & Refunds Models
"""
import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, ForeignKey, Integer, Numeric, Text
from sqlalchemy.orm import relationship
from app.core.database import Base


def utc_now():
    return datetime.now(timezone.utc)


class Sale(Base):
    __tablename__ = "sales"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    organization_id = Column(String(36), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    branch_id = Column(String(36), ForeignKey("branches.id", ondelete="SET NULL"), nullable=True, index=True)
    client_id = Column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    cashier_id = Column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    
    invoice_number = Column(String(100), unique=True, nullable=False, index=True)
    sale_type = Column(String(50), default="SUPPLEMENT")  # MEMBERSHIP, PT, SUPPLEMENT, COMBINED
    subtotal = Column(Numeric(12, 2), nullable=False)
    discount = Column(Numeric(12, 2), default=0.00, nullable=False)
    tax_amount = Column(Numeric(12, 2), default=0.00, nullable=False)
    total_amount = Column(Numeric(12, 2), nullable=False)
    payment_status = Column(String(50), default="UNPAID", index=True)  # UNPAID, PAID, PARTIAL, REFUNDED
    
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False, index=True)

    items = relationship("SaleItem", back_populates="sale", cascade="all, delete-orphan")
    payments = relationship("Payment", back_populates="sale")


class SaleItem(Base):
    __tablename__ = "sale_items"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    sale_id = Column(String(36), ForeignKey("sales.id", ondelete="CASCADE"), nullable=False, index=True)
    
    item_type = Column(String(50), nullable=False)  # PRODUCT, MEMBERSHIP, PT_PACKAGE
    item_id = Column(String(36), nullable=False)
    item_name = Column(String(255), nullable=False)
    quantity = Column(Integer, default=1, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)
    total_price = Column(Numeric(12, 2), nullable=False)

    sale = relationship("Sale", back_populates="items")


class Payment(Base):
    __tablename__ = "payments"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    organization_id = Column(String(36), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    branch_id = Column(String(36), ForeignKey("branches.id", ondelete="SET NULL"), nullable=True, index=True)
    sale_id = Column(String(36), ForeignKey("sales.id", ondelete="SET NULL"), nullable=True, index=True)
    client_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    payment_method = Column(String(50), default="RAZORPAY")  # RAZORPAY, CASH, UPI, CARD
    amount = Column(Numeric(12, 2), nullable=False)
    status = Column(String(50), default="PENDING", index=True)  # PENDING, SUCCESS, FAILED, REFUNDED
    
    # Razorpay Specific Transaction Fields
    razorpay_order_id = Column(String(100), unique=True, nullable=True, index=True)
    razorpay_payment_id = Column(String(100), unique=True, nullable=True, index=True)
    razorpay_signature = Column(String(255), nullable=True)
    
    failure_reason = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False, index=True)

    sale = relationship("Sale", back_populates="payments")
    refunds = relationship("Refund", back_populates="payment")


class Refund(Base):
    __tablename__ = "refunds"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    organization_id = Column(String(36), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    branch_id = Column(String(36), ForeignKey("branches.id", ondelete="SET NULL"), nullable=True, index=True)
    payment_id = Column(String(36), ForeignKey("payments.id", ondelete="RESTRICT"), nullable=False, index=True)
    sale_id = Column(String(36), ForeignKey("sales.id", ondelete="RESTRICT"), nullable=True, index=True)
    approved_by_id = Column(String(36), ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    
    amount = Column(Numeric(12, 2), nullable=False)
    reason = Column(Text, nullable=False)
    status = Column(String(50), default="APPROVED", index=True)  # APPROVED, PROCESSED, REJECTED
    gateway_refund_id = Column(String(100), nullable=True)
    
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)

    payment = relationship("Payment", back_populates="refunds")
