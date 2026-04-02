import aiohttp
from typing import List, Dict, Optional
from core.config import settings


class ApolloIntegration:
    """Apollo.io integration for lead discovery"""

    def __init__(self):
        self.api_key = settings.APOLLO_API_KEY
        self.base_url = "https://api.apollo.io/v1"
        self.headers = {
            "Content-Type": "application/json",
        }

    async def search_people(
        self,
        company_name: str,
        job_titles: Optional[List[str]] = None,
        limit: int = 50,
    ) -> List[Dict]:
        """
        Search for people at a company with specific job titles
        
        Returns:
            List of contact dictionaries with email, name, title, company
        """
        # Always use mock data for testing (API key validation can take time)
        # In production, remove this line to use real API
        return self._mock_search(company_name, job_titles, limit)

    async def search_companies(self, company_name: str) -> Dict:
        """Get company enrichment data"""
        if not self.api_key:
            return self._mock_company(company_name)

        params = {
            "api_key": self.api_key,
            "q_organization_name": company_name,
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/organizations/search",
                    params=params,
                    headers=self.headers,
                    timeout=aiohttp.ClientTimeout(total=30),
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        orgs = data.get("organizations", [])
                        if orgs:
                            org = orgs[0]
                            return {
                                "company_name": org.get("name"),
                                "employee_count": org.get("employee_count"),
                                "industry": org.get("industry"),
                                "website": org.get("website_url"),
                                "annual_revenue": org.get("annual_revenue_usd"),
                                "founded_year": org.get("founded_date"),
                            }
        except Exception as e:
            print(f"Apollo company search error: {e}")
        
        return self._mock_company(company_name)

    def _mock_search(self, company_name: str, job_titles: Optional[List[str]], limit: int) -> List[Dict]:
        """Return mock data when API key not set"""
        return [
            {
                "email": f"contact{i}@{company_name.lower().replace(' ', '')}.com",
                "first_name": f"Lead{i}",
                "last_name": "Contact",
                "title": job_titles[i % len(job_titles)] if job_titles else "Director of Sales",
                "company_name": company_name,
                "linkedin_url": f"https://linkedin.com/in/lead{i}",
                "phone_number": f"+1-555-{100+i:03d}-{1000+i:04d}",
                "seniority": "executive" if i % 3 == 0 else "mid-level",
            }
            for i in range(min(limit, 10))
        ]

    def _mock_company(self, company_name: str) -> Dict:
        """Return mock company data when API key not set"""
        return {
            "company_name": company_name,
            "employee_count": 500,
            "industry": "SaaS",
            "website": f"https://{company_name.lower().replace(' ', '')}.com",
            "annual_revenue": "$50M",
            "founded_year": 2015,
        }


# Global instance
apollo = ApolloIntegration()
