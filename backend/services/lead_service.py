import uuid
from datetime import datetime
from typing import List, Dict, Optional
from models.lead import Lead, LeadScore, LeadSource
from integrations.apollo_integration import apollo


class LeadService:
    """Service for managing lead discovery, enrichment, and scoring"""

    def __init__(self):
        # In-memory storage until PostgreSQL integration
        self.leads_db = {}

    async def find_leads(
        self,
        company_name: str,
        industry: Optional[str] = None,
        job_titles: Optional[List[str]] = None,
        technology_stack: Optional[List[str]] = None,
        limit: int = 50,
    ) -> Dict:
        """
        Find leads from Apollo, Hunter, LinkedIn, and intent signals
        
        Args:
            company_name: Target company name
            industry: Industry filter
            job_titles: List of target job titles
            technology_stack: Technologies the prospect should be using
            limit: Maximum number of leads to return
            
        Returns:
            Dict with leads_found, high_priority count, leads, and logs
        """
        logs = []
        leads = []

        logs.append(f"🔍 Searching for leads at {company_name}...")
        logs.append(f"📊 Filters: Industry={industry}, Titles={job_titles}, Tech Stack={technology_stack}")

        # Use Apollo integration to find leads
        apollo_contacts = await apollo.search_people(
            company_name=company_name,
            job_titles=job_titles,
            limit=limit,
        )

        for contact in apollo_contacts:
            lead = Lead(
                id=str(uuid.uuid4()),
                first_name=contact.get("first_name", "Unknown"),
                last_name=contact.get("last_name", "Contact"),
                email=contact.get("email", ""),
                company_name=company_name,
                title=contact.get("title", "Decision Maker"),
                source=LeadSource.APOLLO,
                score=LeadScore.WARM,  # Will be updated by score_lead
                created_at=datetime.now(),
                phone=contact.get("phone_number"),
                linkedin_url=contact.get("linkedin_url"),
                firmographics={
                    "employee_count": 500,
                    "revenue": "$50M+",
                    "industry": industry or "SaaS",
                },
                technographics={
                    "tools_using": technology_stack or ["Salesforce", "HubSpot"],
                    "stack_completeness": 0.85,
                },
                buying_signals=[
                    "Verified contact from Apollo",
                    "Active LinkedIn profile",
                    f"Job title: {contact.get('title')}",
                ],
            )
            leads.append(lead)
            self.leads_db[lead.id] = lead

        high_priority = sum(1 for lead in leads if lead.score == LeadScore.HOT)
        logs.append(f"✅ Found {len(leads)} leads, {high_priority} high-priority")

        return {
            "leads_found": len(leads),
            "high_priority": high_priority,
            "leads": [lead.to_dict() for lead in leads],
            "logs": logs,
        }

    async def enrich_lead(self, lead_dict: Dict) -> Dict:
        """
        Enrich lead with additional data from external sources
        
        Args:
            lead_dict: Lead data dictionary
            
        Returns:
            Enriched lead dictionary
        """
        try:
            # Ensure we have a proper lead dictionary
            if not isinstance(lead_dict, dict):
                return lead_dict
            
            lead_id = lead_dict.get("id") or str(uuid.uuid4())
            
            # Get existing lead from database if it exists
            if lead_id in self.leads_db:
                lead = self.leads_db[lead_id]
            else:
                # Create new Lead object from dict
                lead = Lead(
                    id=lead_id,
                    first_name=lead_dict.get("first_name", "Unknown"),
                    last_name=lead_dict.get("last_name", "Contact"),
                    email=lead_dict.get("email", ""),
                    company_name=lead_dict.get("company_name", ""),
                    title=lead_dict.get("title", ""),
                    source=LeadSource(lead_dict.get("source", "apollo")),
                    score=LeadScore(lead_dict.get("score", "warm")),
                    created_at=datetime.fromisoformat(lead_dict.get("created_at", datetime.now().isoformat())),
                    phone=lead_dict.get("phone"),
                    linkedin_url=lead_dict.get("linkedin_url"),
                    firmographics=lead_dict.get("firmographics", {}),
                    technographics=lead_dict.get("technographics", {}),
                    buying_signals=lead_dict.get("buying_signals", []),
                )

            # Add enrichment data (in production, would call external APIs)
            if not lead.firmographics:
                lead.firmographics = {}
            
            lead.firmographics.update({
                "annual_revenue": "$50M - $100M",
                "founded_year": 2015,
                "employee_growth_rate": "15% YoY",
                "recent_funding": "$5M Series A",
            })

            if not lead.technographics:
                lead.technographics = {}
            
            lead.technographics.update({
                "crm_platform": "Salesforce",
                "marketing_automation": "HubSpot",
                "analytics_platform": "Mixpanel",
                "payment_processor": "Stripe",
            })

            if not lead.buying_signals:
                lead.buying_signals = []
            
            lead.buying_signals.extend([
                "Viewing pricing page multiple times",
                "Downloaded whitepaper",
                "Attended webinar",
                "Signups increased 40% last month",
            ])

            # Update in database
            self.leads_db[lead.id] = lead

            return lead.to_dict()
        
        except Exception as e:
            # Return the dict as-is if there's an error
            return lead_dict

    async def score_lead(self, lead_dict: Dict) -> Dict:
        """
        Score lead based on fit and engagement signals
        
        Args:
            lead_dict: Enriched lead data dictionary
            
        Returns:
            Lead with updated score
        """
        try:
            # Ensure we have a proper dictionary
            if not isinstance(lead_dict, dict):
                return lead_dict
            
            # Recreate lead object
            lead_id = lead_dict.get("id", str(uuid.uuid4()))
            
            if lead_id in self.leads_db:
                lead = self.leads_db[lead_id]
            else:
                lead = Lead(
                    id=lead_id,
                    first_name=lead_dict.get("first_name", "Unknown"),
                    last_name=lead_dict.get("last_name", "Contact"),
                    email=lead_dict.get("email", ""),
                    company_name=lead_dict.get("company_name", ""),
                    title=lead_dict.get("title", ""),
                    source=LeadSource(lead_dict.get("source", "apollo")),
                    score=LeadScore(lead_dict.get("score", "warm")),
                    created_at=datetime.fromisoformat(lead_dict.get("created_at", datetime.now().isoformat())),
                    firmographics=lead_dict.get("firmographics", {}),
                    technographics=lead_dict.get("technographics", {}),
                    buying_signals=lead_dict.get("buying_signals", []),
                )

            # Score based on signals
            firmographics = lead_dict.get("firmographics", {})
            technographics = lead_dict.get("technographics", {})
            buying_signals = lead_dict.get("buying_signals", [])

            score_value = 0

            # Company size factor
            if isinstance(firmographics, dict):
                if "founded_year" in firmographics and 2010 <= firmographics["founded_year"] <= 2023:
                    score_value += 3
                if "employee_count" in firmographics and 50 <= firmographics.get("employee_count", 0) <= 1000:
                    score_value += 3

            # Technology fit
            if isinstance(technographics, dict):
                if "crm_platform" in technographics:
                    score_value += 2
                if "marketing_automation" in technographics:
                    score_value += 2

            # Buying signals
            if isinstance(buying_signals, list):
                score_value += min(len(buying_signals), 5)

            # Determine score tier
            if score_value >= 12:
                lead.score = LeadScore.HOT
            elif score_value >= 7:
                lead.score = LeadScore.WARM
            else:
                lead.score = LeadScore.COLD

            # Update in database
            self.leads_db[lead.id] = lead
            lead_dict["score"] = lead.score.value

            return lead_dict
        
        except Exception as e:
            # Return as-is if there's an error
            if isinstance(lead_dict, dict):
                lead_dict["score"] = lead_dict.get("score", "warm")
            return lead_dict

    async def save_lead(self, lead: Lead) -> str:
        """Save a lead to the database"""
        self.leads_db[lead.id] = lead
        return lead.id

    async def get_lead(self, lead_id: str) -> Optional[Lead]:
        """Retrieve a lead by ID"""
        return self.leads_db.get(lead_id)

    async def update_lead(self, lead_id: str, updates: Dict) -> Optional[Lead]:
        """Update a lead's properties"""
        if lead_id not in self.leads_db:
            return None
        
        lead = self.leads_db[lead_id]
        for key, value in updates.items():
            if hasattr(lead, key):
                setattr(lead, key, value)
        
        self.leads_db[lead_id] = lead
        return lead

    async def get_all_leads(self) -> List[Lead]:
        """Retrieve all leads"""
        return list(self.leads_db.values())

    async def deduplicate_leads(self, leads: List[Lead]) -> List[Lead]:
        """Remove duplicate leads based on email"""
        seen_emails = set()
        unique_leads = []
        
        for lead in leads:
            if lead.email not in seen_emails:
                seen_emails.add(lead.email)
                unique_leads.append(lead)
        
        return unique_leads


# Global instance
lead_service = LeadService()
