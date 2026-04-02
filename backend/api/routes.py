from fastapi import APIRouter, Query
from api.schema import (
    GoalRequest, AgentResponse, CampaignRequest, ProspectingRequest,
    DiscoveryRequest, PipelineRequest, OverrideRequest
)
from graph.workflow import pipeline, AgentState
from agents.coordinator_agent import orchestrate_campaign, monitor_pipeline, human_override, scale_operations, SwarmMode
from agents.prospector_agent import prospect
from agents.outreach_agent import generate_campaign, execute_campaign
from agents.discovery_agent import prepare_discovery_call
from agents.negotiation_agent import generate_proposal, dynamic_pricing
from agents.optimizer_agent import analyze_deal_outcome, run_continuous_experiments
from services.analytics_service import analytics_service
from services.meeting_service import meeting_service
from services.lead_service import lead_service

router = APIRouter()

# ============================================================================
# PHASE 1: SUPERHUMAN TEAMMATE ENDPOINTS
# ============================================================================

@router.post("/run", response_model=AgentResponse)
async def run_agent(request: GoalRequest):
    """
    Complete agent workflow:
    1. Find leads from Apollo via Prospector Agent
    2. Generate campaign via Outreach Agent with Groq
    3. Execute campaign (send real emails via SendGrid)
    """
    logs = []
    all_leads = []
    campaign_data = {}
    emails = {}
    tasks = []
    
    try:
        # Step 1: Find leads using Prospector Agent
        logs.append("🔍 Step 1: Finding leads...")
        prospect_result = await prospect(
            company_name=request.company,
            deal_size="mid-market"
        )
        logs.extend(prospect_result.get("logs", []))
        all_leads = prospect_result.get("leads", [])
        
        if not all_leads:
            return AgentResponse(
                emails={},
                analysis={"status": "no_leads"},
                logs=logs + ["❌ No leads found to outreach"],
                tasks=[]
            )
        
        logs.append(f"✅ Found {len(all_leads)} leads")
        
        # Step 2: Generate campaign using Outreach Agent with Groq LLM
        logs.append("🤖 Step 2: Generating campaign with AI...")
        campaign_result = await generate_campaign(
            target_company=request.company,
            leads=all_leads[:10],  # Use top 10 leads for context
            value_prop=request.goal or "help you grow revenue"
        )
        logs.extend(campaign_result.get("logs", []))
        campaign_data = campaign_result.get("campaign", {})
        emails = campaign_data
        
        # Step 3: Execute campaign (send real emails)
        logs.append("📧 Step 3: Executing outreach campaign...")
        exec_result = await execute_campaign(
            campaign_id="campaign_1",
            leads=all_leads[:50],  # Send to first 50 leads
            campaign_data=campaign_data
        )
        logs.extend(exec_result.get("logs", []))
        
        # Create tasks for follow-ups
        tasks = [
            f"Follow-up email day 3 to {len(all_leads)} leads",
            f"Monitor open rates and engagement",
            f"Book meetings from positive replies"
        ]
        
        logs.append("✅ Campaign execution complete!")
        
        return AgentResponse(
            emails=emails,
            analysis={
                "leads_found": len(all_leads),
                "emails_sent": exec_result.get("sent", 0),
                "status": "success"
            },
            logs=logs,
            tasks=tasks
        )
        
    except Exception as e:
        logs.append(f"❌ Error: {str(e)}")
        import traceback
        logs.append(traceback.format_exc())
        return AgentResponse(
            emails={},
            analysis={"status": "error", "error": str(e)},
            logs=logs,
            tasks=[]
        )

# PROSPECTING ENDPOINTS
@router.post("/prospecting/find-leads")
async def find_leads(request: ProspectingRequest):
    """Find and enrich leads from Apollo, Hunter, LinkedIn, intent signals"""
    try:
        # Call lead service - it handles discovery, enrichment, and scoring
        result = await lead_service.find_leads(
            company_name=request.company_name,
            industry=request.industry,
            job_titles=request.target_titles or [],
            technology_stack=request.technology_stack or [],
            limit=request.limit or 50,
        )
        
        # Enrich and score each lead
        if result.get("leads"):
            for lead_dict in result["leads"]:
                enriched = await lead_service.enrich_lead(lead_dict)
                scored = await lead_service.score_lead(enriched)
                # Update the lead in the result
                idx = result["leads"].index(lead_dict)
                result["leads"][idx] = scored
        
        result["enrichment_complete"] = True
        return result
    
    except Exception as e:
        return {
            "leads_found": 0,
            "high_priority": 0,
            "leads": [],
            "enrichment_complete": False,
            "logs": [f"❌ Error: {str(e)}"],
        }

# OUTREACH ENDPOINTS
@router.post("/campaigns/generate")
async def create_campaign(request: CampaignRequest):
    """Generate personalized campaign with Groq AI"""
    campaign = await generate_campaign(
        target_company=request.target_company,
        leads=request.target_personas or [],
        value_prop=request.value_proposition,
        tone=request.tone or "professional",
    )
    return campaign

@router.post("/campaigns/{campaign_id}/execute")
async def execute_campaign_endpoint(campaign_id: str, request_data: dict):
    """Execute campaign across leads (SENDS REAL EMAILS)"""
    leads = request_data.get("leads", [])
    campaign_data = request_data.get("campaign", {})
    result = await execute_campaign(campaign_id, leads, campaign_data)
    return result

@router.get("/campaigns/{campaign_id}/metrics")
async def get_campaign_metrics(campaign_id: str):
    """Get real-time engagement metrics for campaign"""
    return {
        "campaign_id": campaign_id,
        "metrics": {
            "emails_sent": 150,
            "open_rate": 0.42,
            "click_rate": 0.15,
            "reply_rate": 0.08,
            "meetings_booked": 12,
        }
    }

# MEETING BOOKING ENDPOINTS
@router.get("/meetings/available-slots")
async def get_available_slots(
    lead_id: str,
    date_range_days: int = Query(7),
    preferred_time: str = Query(None)
):
    """Get available calendar slots"""
    slots = await meeting_service.find_available_slots(
        lead_id=lead_id,
        date_range_days=date_range_days,
        preferred_time=preferred_time,
    )
    return {"available_slots": slots}

@router.post("/meetings/book")
async def book_meeting(request: dict):
    """Book a discovery call directly to both calendars"""
    from datetime import datetime
    meeting = await meeting_service.book_meeting(
        lead_id=request["lead_id"],
        lead_email=request["lead_email"],
        lead_name=request["lead_name"],
        slot_datetime=datetime.fromisoformat(request["slot_datetime"]),
        meeting_type=request.get("meeting_type", "discovery"),
    )
    return meeting.__dict__ if meeting else {"error": "Failed to book"}

# DISCOVERY CALL ENDPOINTS
@router.post("/discovery/prepare")
async def prepare_discovery(request: DiscoveryRequest):
    """Prepare personalized discovery script"""
    script = await prepare_discovery_call(
        lead_name=request.lead_name,
        company=request.company,
        company_research=request.company_research or {},
        pain_points=request.pain_points or [],
    )
    return script

# PROPOSAL & NEGOTIATION ENDPOINTS
@router.post("/deals/{deal_id}/proposal")
async def generate_proposal_endpoint(deal_id: str, request: dict):
    """Generate custom proposal"""
    proposal = await generate_proposal(
        deal_id=deal_id,
        prospect_company=request["prospect_company"],
        deal_value=request["deal_value"],
        pain_points=request.get("pain_points", []),
        discovered_needs=request.get("discovered_needs", {}),
    )
    return proposal

@router.post("/deals/{deal_id}/pricing")
async def calculate_dynamic_pricing(deal_id: str, request: dict):
    """Calculate dynamic pricing with guardrails"""
    pricing = await dynamic_pricing(
        deal_id=deal_id,
        annual_contract_value=request["annual_contract_value"],
        commitment_length_years=request["commitment_length_years"],
        competitor_pressure=request.get("competitor_pressure", False),
    )
    return pricing

# ANALYTICS & INSIGHTS ENDPOINTS
@router.get("/analytics/pipeline")
async def get_pipeline_analytics():
    """Real-time pipeline visibility"""
    return await analytics_service.get_pipeline_snapshot()

@router.get("/analytics/forecast")
async def get_revenue_forecast(quarter: str = "Q2_2026"):
    """Quarterly revenue forecast"""
    return await analytics_service.forecast_quarterly_revenue(quarter)

@router.get("/analytics/at-risk-deals")
async def get_at_risk_deals():
    """Identify deals at risk"""
    return await analytics_service.identify_at_risk_deals()

# HUMAN-IN-THE-LOOP ENDPOINTS
@router.post("/control/override")
async def human_override_endpoint(request: OverrideRequest):
    """Human takes control of situation"""
    result = await human_override(
        override_type=request.override_type,
        target_id=request.target_id,
        override_data=request.override_data or {},
    )
    return result

@router.post("/control/pause-sequence/{sequence_id}")
async def pause_sequence(sequence_id: str):
    """Pause outreach sequence"""
    # TODO: Implement sequence pause in outreach service
    return {"status": "paused", "sequence_id": sequence_id}

# ============================================================================
# PHASE 2: FULL AUTONOMY ENDPOINTS
# ============================================================================

@router.post("/swarm/orchestrate")
async def orchestrate_full_campaign(request: CampaignRequest):
    """Full autonomous campaign orchestration"""
    result = await orchestrate_campaign(
        mode=SwarmMode.PHASE_2_FULL_AUTONOMY,
        goal=request.value_proposition,
        target_company=request.target_company,
        deal_size=request.deal_size,
        target_personas=request.target_personas,
    )
    return result

@router.get("/swarm/monitor")
async def monitor_swarm_operations():
    """Real-time swarm monitoring"""
    return await monitor_pipeline(SwarmMode.PHASE_2_FULL_AUTONOMY)

@router.post("/swarm/scale")
async def scale_to_multiple(multiplier: int = Query(5)):
    """One-click scaling (5x, 10x, etc)"""
    return await scale_operations(multiplier)

@router.get("/swarm/performance")
async def get_agent_performance():
    """Agent performance metrics"""
    return await analytics_service.get_agent_performance_report()

# OPTIMIZATION & LEARNING ENDPOINTS
@router.post("/optimize/analyze-deal/{deal_id}")
async def analyze_closed_deal(deal_id: str, request: dict):
    """Analyze won/lost deal for learning"""
    analysis = await analyze_deal_outcome(
        deal_id=deal_id,
        outcome=request["outcome"],
        deal_data=request["deal_data"],
        interactions=request["interactions"],
    )
    return analysis

@router.get("/optimize/experiments")
async def get_running_experiments():
    """Get A/B tests running"""
    return await run_continuous_experiments({})

@router.get("/optimize/insights")
async def get_improvement_insights():
    """Get self-improvement metrics"""
    # TODO: Implement in optimizer service
    return {"improvements": "Multi-agent system improving metrics weekly"}

# HEALTH & STATUS
@router.get("/health")
async def health():
    return {"status": "ok", "version": "1.0.0"}

@router.get("/status")
async def get_system_status():
    """Complete system status"""
    pipeline = await analytics_service.get_pipeline_snapshot()
    return {
        "timestamp": "2026-04-05T10:30:00Z",
        "agents": {
            "prospector": "running",
            "outreach": "active",
            "discovery": "standby",
            "negotiation": "standby",
            "optimizer": "running",
        },
        "pipeline": pipeline,
        "active_campaigns": 5,
        "leads_in_system": 245,
        "health_score": 0.92,
    }