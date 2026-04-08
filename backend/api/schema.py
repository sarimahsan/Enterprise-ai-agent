from pydantic import BaseModel, EmailStr, Field
from typing import List, Dict, Optional
from datetime import datetime
from enum import Enum

# ============ ENUMS ============
class EmailStatus(str, Enum):
    DRAFT = "draft"
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"
    BOUNCED = "bounced"
    READ = "read"

class EmailPriority(str, Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"

# ============ REQUEST SCHEMAS ============
class GoalRequest(BaseModel):
    company: str = Field(..., min_length=1, description="Company name")
    goal: str = Field(..., min_length=1, description="Outreach goal")

class SendEmailRequest(BaseModel):
    to_email: EmailStr = Field(..., description="Recipient email address")
    subject: str = Field(..., min_length=1, description="Email subject")
    html_body: str = Field(..., min_length=1, description="HTML email body")
    cc: Optional[str] = Field(None, description="CC email address")
    bcc: Optional[str] = Field(None, description="BCC email address")
    priority: EmailPriority = Field(EmailPriority.NORMAL, description="Email priority")

class SendProfessionalEmailRequest(BaseModel):
    to_email: EmailStr
    company: str
    subject_line: str
    body_content: str
    decision_maker: str = ""
    priority: EmailPriority = EmailPriority.NORMAL

class BulkEmailRequest(BaseModel):
    recipients: List[Dict[str, str]] = Field(..., description="List of {email, name, company}")
    subject: str
    html_body: str

# ============ RESPONSE SCHEMAS ============
class EmailTrackingInfo(BaseModel):
    id: str
    to_email: str
    subject: str
    status: EmailStatus
    priority: EmailPriority
    created_at: datetime
    sent_at: Optional[datetime] = None
    attempts: int
    message_id: Optional[str] = None
    error: Optional[str] = None

class EmailSendResponse(BaseModel):
    success: bool
    message: str
    email_id: Optional[str] = None
    message_id: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)

class AgentResponse(BaseModel):
    emails: Dict
    email_templates: Dict
    analysis: Dict
    variants: Dict
    logs: List[str]
    tasks: List[str]
    analytics: Dict
    follow_up_schedule: Dict

class EmailStats(BaseModel):
    total_sent: int
    pending: int
    failed: int
    success_rate: float
    sent_emails: List[EmailTrackingInfo]
    pending_emails: List[EmailTrackingInfo]
    failed_emails: List[EmailTrackingInfo]

class GmailAuthStatus(BaseModel):
    is_authenticated: bool
    email: Optional[str] = None
    message_count: Optional[int] = None
    threads_count: Optional[int] = None
    status: str

# ============ CALENDAR REQUEST MODELS ============
class ScheduleCampaignRequest(BaseModel):
    company: str = Field(..., min_length=1, description="Company name")
    campaign_name: str = Field(..., min_length=1, description="Campaign name")
    send_time: str = Field(..., description="ISO format datetime string")

class ScheduleFollowupRequest(BaseModel):
    campaign_name: str = Field(..., min_length=1, description="Campaign name")
    initial_time: str = Field(..., description="ISO format datetime string")
    followup_days: int = Field(3, ge=1, le=30, description="Days until follow-up")

# ============ LINKEDIN REQUEST MODELS ============
class GetMembersRequest(BaseModel):
    company_name: str = Field(..., min_length=1, description="Company name")
    department: Optional[str] = Field(None, description="Department to filter by")
    limit: int = Field(50, ge=1, le=250, description="Max members to return")

class GenerateMessagesRequest(BaseModel):
    company_name: str = Field(..., min_length=1, description="Company name")
    department: Optional[str] = Field(None, description="Department to filter by")
    campaign_topic: str = Field("partnership opportunity", description="Campaign topic")
    tone: str = Field("professional", description="Message tone: professional, casual, consultative")
    limit: int = Field(50, ge=1, le=250, description="Max members to generate for")

class GenerateSingleMessageRequest(BaseModel):
    member_name: str = Field(..., min_length=1, description="Member name")
    member_title: str = Field(..., min_length=1, description="Member job title")
    company_name: str = Field(..., min_length=1, description="Company name")
    campaign_topic: str = Field(..., min_length=1, description="Campaign topic")
    tone: str = Field("professional", description="Message tone")