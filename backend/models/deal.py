from enum import Enum
from typing import Optional
from datetime import datetime

class DealStage(str, Enum):
    PROSPECT = "prospect"
    DISCOVERY = "discovery"
    QUALIFIED = "qualified"
    PROPOSAL = "proposal"
    NEGOTIATION = "negotiation"
    CLOSED_WON = "closed_won"
    CLOSED_LOST = "closed_lost"
    ON_HOLD = "on_hold"

class Deal:
    def __init__(
        self,
        id: str,
        lead_id: str,
        company_name: str,
        deal_name: str,
        amount: float,
        currency: str,
        stage: DealStage,
        created_at: datetime,
        expected_close_date: Optional[datetime] = None,
        close_date: Optional[datetime] = None,
        win_probability: float = 0.0,
        notes: Optional[str] = None,
        assigned_to: Optional[str] = None,
        custom_fields: Optional[dict] = None,
    ):
        self.id = id
        self.lead_id = lead_id
        self.company_name = company_name
        self.deal_name = deal_name
        self.amount = amount
        self.currency = currency
        self.stage = stage
        self.created_at = created_at
        self.expected_close_date = expected_close_date
        self.close_date = close_date
        self.win_probability = win_probability
        self.notes = notes
        self.assigned_to = assigned_to
        self.custom_fields = custom_fields or {}

    def to_dict(self):
        return {
            "id": self.id,
            "lead_id": self.lead_id,
            "company_name": self.company_name,
            "deal_name": self.deal_name,
            "amount": self.amount,
            "currency": self.currency,
            "stage": self.stage.value,
            "created_at": self.created_at.isoformat(),
            "expected_close_date": self.expected_close_date.isoformat() if self.expected_close_date else None,
            "close_date": self.close_date.isoformat() if self.close_date else None,
            "win_probability": self.win_probability,
            "notes": self.notes,
            "assigned_to": self.assigned_to,
            "custom_fields": self.custom_fields,
        }
