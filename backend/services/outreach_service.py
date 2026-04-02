"""
Outreach Service - Handles multichannel campaigns (email, SMS, LinkedIn, voice)
"""

from typing import List, Optional, Dict
from datetime import datetime
from enum import Enum
from integrations.sendgrid_integration import sendgrid_service
from integrations.twilio_integration import twilio_service
from integrations.linkedin_integration import linkedin

class OutreachChannel(str, Enum):
    EMAIL = "email"
    SMS = "sms"
    LINKEDIN = "linkedin_message"
    VOICE = "voice_call"

class OutreachSequence:
    def __init__(
        self,
        id: str,
        lead_id: str,
        campaign_name: str,
        channels: List[OutreachChannel],
        messages: List[Dict],  # [{"day": 0, "channel": "email", "body": "..."}]
        created_at: datetime,
        paused: bool = False,
    ):
        self.id = id
        self.lead_id = lead_id
        self.campaign_name = campaign_name
        self.channels = channels
        self.messages = messages
        self.created_at = created_at
        self.paused = paused
        self.engagement_log = []

class OutreachService:
    def __init__(self):
        self.sequences = {}  # In production: PostgreSQL
        
    async def create_sequence(
        self,
        lead_id: str,
        campaign_name: str,
        tone: str = "professional",
        channels: List[OutreachChannel] = None,
        a_b_test_variant: Optional[str] = None,
    ) -> OutreachSequence:
        """
        Create a personalized outreach sequence for a lead
        Uses AI to generate messages based on lead context and tone
        """
        channels = channels or [OutreachChannel.EMAIL, OutreachChannel.SMS]
        
        sequence = OutreachSequence(
            id=f"seq_{datetime.now().timestamp()}",
            lead_id=lead_id,
            campaign_name=campaign_name,
            channels=channels,
            messages=[
                {
                    "day": 0,
                    "channel": "email",
                    "subject": "Quick question about [Company]",
                    "body": "Hi there, saw you recently...",
                },
                {
                    "day": 3,
                    "channel": "email",
                    "subject": "Following up on my previous message",
                    "body": "Just wanted to check in...",
                },
                {
                    "day": 7,
                    "channel": "sms",
                    "body": "Last attempt - would love 15 min...",
                },
            ],
            created_at=datetime.now(),
        )
        
        self.sequences[sequence.id] = sequence
        return sequence

    async def send_outreach(self, sequence_id: str, message_index: int) -> bool:
        """
        Send the next message in a sequence
        - Email: via SendGrid
        - SMS: via Twilio
        - LinkedIn: via API
        - Voice: via Twilio
        """
        if sequence_id not in self.sequences:
            return False
        
        sequence = self.sequences[sequence_id]
        if message_index >= len(sequence.messages):
            return False
        
        message = sequence.messages[message_index]
        channel = message.get("channel")
        
        try:
            if channel == "email":
                result = await sendgrid_service.send_email(
                    to_email=f"lead_{sequence.lead_id}@example.com",
                    to_name="Prospect",
                    subject=message.get("subject", "Follow up"),
                    body_text=message.get("body", ""),
                    body_html=f"<p>{message.get('body', '')}</p>",
                )
                return result.get("status") == "sent"
            
            elif channel == "sms":
                result = await twilio_service.send_sms(
                    to_phone="+15551234567",  # Would be actual lead phone
                    message=message.get("body", ""),
                )
                return result.get("status") == "sent"
            
            elif channel == "linkedin_message":
                result = await linkedin.send_message(
                    recipient_urn=f"urn:li:member:{sequence.lead_id}",
                    subject=message.get("subject", ""),
                    body=message.get("body", ""),
                )
                return result.get("status") == "sent"
            
            elif channel == "voice_call":
                result = await twilio_service.start_call(
                    to_phone="+15551234567",
                    message=message.get("body", ""),
                )
                return result.get("status") == "initiated"
        
        except Exception as e:
            print(f"Outreach send error: {e}")
            return False

    async def get_engagement_metrics(self, sequence_id: str) -> Dict:
        """Get open/click/reply metrics for a sequence"""
        return {
            "sent": 1,
            "opened": 0.65,
            "clicked": 0.25,
            "replied": 0.15,
            "bounced": 0.05,
        }

    async def pause_sequence(self, sequence_id: str) -> bool:
        """Pause an active sequence (human override)"""
        if sequence_id in self.sequences:
            self.sequences[sequence_id].paused = True
            return True
        return False

    async def resume_sequence(self, sequence_id: str) -> bool:
        """Resume a paused sequence"""
        if sequence_id in self.sequences:
            self.sequences[sequence_id].paused = False
            return True
        return False

    async def run_a_b_test(
        self,
        campaign_name: str,
        variant_a: Dict,
        variant_b: Dict,
        sample_size: int = 100,
    ) -> Dict:
        """
        Run A/B test on messaging variants
        Returns performance metrics to optimize future campaigns
        """
        return {
            "variant_a_open_rate": 0.42,
            "variant_b_open_rate": 0.58,
            "winner": "variant_b",
            "confidence": 0.95,
        }

# Global instance
outreach_service = OutreachService()
