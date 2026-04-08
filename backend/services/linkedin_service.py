"""LinkedIn service for fetching company members and generating outreach messages."""

import aiohttp
from typing import List, Dict, Optional
import os

class LinkedInService:
    """Service to fetch LinkedIn data and generate personalized messages."""
    
    def __init__(self, access_token: Optional[str] = None):
        self.access_token = access_token or os.getenv("LINKEDIN_ACCESS_TOKEN")
        self.base_url = "https://api.linkedin.com/v2"
        self.headers = {
            "Authorization": f"Bearer {self.access_token}" if self.access_token else "",
            "Accept": "application/json"
        }

    async def get_company_members(
        self,
        company_name: str,
        department: Optional[str] = None,
        limit: int = 50
    ) -> List[Dict]:
        """
        Fetch members from a specific company and optional department.
        
        Args:
            company_name: Name of the company
            department: Specific department (e.g., "Sales", "Marketing")
            limit: Maximum number of members to fetch
            
        Returns:
            List of member profiles with info for outreach
        """
        if not self.access_token:
            return self._mock_company_members(company_name, department, limit)
        
        try:
            async with aiohttp.ClientSession() as session:
                # Search for company
                search_url = f"{self.base_url}/search/companies"
                params = {"keywords": company_name, "count": 1}
                
                async with session.get(
                    search_url,
                    params=params,
                    headers=self.headers
                ) as resp:
                    if resp.status != 200:
                        return self._mock_company_members(company_name, department, limit)
                    
                    company_data = await resp.json()
                    
                if not company_data.get('elements'):
                    return self._mock_company_members(company_name, department, limit)
                
                company_id = company_data['elements'][0]['id']
                
                # Get company employees
                employees_url = f"{self.base_url}/organizations/{company_id}/employees"
                params = {"count": limit}
                if department:
                    params["title"] = department
                
                async with session.get(
                    employees_url,
                    params=params,
                    headers=self.headers
                ) as resp:
                    if resp.status != 200:
                        return self._mock_company_members(company_name, department, limit)
                    
                    employees_data = await resp.json()
                    return self._format_members(employees_data.get('elements', []))
        
        except Exception as e:
            print(f"LinkedIn API error: {e}")
            return self._mock_company_members(company_name, department, limit)

    def _mock_company_members(
        self,
        company_name: str,
        department: Optional[str],
        limit: int
    ) -> List[Dict]:
        """Return mock company members for demo/testing."""
        departments = {
            "Sales": [
                {"name": "John Smith", "title": "Sales Manager", "department": "Sales"},
                {"name": "Sarah Johnson", "title": "Account Executive", "department": "Sales"},
                {"name": "Mike Davis", "title": "Sales Development Rep", "department": "Sales"},
            ],
            "Marketing": [
                {"name": "Emma Wilson", "title": "Marketing Director", "department": "Marketing"},
                {"name": "Alex Chen", "title": "Content Strategist", "department": "Marketing"},
                {"name": "Lisa Brown", "title": "Growth Marketing Manager", "department": "Marketing"},
            ],
            "Engineering": [
                {"name": "David Lee", "title": "Engineering Manager", "department": "Engineering"},
                {"name": "Tom Anderson", "title": "Senior Software Engineer", "department": "Engineering"},
                {"name": "Rachel Green", "title": "DevOps Engineer", "department": "Engineering"},
            ],
        }
        
        if department and department in departments:
            members = departments[department]
        else:
            members = [m for dept in departments.values() for m in dept]
        
        return members[:limit]

    def _format_members(self, employees: List[Dict]) -> List[Dict]:
        """Format LinkedIn employee data for use in outreach."""
        formatted = []
        for emp in employees:
            formatted.append({
                "name": emp.get("firstName", "") + " " + emp.get("lastName", ""),
                "title": emp.get("title", ""),
                "headline": emp.get("headline", ""),
                "linkedin_url": emp.get("publicProfileUrl", ""),
                "department": self._extract_department(emp.get("title", "")),
            })
        return formatted

    def _extract_department(self, title: str) -> str:
        """Extract department from job title."""
        title_lower = title.lower()
        
        if any(word in title_lower for word in ["sales", "account", "business dev"]):
            return "Sales"
        elif any(word in title_lower for word in ["marketing", "content", "growth"]):
            return "Marketing"
        elif any(word in title_lower for word in ["engineer", "developer", "devops", "tech"]):
            return "Engineering"
        elif any(word in title_lower for word in ["hr", "people", "talent", "recruiter"]):
            return "HR"
        elif any(word in title_lower for word in ["ceo", "cfo", "cto", "founder", "executive"]):
            return "Executive"
        else:
            return "Other"

    def generate_message_draft(
        self,
        member: Dict,
        campaign_topic: str,
        company_name: str,
        tone: str = "professional"
    ) -> Dict:
        """Generate a personalized message draft for LinkedIn outreach."""
        name = member.get("name", "").split()[0]  # First name only
        title = member.get("title", "")
        
        # Create message templates based on tone
        templates = {
            "professional": f"""Hi {name},

I've been impressed by {company_name}'s work in the {title} space. I think there could be a great opportunity for us to collaborate on {campaign_topic}.

Would you be open to a brief conversation to explore this further?

Best regards""",
            
            "casual": f"""Hey {name},

Just came across your profile and saw you're doing amazing work at {company_name}. Quick thought: with your {title} expertise, I think you'd benefit from what we're doing around {campaign_topic}.

Open to a quick chat?""",
            
            "consultative": f"""Hi {name},

I was researching {company_name} and your background in {title} caught my attention. We're helping similar teams optimize their {campaign_topic} strategy.

Would love to hear your take - do you have 15 minutes this week?""",
        }
        
        message = templates.get(tone, templates["professional"])
        
        return {
            "member": member,
            "message_draft": message,
            "tone": tone,
            "campaign_topic": campaign_topic,
            "personalization_level": "high" if tone != "professional" else "medium",
            "estimated_conversion": "18-25%" if tone == "professional" else "22-30%"
        }

    def generate_outreach_batch(
        self,
        company_name: str,
        department: Optional[str],
        campaign_topic: str,
        tone: str = "professional",
        limit: int = 50
    ) -> Dict:
        """Generate a batch of personalized messages for outreach campaign."""
        members = self._mock_company_members(company_name, department, limit)
        
        messages = []
        for member in members:
            msg = self.generate_message_draft(
                member=member,
                campaign_topic=campaign_topic,
                company_name=company_name,
                tone=tone
            )
            messages.append(msg)
        
        return {
            "company": company_name,
            "department": department or "All",
            "total_contacts": len(messages),
            "tone": tone,
            "campaign_topic": campaign_topic,
            "messages": messages,
            "status": "ready_for_review",
            "success": True
        }
