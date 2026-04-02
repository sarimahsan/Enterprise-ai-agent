from enum import Enum
from typing import Optional
from datetime import datetime

class InteractionType(str, Enum):
    EMAIL = "email"
    SMS = "sms"
    LINKEDIN_MESSAGE = "linkedin_message"
    CALL = "call"
    MEETING = "meeting"
    NOTE = "note"
    TASK = "task"

class InteractionStatus(str, Enum):
    PENDING = "pending"
    SENT = "sent"
    OPENED = "opened"
    CLICKED = "clicked"
    REPLIED = "replied"
    SCHEDULED = "scheduled"
    COMPLETED = "completed"
    FAILED = "failed"

class Interaction:
    def __init__(
        self,
        id: str,
        lead_id: str,
        interaction_type: InteractionType,
        status: InteractionStatus,
        created_at: datetime,
        subject: Optional[str] = None,
        body: Optional[str] = None,
        initiated_by: Optional[str] = None,  # "agent" or user name
        channel: Optional[str] = None,
        engagement_metadata: Optional[dict] = None,
        duration_seconds: Optional[int] = None,
        notes: Optional[str] = None,
    ):
        self.id = id
        self.lead_id = lead_id
        self.interaction_type = interaction_type
        self.status = status
        self.created_at = created_at
        self.subject = subject
        self.body = body
        self.initiated_by = initiated_by or "agent"
        self.channel = channel
        self.engagement_metadata = engagement_metadata or {}
        self.duration_seconds = duration_seconds
        self.notes = notes

    def to_dict(self):
        return {
            "id": self.id,
            "lead_id": self.lead_id,
            "interaction_type": self.interaction_type.value,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "subject": self.subject,
            "body": self.body,
            "initiated_by": self.initiated_by,
            "channel": self.channel,
            "engagement_metadata": self.engagement_metadata,
            "duration_seconds": self.duration_seconds,
            "notes": self.notes,
        }
