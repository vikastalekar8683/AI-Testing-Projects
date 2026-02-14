from sqlalchemy import create_engine, Column, Integer, String, Boolean, Date, Float, ForeignKey, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

DATABASE_URL = "sqlite:///./applications.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Application(Base):
    __tablename__ = "applications"
    id = Column(Integer, primary_key=True, index=True)
    job_title = Column(String)
    company_name = Column(String)
    location = Column(String, nullable=True)
    job_type = Column(String, nullable=True)
    work_model = Column(String, nullable=True)
    industry = Column(String, nullable=True)
    application_date = Column(Date, default=datetime.now().date)
    job_url = Column(String, nullable=True)
    company_website = Column(String, nullable=True)
    job_description = Column(Text, nullable=True)
    salary_range = Column(String, nullable=True)
    deadline = Column(Date, nullable=True)
    source = Column(String, nullable=True)
    source_details = Column(String, nullable=True)
    resume_version = Column(String, nullable=True)
    cover_letter_used = Column(Boolean, default=False)
    cover_letter_version = Column(String, nullable=True)
    portfolio_submitted = Column(Boolean, default=False)
    recruiter_name = Column(String, nullable=True)
    recruiter_email = Column(String, nullable=True)
    recruiter_phone = Column(String, nullable=True)
    hr_contact = Column(String, nullable=True)
    hiring_manager = Column(String, nullable=True)
    match_score = Column(Integer, nullable=True)
    interest_level = Column(Integer, nullable=True)
    priority = Column(String, default="Medium")
    keywords = Column(Text, nullable=True)
    skills_required = Column(Text, nullable=True)
    skills_have = Column(Text, nullable=True)
    skills_need = Column(Text, nullable=True)
    status = Column(String, default="To Apply")
    notes = Column(Text, nullable=True)
    interview_notes = Column(Text, nullable=True)
    questions_to_ask = Column(Text, nullable=True)
    red_flags = Column(Text, nullable=True)
    culture_notes = Column(Text, nullable=True)
    created_at = Column(Date, default=datetime.now)
    updated_at = Column(Date, default=datetime.now, onupdate=datetime.now)
    archived = Column(Boolean, default=False)

    history = relationship("StatusHistory", back_populates="application")
    interviews = relationship("Interview", back_populates="application")
    reminders = relationship("Reminder", back_populates="application")

class StatusHistory(Base):
    __tablename__ = "status_history"
    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id"))
    old_status = Column(String)
    new_status = Column(String)
    changed_at = Column(Date, default=datetime.now)
    notes = Column(Text, nullable=True)

    application = relationship("Application", back_populates="history")

class Interview(Base):
    __tablename__ = "interviews"
    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id"))
    interview_type = Column(String)
    interview_date = Column(Date)
    interview_time = Column(String, nullable=True)
    interviewer_name = Column(String, nullable=True)
    interviewer_title = Column(String, nullable=True)
    location = Column(String, nullable=True)
    meeting_link = Column(String, nullable=True)
    preparation_status = Column(String, default="Pending")
    outcome = Column(String, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(Date, default=datetime.now)

    application = relationship("Application", back_populates="interviews")

class Reminder(Base):
    __tablename__ = "reminders"
    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id"))
    reminder_type = Column(String)
    reminder_date = Column(Date)
    reminder_time = Column(String, nullable=True)
    message = Column(Text)
    completed = Column(Boolean, default=False)
    created_at = Column(Date, default=datetime.now)

    application = relationship("Application", back_populates="reminders")

class Goal(Base):
    __tablename__ = "goals"
    id = Column(Integer, primary_key=True, index=True)
    goal_type = Column(String)
    target_value = Column(Integer)
    time_period = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)
    created_at = Column(Date, default=datetime.now)

Base.metadata.create_all(bind=engine)
