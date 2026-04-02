from enum import Enum
from typing import Optional, List
from datetime import datetime

class LeadSource(str, Enum):
    LINKEDIN = "linkedin"
    APOLLO = "apollo"
    HUNTER = "hunter"
    WEBSITE = "website"
    INTENT_SIGNAL = "intent_signal"
    MANUAL = "manual"

class LeadScore(str, Enum):
    HOT = "hot"
    WARM = "warm"
    COLD = "cold"

class Lead:
    def __init__(
        self,
        id: str,
        first_name: str,
        last_name: str,
        email: str,
        company_name: str,
        title: str,
        source: LeadSource,
        score: LeadScore,
        created_at: datetime,
        last_contacted: Optional[datetime] = None,
        phone: Optional[str] = None,
        linkedin_url: Optional[str] = None,
        firmographics: Optional[dict] = None,
        technographics: Optional[dict] = None,
        buying_signals: Optional[List[str]] = None,
        notes: Optional[str] = None,
        custom_fields: Optional[dict] = None,
    ):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.company_name = company_name
        self.title = title
        self.source = source
        self.score = score
        self.created_at = created_at
        self.last_contacted = last_contacted
        self.phone = phone
        self.linkedin_url = linkedin_url
        self.firmographics = firmographics or {}
        self.technographics = technographics or {}
        self.buying_signals = buying_signals or []
        self.notes = notes
        self.custom_fields = custom_fields or {}

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "company_name": self.company_name,
            "title": self.title,
            "source": self.source.value,
            "score": self.score.value,
            "created_at": self.created_at.isoformat(),
            "last_contacted": self.last_contacted.isoformat() if self.last_contacted else None,
            "phone": self.phone,
            "linkedin_url": self.linkedin_url,
            "firmographics": self.firmographics,
            "technographics": self.technographics,
            "buying_signals": self.buying_signals,
            "notes": self.notes,
            "custom_fields": self.custom_fields,
        }
