"""
Database service layer for CRUD operations and business logic
"""
from sqlalchemy.orm import Session
from sqlalchemy import and_, desc
from datetime import datetime, timedelta
from typing import List, Optional, Dict
from models.database_models import (
    Company, Campaign, Email, EmailVariant, EmailScore, 
    Objection, FollowUp, Export, Analytics
)


class CompanyService:
    """Service for company/lead management"""
    
    @staticmethod
    def create_company(db: Session, name: str, industry: str = None, 
                      website: str = None, **kwargs) -> Company:
        company = Company(name=name, industry=industry, website=website, **kwargs)
        db.add(company)
        db.commit()
        db.refresh(company)
        return company
    
    @staticmethod
    def get_company_by_name(db: Session, name: str) -> Optional[Company]:
        return db.query(Company).filter(Company.name == name).first()
    
    @staticmethod
    def get_company_by_id(db: Session, company_id: int) -> Optional[Company]:
        return db.query(Company).filter(Company.id == company_id).first()
    
    @staticmethod
    def get_all_companies(db: Session, skip: int = 0, limit: int = 100) -> List[Company]:
        return db.query(Company).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_companies_by_opportunity_score(db: Session, limit: int = 50) -> List[Company]:
        """Get companies sorted by opportunity score (highest first)"""
        return db.query(Company).order_by(desc(Company.opportunity_score)).limit(limit).all()
    
    @staticmethod
    def update_opportunity_score(db: Session, company_id: int, score: float) -> Company:
        company = db.query(Company).filter(Company.id == company_id).first()
        if company:
            company.opportunity_score = score
            db.commit()
            db.refresh(company)
        return company
    
    @staticmethod
    def update_urgency_level(db: Session, company_id: int, urgency: str) -> Company:
        company = db.query(Company).filter(Company.id == company_id).first()
        if company:
            company.urgency_level = urgency
            db.commit()
            db.refresh(company)
        return company


class CampaignService:
    """Service for campaign management"""
    
    @staticmethod
    def create_campaign(db: Session, company_id: int, name: str, 
                       goal: str, analysis_data: Dict = None) -> Campaign:
        campaign = Campaign(
            company_id=company_id,
            name=name,
            goal=goal,
            analysis_data=analysis_data or {}
        )
        db.add(campaign)
        db.commit()
        db.refresh(campaign)
        return campaign
    
    @staticmethod
    def get_campaign_by_id(db: Session, campaign_id: int) -> Optional[Campaign]:
        return db.query(Campaign).filter(Campaign.id == campaign_id).first()
    
    @staticmethod
    def get_campaigns_by_company(db: Session, company_id: int) -> List[Campaign]:
        return db.query(Campaign).filter(Campaign.company_id == company_id).all()
    
    @staticmethod
    def update_campaign_status(db: Session, campaign_id: int, status: str) -> Campaign:
        campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
        if campaign:
            campaign.status = status
            campaign.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(campaign)
        return campaign


class EmailService:
    """Service for email management"""
    
    @staticmethod
    def create_email(db: Session, company_id: int, campaign_id: int,
                    subject: str, body: str, sequence_number: int = 1,
                    variant_type: str = "balanced", **kwargs) -> Email:
        email = Email(
            company_id=company_id,
            campaign_id=campaign_id,
            subject=subject,
            body=body,
            sequence_number=sequence_number,
            variant_type=variant_type,
            **kwargs
        )
        db.add(email)
        db.commit()
        db.refresh(email)
        return email
    
    @staticmethod
    def get_email_by_id(db: Session, email_id: int) -> Optional[Email]:
        return db.query(Email).filter(Email.id == email_id).first()
    
    @staticmethod
    def get_emails_by_campaign(db: Session, campaign_id: int) -> List[Email]:
        return db.query(Email).filter(Email.campaign_id == campaign_id).order_by(Email.sequence_number).all()
    
    @staticmethod
    def update_email_status(db: Session, email_id: int, status: str, 
                           sent_at: datetime = None) -> Email:
        email = db.query(Email).filter(Email.id == email_id).first()
        if email:
            email.status = status
            if sent_at:
                email.sent_at = sent_at
            db.commit()
            db.refresh(email)
        return email
    
    @staticmethod
    def update_email_scores(db: Session, email_id: int, confidence_score: float,
                           personalization_score: float, quality_feedback: Dict) -> Email:
        email = db.query(Email).filter(Email.id == email_id).first()
        if email:
            email.confidence_score = confidence_score
            email.personalization_score = personalization_score
            email.quality_feedback = quality_feedback
            db.commit()
            db.refresh(email)
        return email


class EmailScoreService:
    """Service for email quality scores"""
    
    @staticmethod
    def create_email_score(db: Session, email_id: int, overall_score: float,
                          scores_dict: Dict, feedback_dict: Dict,
                          recommendations: List = None, issues_found: List = None) -> EmailScore:
        email_score = EmailScore(
            email_id=email_id,
            overall_score=overall_score,
            subject_line_score=scores_dict.get("subject_line_score"),
            body_quality_score=scores_dict.get("body_quality_score"),
            personalization_score=scores_dict.get("personalization_score"),
            call_to_action_score=scores_dict.get("call_to_action_score"),
            subject_feedback=feedback_dict.get("subject_feedback"),
            body_feedback=feedback_dict.get("body_feedback"),
            personalization_feedback=feedback_dict.get("personalization_feedback"),
            cta_feedback=feedback_dict.get("cta_feedback"),
            recommendations=recommendations or [],
            issues_found=issues_found or []
        )
        db.add(email_score)
        db.commit()
        db.refresh(email_score)
        return email_score
    
    @staticmethod
    def get_email_score(db: Session, email_id: int) -> Optional[EmailScore]:
        return db.query(EmailScore).filter(EmailScore.email_id == email_id).first()


class ObjectionService:
    """Service for objection management"""
    
    @staticmethod
    def create_objections(db: Session, campaign_id: int, objections_list: List[Dict]) -> List[Objection]:
        created_objections = []
        for idx, obj_data in enumerate(objections_list, 1):
            objection = Objection(
                campaign_id=campaign_id,
                objection_number=idx,
                objection_text=obj_data.get("objection"),
                likelihood=obj_data.get("likelihood", "medium"),
                likelihood_percentage=obj_data.get("likelihood_percentage", 0),
                response_text=obj_data.get("response"),
                response_approach=obj_data.get("approach", "empathetic"),
                alternative_responses=obj_data.get("alternatives", []),
                context=obj_data.get("context"),
                triggers=obj_data.get("triggers", [])
            )
            db.add(objection)
            created_objections.append(objection)
        
        db.commit()
        return created_objections
    
    @staticmethod
    def get_objections_by_campaign(db: Session, campaign_id: int) -> List[Objection]:
        return db.query(Objection).filter(Objection.campaign_id == campaign_id).order_by(Objection.objection_number).all()


class FollowUpService:
    """Service for follow-up scheduling"""
    
    @staticmethod
    def create_followup(db: Session, campaign_id: int, email_id: int,
                       sequence_day: int, suggested_send_time: datetime,
                       industry: str = None, rationale: str = None) -> FollowUp:
        followup = FollowUp(
            campaign_id=campaign_id,
            email_id=email_id,
            sequence_day=sequence_day,
            suggested_send_time=suggested_send_time,
            industry=industry,
            rationale=rationale
        )
        db.add(followup)
        db.commit()
        db.refresh(followup)
        return followup
    
    @staticmethod
    def get_followups_by_campaign(db: Session, campaign_id: int) -> List[FollowUp]:
        return db.query(FollowUp).filter(FollowUp.campaign_id == campaign_id).order_by(FollowUp.sequence_day).all()
    
    @staticmethod
    def schedule_followup(db: Session, followup_id: int, calendar_event_id: str) -> FollowUp:
        followup = db.query(FollowUp).filter(FollowUp.id == followup_id).first()
        if followup:
            followup.scheduled = True
            followup.calendar_event_id = calendar_event_id
            db.commit()
            db.refresh(followup)
        return followup


class AnalyticsService:
    """Service for analytics tracking"""
    
    @staticmethod
    def create_analytics(db: Session, campaign_id: int) -> Analytics:
        analytics = Analytics(campaign_id=campaign_id)
        db.add(analytics)
        db.commit()
        db.refresh(analytics)
        return analytics
    
    @staticmethod
    def get_analytics_by_campaign(db: Session, campaign_id: int) -> Optional[Analytics]:
        return db.query(Analytics).filter(Analytics.campaign_id == campaign_id).first()
    
    @staticmethod
    def update_analytics(db: Session, campaign_id: int, **updates) -> Analytics:
        analytics = db.query(Analytics).filter(Analytics.campaign_id == campaign_id).first()
        if analytics:
            for key, value in updates.items():
                setattr(analytics, key, value)
            analytics.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(analytics)
        return analytics


class ExportService:
    """Service for managing exports"""
    
    @staticmethod
    def create_export(db: Session, campaign_id: int, export_type: str,
                     destination_url: str, destination_id: str,
                     content_type: str = "full_report") -> Export:
        export = Export(
            campaign_id=campaign_id,
            export_type=export_type,
            destination_url=destination_url,
            destination_id=destination_id,
            content_type=content_type
        )
        db.add(export)
        db.commit()
        db.refresh(export)
        return export
    
    @staticmethod
    def get_exports_by_campaign(db: Session, campaign_id: int) -> List[Export]:
        return db.query(Export).filter(
            and_(Export.campaign_id == campaign_id, Export.is_active == True)
        ).all()
