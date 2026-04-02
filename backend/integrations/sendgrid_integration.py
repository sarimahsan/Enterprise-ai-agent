import aiohttp
import base64
from typing import Dict, Optional
from core.config import settings


class SendGridIntegration:
    """SendGrid integration for email campaigns"""

    def __init__(self):
        self.api_key = settings.SENDGRID_API_KEY
        self.from_email = settings.SENDGRID_FROM_EMAIL or "noreply@flowforge.ai"
        self.base_url = "https://api.sendgrid.com/v3"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    async def send_email(
        self,
        to_email: str,
        subject: str,
        body: str = None,
        body_text: str = None,
        body_html: Optional[str] = None,
        to_name: str = "Recipient",
        from_name: str = "Flowforge",
        tracking_enabled: bool = True,
    ) -> bool:
        """
        Send a single email via SendGrid
        
        Returns:
            bool - True if sent, False if failed
        """
        # Support both 'body' and 'body_text' parameters
        text_body = body_text or body or ""
        
        if not self.api_key:
            # Mock email sending when no API key
            return True

        payload = {
            "personalizations": [
                {
                    "to": [{"email": to_email, "name": to_name}],
                    "subject": subject,
                }
            ],
            "from": {"email": self.from_email, "name": from_name},
            "content": [
                {"type": "text/plain", "value": text_body},
            ],
        }

        if body_html:
            payload["content"].append({"type": "text/html", "value": body_html})

        # Add tracking if enabled
        if tracking_enabled:
            payload["tracking_settings"] = {
                "open": {"enable": True},
                "click": {"enable": True},
            }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/mail/send",
                    json=payload,
                    headers=self.headers,
                    timeout=aiohttp.ClientTimeout(total=30),
                ) as response:
                    return response.status == 202
        except Exception as e:
            print(f"SendGrid error: {e}")
            return False

    async def send_batch(self, emails: list) -> Dict:
        """
        Send multiple emails in a batch
        
        Args:
            emails: List of dicts with to, subject, body_text, body_html
            
        Returns:
            Dict with sent, failed counts and batch_id
        """
        if not self.api_key:
            return {
                "status": "sent",
                "batch_id": "mock_batch",
                "sent": len(emails),
                "failed": 0,
            }

        results = []
        for email in emails:
            result = await self.send_email(
                to_email=email["to"],
                to_name=email.get("name", "Recipient"),
                subject=email["subject"],
                body_text=email["body_text"],
                body_html=email.get("body_html"),
            )
            results.append(result)

        sent = sum(1 for r in results if r["status"] == "sent")
        failed = len(results) - sent

        return {
            "status": "completed",
            "batch_id": f"batch_{sent}_{failed}",
            "sent": sent,
            "failed": failed,
            "details": results,
        }

    async def add_to_contact_list(self, email: str, name: str, list_id: str = "") -> Dict:
        """Add an email to a SendGrid contact list"""
        if not self.api_key:
            return {"status": "added", "contact_id": f"mock_{email}"}

        payload = {
            "contacts": [
                {
                    "email": email,
                    "first_name": name.split()[0] if name else "Contact",
                }
            ]
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.put(
                    f"{self.base_url}/marketing/contacts",
                    json=payload,
                    headers=self.headers,
                    timeout=aiohttp.ClientTimeout(total=30),
                ) as response:
                    if response.status == 202:
                        data = await response.json()
                        return {
                            "status": "added",
                            "contact_id": data.get("job_id", ""),
                        }
        except Exception as e:
            print(f"SendGrid contact list error: {e}")
        
        return {"status": "error", "message": "Failed to add contact"}

    async def get_stats(self) -> Dict:
        """Get email campaign statistics"""
        if not self.api_key:
            return {
                "messages_sent": 0,
                "opens": 0,
                "clicks": 0,
                "bounces": 0,
            }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/stats?limit=1",
                    headers=self.headers,
                    timeout=aiohttp.ClientTimeout(total=30),
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data[0] if data else {}
        except Exception as e:
            print(f"SendGrid stats error: {e}")
        
        return {}


# Global instance
sendgrid_service = SendGridIntegration()
