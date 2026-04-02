from typing import Dict, Optional
from core.config import settings


class TwilioIntegration:
    """Twilio integration for SMS and voice calls"""

    def __init__(self):
        self.account_sid = settings.TWILIO_ACCOUNT_SID
        self.auth_token = settings.TWILIO_AUTH_TOKEN
        self.from_number = settings.TWILIO_PHONE_NUMBER
        self.client = None
        self._initialized = False

    async def initialize(self):
        """Initialize Twilio client"""
        if not self.account_sid or not self.auth_token:
            return False

        try:
            from twilio.rest import Client

            self.client = Client(self.account_sid, self.auth_token)
            self._initialized = True
            return True
        except Exception as e:
            print(f"Twilio initialization error: {e}")
            return False

    async def send_sms(self, to_phone: str, message: str) -> Dict:
        """
        Send SMS message
        
        Args:
            to_phone: Recipient phone number (e.g., +1234567890)
            message: SMS message content
            
        Returns:
            Dict with status, message_id, and delivery details
        """
        if not self._initialized:
            # Mock SMS sending
            return {
                "status": "sent",
                "message_id": f"mock_sms_{to_phone}",
                "to": to_phone,
                "body": message,
            }

        try:
            sms = self.client.messages.create(
                body=message,
                from_=self.from_number,
                to=to_phone,
            )

            return {
                "status": "sent",
                "message_id": sms.sid,
                "to": to_phone,
                "body": message,
                "price": str(sms.price) if sms.price else None,
            }
        except Exception as e:
            print(f"Twilio SMS error: {e}")
            return {
                "status": "failed",
                "error": str(e),
            }

    async def send_sms_batch(self, recipients: list, message: str) -> Dict:
        """
        Send SMS to multiple recipients
        
        Args:
            recipients: List of phone numbers
            message: SMS message content
            
        Returns:
            Dict with sent count, failed count, and details
        """
        results = []
        for phone in recipients:
            result = await self.send_sms(phone, message)
            results.append(result)

        sent = sum(1 for r in results if r["status"] == "sent")
        failed = len(results) - sent

        return {
            "status": "completed",
            "sent": sent,
            "failed": failed,
            "total": len(recipients),
            "details": results,
        }

    async def start_call(
        self,
        to_phone: str,
        twiml_url: Optional[str] = None,
        message: Optional[str] = None,
    ) -> Dict:
        """
        Start an outbound call
        
        Args:
            to_phone: Recipient phone number
            twiml_url: URL to TwiML instructions
            message: Text-to-speech message
            
        Returns:
            Dict with call_id and status
        """
        if not self._initialized:
            return {
                "status": "initiated",
                "call_id": f"mock_call_{to_phone}",
                "to": to_phone,
            }

        try:
            # Create TwiML if message provided
            if message and not twiml_url:
                from twilio.twiml.voice_response import VoiceResponse

                response = VoiceResponse()
                response.say(message, voice="alice")
                twiml_url = f"<Response>{response}</Response>"

            call = self.client.calls.create(
                to=to_phone,
                from_=self.from_number,
                url=twiml_url or "https://demo.twilio.com/docs/voice.xml",
            )

            return {
                "status": "initiated",
                "call_id": call.sid,
                "to": to_phone,
                "duration": 0,
            }
        except Exception as e:
            print(f"Twilio call error: {e}")
            return {
                "status": "failed",
                "error": str(e),
            }

    async def record_call(self, call_sid: str) -> Dict:
        """Check recording status of a call"""
        if not self._initialized:
            return {"status": "no_recording"}

        try:
            call = self.client.calls(call_sid).fetch()
            if call.subresource_uris.get("recordings"):
                recordings = self.client.calls(call_sid).recordings.list()
                return {
                    "status": "recorded",
                    "count": len(recordings),
                    "recordings": [
                        {
                            "sid": r.sid,
                            "duration": r.duration,
                            "uri": r.uri,
                        }
                        for r in recordings
                    ],
                }
            else:
                return {"status": "no_recording"}
        except Exception as e:
            print(f"Twilio recording check error: {e}")
            return {"status": "error"}

    async def send_whatsapp(self, to_phone: str, message: str) -> Dict:
        """
        Send WhatsApp message (requires WhatsApp Business API setup)
        
        Args:
            to_phone: Recipient WhatsApp number
            message: Message content
            
        Returns:
            Dict with status and message_id
        """
        if not self._initialized:
            return {
                "status": "sent",
                "message_id": f"mock_whatsapp_{to_phone}",
            }

        try:
            sms = self.client.messages.create(
                body=message,
                from_=f"whatsapp:{self.from_number}",
                to=f"whatsapp:{to_phone}",
            )

            return {
                "status": "sent",
                "message_id": sms.sid,
            }
        except Exception as e:
            print(f"Twilio WhatsApp error: {e}")
            return {
                "status": "failed",
                "error": str(e),
            }


# Global instance
twilio_service = TwilioIntegration()
