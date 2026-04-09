"""
SQLAlchemy database models for FlowForge
"""
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, Boolean, ForeignKey, JSON, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base
import enum


class Company(Base):
    """Company/Lead model"""
    __tablename__ = "companies"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True, nullable=False)
    industry = Column(String(100))
    size = Column(String(50))  # e.g., "startup", "mid-market", "enterprise"
    website = Column(String(255))
    revenue_range = Column(String(100))
    decision_maker = Column(String(255))
    decision_maker_email = Column(String(255))
    location = Column(String(255))
    
    # Scoring
    opportunity_score = Column(Float, default=0.0)  # 0-100
    urgency_level = Column(String(50), default="medium")  # low, medium, high, critical
    fit_score = Column(Float, default=0.0)
    
    # Metadata
    research_data = Column(JSON)  # Store research results
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    campaigns = relationship("Campaign", back_populates="company")
    emails = relationship("Email", back_populates="company")

    def __repr__(self):
        return f"<Company {self.name}>"


class Campaign(Base):
    """Campaign model"""
    __tablename__ = "campaigns"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    name = Column(String(255), nullable=False)
    goal = Column(Text, nullable=False)
    
    # Campaign details
    analysis_data = Column(JSON)  # AI analysis results
    discovered_pain_points = Column(JSON)  # List of pain points
    unique_angle = Column(Text)
    
    # Status
    status = Column(String(50), default="draft")  # draft, active, completed, paused
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    company = relationship("Company", back_populates="campaigns")
    emails = relationship("Email", back_populates="campaign")
    objections = relationship("Objection", back_populates="campaign")

    def __repr__(self):
        return f"<Campaign {self.name}>"


class Email(Base):
    """Email model"""
    __tablename__ = "emails"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=False)
    
    sequence_number = Column(Integer)  # 1, 2, 3, etc.
    subject = Column(String(255), nullable=False)
    body = Column(Text, nullable=False)
    html_body = Column(Text)
    
    # Email variants
    variant_type = Column(String(50))  # aggressive, soft, balanced
    
    # Scoring & Feedback
    confidence_score = Column(Float)  # 0-100
    personalization_score = Column(Float)  # 0-10
    subject_quality_feedback = Column(Text)
    quality_feedback = Column(JSON)  # Structured feedback
    recommended_changes = Column(JSON)
    
    # Sending
    to_email = Column(String(255))
    status = Column(String(50), default="draft")  # draft, scheduled, sent, failed, read
    sent_at = Column(DateTime)
    opened_at = Column(DateTime)
    clicked_at = Column(DateTime)
    reply_received_at = Column(DateTime)
    
    # Tracking
    open_count = Column(Integer, default=0)
    click_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    company = relationship("Company", back_populates="emails")
    campaign = relationship("Campaign", back_populates="emails")
    variants = relationship("EmailVariant", back_populates="email")

    def __repr__(self):
        return f"<Email {self.subject}>"


class EmailVariant(Base):
    """Email A/B variant model"""
    __tablename__ = "email_variants"
    
    id = Column(Integer, primary_key=True, index=True)
    email_id = Column(Integer, ForeignKey("emails.id"), nullable=False)
    
    variant_letter = Column(String(1))  # A, B
    subject = Column(String(255))
    body = Column(Text)
    approach = Column(String(50))  # aggressive, soft
    
    # Performance
    send_count = Column(Integer, default=0)
    open_count = Column(Integer, default=0)
    click_count = Column(Integer, default=0)
    reply_count = Column(Integer, default=0)
    conversion_count = Column(Integer, default=0)
    
    open_rate = Column(Float, default=0.0)
    click_rate = Column(Float, default=0.0)
    reply_rate = Column(Float, default=0.0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    email = relationship("Email", back_populates="variants")

    def __repr__(self):
        return f"<EmailVariant {self.variant_letter}>"


class EmailScore(Base):
    """Email quality score from QA agent"""
    __tablename__ = "email_scores"
    
    id = Column(Integer, primary_key=True, index=True)
    email_id = Column(Integer, ForeignKey("emails.id"), nullable=False)
    
    overall_score = Column(Float)  # 0-100
    subject_line_score = Column(Float)
    body_quality_score = Column(Float)
    personalization_score = Column(Float)  # 0-10
    call_to_action_score = Column(Float)
    
    # Detailed feedback
    subject_feedback = Column(Text)
    body_feedback = Column(Text)
    personalization_feedback = Column(Text)
    cta_feedback = Column(Text)
    
    # Recommendations
    issues_found = Column(JSON)  # List of issues
    recommendations = Column(JSON)  # List of improvements
    
    reviewed_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<EmailScore {self.overall_score}>"


class Objection(Base):
    """Likely objections and pre-generated responses"""
    __tablename__ = "objections"
    
    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=False)
    
    objection_number = Column(Integer)  # 1, 2, 3
    objection_text = Column(Text)  # e.g., "That's too expensive"
    likelihood = Column(String(50))  # high, medium, low
    likelihood_percentage = Column(Float)
    
    # Pre-generated responses
    response_text = Column(Text)
    response_approach = Column(String(50))  # empathetic, logical, social_proof
    
    # Alternative responses
    alternative_responses = Column(JSON)  # List of alternative responses
    
    # Context
    context = Column(Text)  # Why this objection is likely
    triggers = Column(JSON)  # What triggers this objection
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    campaign = relationship("Campaign", back_populates="objections")

    def __repr__(self):
        return f"<Objection {self.objection_text[:30]}>"


class FollowUp(Base):
    """Follow-up timeline and scheduling"""
    __tablename__ = "followups"
    
    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=False)
    email_id = Column(Integer, ForeignKey("emails.id"), nullable=False)
    
    sequence_day = Column(Integer)  # Day 1, Day 4, Day 8
    suggested_send_time = Column(DateTime)
    calendar_event_id = Column(String(255))  # Google Calendar event ID
    
    # Industry-based recommendations
    industry = Column(String(100))
    rationale = Column(Text)  # Why this timing
    
    # Status
    scheduled = Column(Boolean, default=False)
    sent = Column(Boolean, default=False)
    sent_at = Column(DateTime)
    
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<FollowUp Day {self.sequence_day}>"


class Export(Base):
    """Track exports to Notion/Google Docs"""
    __tablename__ = "exports"
    
    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=False)
    
    export_type = Column(String(50))  # notion, google_docs
    destination_url = Column(String(500))
    destination_id = Column(String(255))  # Notion page ID or Google Doc ID
    
    content_type = Column(String(50))  # full_report, email_sequence, objections
    
    # Metadata
    exported_at = Column(DateTime, default=datetime.utcnow)
    last_synced_at = Column(DateTime)
    is_active = Column(Boolean, default=True)

    def __repr__(self):
        return f"<Export {self.export_type}>"


class Analytics(Base):
    """Campaign analytics and performance metrics"""
    __tablename__ = "analytics"
    
    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=False)
    
    # Email performance
    emails_sent = Column(Integer, default=0)
    emails_opened = Column(Integer, default=0)
    emails_clicked = Column(Integer, default=0)
    emails_replied = Column(Integer, default=0)
    emails_bounced = Column(Integer, default=0)
    
    # Rates
    open_rate = Column(Float, default=0.0)
    click_rate = Column(Float, default=0.0)
    reply_rate = Column(Float, default=0.0)
    bounce_rate = Column(Float, default=0.0)
    conversion_rate = Column(Float, default=0.0)
    
    # Quality metrics
    avg_confidence_score = Column(Float)
    avg_personalization_score = Column(Float)
    
    # Timeline
    first_sent_at = Column(DateTime)
    last_sent_at = Column(DateTime)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Analytics Campaign {self.campaign_id}>"
