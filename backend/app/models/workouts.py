"""
Workouts, Exercises, Instructions & Fitness Measurements Models
"""
import uuid
from datetime import datetime, timezone, date
from sqlalchemy import Column, String, DateTime, ForeignKey, Integer, Numeric, Text, Date
from sqlalchemy.orm import relationship
from app.core.database import Base


def utc_now():
    return datetime.now(timezone.utc)


class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    organization_id = Column(String(36), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=True, index=True)
    
    name = Column(String(255), nullable=False, index=True)
    category = Column(String(100), default="Strength")  # Strength, Cardio, Flexibility, Olympic
    target_muscle = Column(String(100), nullable=True)  # Chest, Back, Legs, Shoulders, Core
    equipment = Column(String(100), nullable=True)  # Barbell, Dumbbell, Cable, Bodyweight
    instructions = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)


class WorkoutPlan(Base):
    __tablename__ = "workout_plans"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    organization_id = Column(String(36), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    branch_id = Column(String(36), ForeignKey("branches.id", ondelete="SET NULL"), nullable=True, index=True)
    client_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    trainer_id = Column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    diet_instructions = Column(Text, nullable=True)
    trainer_notes = Column(Text, nullable=True)
    
    is_active = Column(String(50), default="ACTIVE")
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False)

    items = relationship("WorkoutPlanItem", back_populates="plan", cascade="all, delete-orphan")


class WorkoutPlanItem(Base):
    __tablename__ = "workout_plan_items"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    workout_plan_id = Column(String(36), ForeignKey("workout_plans.id", ondelete="CASCADE"), nullable=False, index=True)
    exercise_id = Column(String(36), ForeignKey("exercises.id", ondelete="RESTRICT"), nullable=False)
    
    day_of_week = Column(String(20), default="Monday")  # Monday, Tuesday, etc.
    sets = Column(Integer, default=3, nullable=False)
    reps = Column(String(50), default="10-12", nullable=False)
    target_weight_kg = Column(Numeric(6, 2), nullable=True)
    rest_seconds = Column(Integer, default=60, nullable=False)
    
    plan = relationship("WorkoutPlan", back_populates="items")


class FitnessMeasurement(Base):
    __tablename__ = "fitness_measurements"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    organization_id = Column(String(36), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    client_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    recorded_by_id = Column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    
    recorded_date = Column(Date, default=date.today, nullable=False, index=True)
    weight_kg = Column(Numeric(5, 2), nullable=False)
    height_cm = Column(Numeric(5, 2), nullable=True)
    body_fat_percentage = Column(Numeric(4, 1), nullable=True)
    chest_cm = Column(Numeric(5, 2), nullable=True)
    waist_cm = Column(Numeric(5, 2), nullable=True)
    arms_cm = Column(Numeric(5, 2), nullable=True)
    notes = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)
