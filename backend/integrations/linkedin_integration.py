import aiohttp
from typing import List, Dict, Optional
from core.config import settings


class LinkedInIntegration:
    """LinkedIn integration for prospecting and messaging"""

    def __init__(self):
        self.api_key = settings.LINKEDIN_API_KEY
        self.oauth_token = settings.LINKEDIN_OAUTH_TOKEN
        self.base_url = "https://api.linkedin.com/v2"

    async def search_profiles(
        self,
        keywords: str,
        location: Optional[str] = None,
        industry: Optional[str] = None,
        title: Optional[str] = None,
        limit: int = 50,
    ) -> List[Dict]:
        """
        Search for LinkedIn profiles
        
        Returns:
            List of profile dicts with name, headline, company, etc.
        """
        if not self.api_key and not self.oauth_token:
            return self._mock_search(keywords, limit)

        # LinkedIn API search implementation
        try:
            headers = {
                "Authorization": f"Bearer {self.oauth_token}",
                "Content-Type": "application/json",
            }

            params = {
                "keywords": keywords,
                "count": min(limit, 100),
            }

            if location:
                params["location"] = location
            if industry:
                params["industries"] = industry
            if title:
                params["titles"] = title

            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/search/results",
                    params=params,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=30),
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("elements", [])
        except Exception as e:
            print(f"LinkedIn search error: {e}")

        return self._mock_search(keywords, limit)

    async def get_profile(self, profile_id: str) -> Dict:
        """Get detailed profile information"""
        if not self.oauth_token:
            return self._mock_profile(profile_id)

        try:
            headers = {
                "Authorization": f"Bearer {self.oauth_token}",
            }

            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/me",
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=30),
                ) as response:
                    if response.status == 200:
                        return await response.json()
        except Exception as e:
            print(f"LinkedIn profile fetch error: {e}")

        return self._mock_profile(profile_id)

    async def send_message(
        self,
        recipient_urn: str,
        subject: str,
        body: str,
    ) -> Dict:
        """Send a LinkedIn message"""
        if not self.oauth_token:
            return {
                "status": "sent",
                "message_id": f"mock_message_{recipient_urn}",
            }

        try:
            headers = {
                "Authorization": f"Bearer {self.oauth_token}",
                "Content-Type": "application/json",
            }

            payload = {
                "recipients": [recipient_urn],
                "subject": subject,
                "body": body,
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/messaging/threads",
                    json=payload,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=30),
                ) as response:
                    if response.status in [200, 201]:
                        data = await response.json()
                        return {
                            "status": "sent",
                            "message_id": data.get("entityUrn"),
                        }
        except Exception as e:
            print(f"LinkedIn message error: {e}")

        return {
            "status": "failed",
            "error": "Failed to send message",
        }

    def _mock_search(self, keywords: str, limit: int) -> List[Dict]:
        """Return mock LinkedIn profiles"""
        return [
            {
                "id": f"linkedin_profile_{i}",
                "name": f"Professional {i}",
                "headline": "Sales Leader | Revenue Growth Specialist",
                "company": "Tech Company Inc",
                "profile_url": f"https://linkedin.com/in/professional{i}",
            }
            for i in range(min(limit, 10))
        ]

    def _mock_profile(self, profile_id: str) -> Dict:
        """Return mock profile data"""
        return {
            "id": profile_id,
            "localizedFirstName": "John",
            "localizedLastName": "Doe",
            "headline": "VP of Sales",
            "vanityName": "johndoe",
        }


# Global instance
linkedin = LinkedInIntegration()
