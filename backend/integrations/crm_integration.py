import aiohttp
from typing import Dict, Optional, List
from core.config import settings


class CRMIntegration:
    """Integration with CRM systems (Salesforce, HubSpot)"""

    def __init__(self):
        self.hubspot_key = settings.HUBSPOT_API_KEY
        self.salesforce_id = settings.SALESFORCE_CLIENT_ID
        self.salesforce_secret = settings.SALESFORCE_CLIENT_SECRET
        self.salesforce_url = settings.SALESFORCE_INSTANCE_URL

    async def create_contact(
        self,
        email: str,
        first_name: str,
        last_name: str,
        company: str,
        phone: Optional[str] = None,
        properties: Optional[Dict] = None,
    ) -> Dict:
        """Create a new contact in HubSpot"""
        if not self.hubspot_key:
            return {
                "status": "created",
                "contact_id": f"mock_{email}",
            }

        try:
            headers = {
                "Authorization": f"Bearer {self.hubspot_key}",
                "Content-Type": "application/json",
            }

            payload = {
                "properties": {
                    "firstname": first_name,
                    "lastname": last_name,
                    "email": email,
                    "company": company,
                    "phone": phone or "",
                    **(properties or {}),
                }
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "https://api.hubapi.com/crm/v3/objects/contacts",
                    json=payload,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=30),
                ) as response:
                    if response.status in [200, 201]:
                        data = await response.json()
                        return {
                            "status": "created",
                            "contact_id": data.get("id"),
                            "crm": "hubspot",
                        }
        except Exception as e:
            print(f"HubSpot contact creation error: {e}")

        return {
            "status": "error",
            "message": "Failed to create contact",
        }

    async def create_deal(
        self,
        deal_name: str,
        amount: float,
        contact_id: str,
        stage: str = "negotiation",
        properties: Optional[Dict] = None,
    ) -> Dict:
        """Create a deal in HubSpot"""
        if not self.hubspot_key:
            return {
                "status": "created",
                "deal_id": f"mock_deal_{contact_id}",
            }

        try:
            headers = {
                "Authorization": f"Bearer {self.hubspot_key}",
                "Content-Type": "application/json",
            }

            payload = {
                "properties": {
                    "dealname": deal_name,
                    "amount": str(amount),
                    "dealstage": stage,
                    **(properties or {}),
                }
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "https://api.hubapi.com/crm/v3/objects/deals",
                    json=payload,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=30),
                ) as response:
                    if response.status in [200, 201]:
                        data = await response.json()
                        return {
                            "status": "created",
                            "deal_id": data.get("id"),
                            "crm": "hubspot",
                        }
        except Exception as e:
            print(f"HubSpot deal creation error: {e}")

        return {
            "status": "error",
            "message": "Failed to create deal",
        }

    async def update_contact(
        self,
        contact_id: str,
        properties: Dict,
    ) -> Dict:
        """Update a contact in HubSpot"""
        if not self.hubspot_key:
            return {
                "status": "updated",
                "contact_id": contact_id,
            }

        try:
            headers = {
                "Authorization": f"Bearer {self.hubspot_key}",
                "Content-Type": "application/json",
            }

            payload = {"properties": properties}

            async with aiohttp.ClientSession() as session:
                async with session.patch(
                    f"https://api.hubapi.com/crm/v3/objects/contacts/{contact_id}",
                    json=payload,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=30),
                ) as response:
                    if response.status in [200, 201]:
                        return {
                            "status": "updated",
                            "contact_id": contact_id,
                        }
        except Exception as e:
            print(f"HubSpot contact update error: {e}")

        return {
            "status": "error",
            "message": "Failed to update contact",
        }

    async def get_contact(self, contact_id: str) -> Dict:
        """Get contact details from HubSpot"""
        if not self.hubspot_key:
            return {
                "id": contact_id,
                "properties": {},
            }

        try:
            headers = {
                "Authorization": f"Bearer {self.hubspot_key}",
            }

            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"https://api.hubapi.com/crm/v3/objects/contacts/{contact_id}",
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=30),
                ) as response:
                    if response.status == 200:
                        return await response.json()
        except Exception as e:
            print(f"HubSpot contact fetch error: {e}")

        return {
            "id": contact_id,
            "properties": {},
        }

    async def sync_to_crm(self, lead_data: Dict) -> Dict:
        """Sync lead data to CRM"""
        result = await self.create_contact(
            email=lead_data.get("email"),
            first_name=lead_data.get("first_name"),
            last_name=lead_data.get("last_name"),
            company=lead_data.get("company"),
            phone=lead_data.get("phone"),
            properties={
                "lifecyclestage": "lead",
                "leadscore": lead_data.get("score", "warm"),
                "source": "flowforge",
            },
        )
        return result


# Global instance
crm_service = CRMIntegration()
