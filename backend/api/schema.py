from pydantic import BaseModel
from typing import List, Dict, Optional

# Original Schemas
class GoalRequest(BaseModel):
    company: str
    goal: str

class AgentResponse(BaseModel):
    emails: Dict
    analysis: Dict
    logs: List[str]
    tasks: List[str]

# ============================================================================
# PHASE 1: NEW SCHEMAS
# ============================================================================

# Prospecting Schemas
class ProspectingRequest(BaseModel):
    company_name: str
    industry: Optional[str] = None
    target_titles: Optional[List[str]] = None
    technology_stack: Optional[List[str]] = None
    growth_signals: Optional[List[str]] = None
    limit: Optional[int] = 50

class Lead(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: str
    company_name: str
    title: str
    source: str
    score: str
    buying_signals: List[str]
    firmographics: Dict
    technographics: Dict

class ProspectingResponse(BaseModel):
    leads_found: int
    high_priority: int
    leads: List[Lead]
    enrichment_complete: bool
    logs: List[str]

# Campaign Schemas
class CampaignRequest(BaseModel):
    target_company: str
    value_proposition: str
    target_personas: Optional[List[str]] = None
    tone: Optional[str] = "professional"
    deal_size: Optional[float] = None
    channels: Optional[List[str]] = ["email", "sms"]

class CampaignResponse(BaseModel):
    campaign: Dict
    channels: List[str]
    messages_ready: int
    personalization_level: str
    logs: List[str]

# Meeting Booking Schemas
class MeetingSlotRequest(BaseModel):
    lead_id: str
    date_range_days: int = 7
    preferred_time: Optional[str] = None

class MeetingSlot(BaseModel):
    date: str
    time: str
    duration: int

class MeetingResponse(BaseModel):
    available_slots: List[MeetingSlot]

class BookMeetingRequest(BaseModel):
    lead_id: str
    lead_email: str
    lead_name: str
    slot_datetime: str
    meeting_type: Optional[str] = "discovery"

# Discovery Schemas
class DiscoveryRequest(BaseModel):
    lead_name: str
    company: str
    company_research: Optional[Dict] = None
    pain_points: Optional[List[str]] = None

class DiscoveryResponse(BaseModel):
    script_ready: bool
    call_script: Dict
    talking_points: List[str]
    expected_duration: str
    success_metrics: List[str]

# Proposal Schemas
class ProposalRequest(BaseModel):
    prospect_company: str
    deal_value: float
    pain_points: Optional[List[str]] = None
    discovered_needs: Optional[Dict] = None

class ProposalResponse(BaseModel):
    proposal_generated: bool
    proposal_id: str
    prospect: str
    amount: float
    proposal_data: Dict

# Pricing Schemas
class PricingRequest(BaseModel):
    annual_contract_value: float
    commitment_length_years: int
    competitor_pressure: Optional[bool] = False

class PricingResponse(BaseModel):
    deal_id: str
    base_annual_cost: float
    discounts_applied: Dict
    final_annual_cost: float
    total_contract_value: float
    margin_percentage: float
    guardrails_respected: bool

# Pipeline Schemas
class PipelineRequest(BaseModel):
    quarter: Optional[str] = "Q2_2026"

class PipelineResponse(BaseModel):
    total_pipeline: float
    by_stage: Dict
    weighted_forecast: float
    closing_this_month: float
    at_risk_alerts: int

# Override Schemas
class OverrideRequest(BaseModel):
    override_type: str  # take_call, approve_discount, change_offer, pause_sequence
    target_id: str
    override_data: Optional[Dict] = None

class OverrideResponse(BaseModel):
    override_type: str
    target_id: str
    status: str
    autonomy_temporarily_suspended: bool
    human_took_control: bool

# ============================================================================
# PHASE 2: SWARM & OPTIMIZATION SCHEMAS
# ============================================================================

class SwarmOrchestrationRequest(BaseModel):
    goal: str
    target_company: str
    deal_size: Optional[float] = None
    target_personas: Optional[List[str]] = None

class SwarmStatus(BaseModel):
    timestamp: str
    agents: Dict
    pipeline: Dict
    active_campaigns: int
    leads_in_system: int
    health_score: float

class ScalingRequest(BaseModel):
    multiplier: int  # 5, 10, 50, etc

class ScalingResponse(BaseModel):
    scaling_factor: str
    agents_deployed: Dict
    monthly_lead_capacity: int
    expected_deals_closed: int
    infrastructure_cost_increase: str
    expected_revenue_increase: str
    net_profit_increase: str

class DealAnalysisRequest(BaseModel):
    outcome: str  # won or lost
    deal_data: Dict
    interactions: List[Dict]

class DealAnalysisResponse(BaseModel):
    deal_id: str
    analysis: Dict
    insights_stored: bool
    models_updated: bool

class PerformanceReport(BaseModel):
    deals_closed_this_month: int
    avg_deal_size: float
    win_rate: float
    cost_per_deal: float
    revenue_this_month: float
    human_team_cost: float
    net_profit: float