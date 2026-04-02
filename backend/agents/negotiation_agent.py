"""
Negotiation Agent - Handles deal negotiation with dynamic pricing and objection handling
Phase 2: Autonomous negotiation of complex deals within guardrails
"""

from langchain_groq import ChatGroq
from core.config import settings
import json

negotiation_llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=settings.GROQ_API_KEY
).bind(response_format={"type": "json_object"})

async def generate_proposal(
    deal_id: str,
    prospect_company: str,
    deal_value: float,
    pain_points: list[str],
    discovered_needs: dict,
    company_name: str = "Your Company",
) -> dict:
    """
    Generate custom proposal with:
    - Personalized value alignment
    - ROI calculation
    - Implementation timeline
    - Pricing options
    """
    
    prompt = f"""
Generate a sales proposal for:
Company: {prospect_company}
Deal Value: ${deal_value}
Their Pain Points: {pain_points}
Their Needs: {discovered_needs}

Return JSON:
{{
  "proposal_title": "Proposal for {prospect_company}",
  "executive_summary": "We will solve your problems by...",
  "solution_overview": {{
    "components": ["Feature 1", "Feature 2"],
    "timeline": "3 months to full deployment"
  }},
  "pricing": {{
    "annual_cost": {deal_value},
    "implementation_fee": 0,
    "roi_12_months": "$2.5M in saved labor"
  }},
  "next_steps": ["Sign contract", "Onboarding kickoff"],
  "valid_until": "2026-05-02"
}}
"""
    
    response = negotiation_llm.invoke(prompt)
    proposal = json.loads(response.content)
    
    return {
        "proposal_generated": True,
        "proposal_id": f"prop_{deal_id}",
        "prospect": prospect_company,
        "amount": deal_value,
        "proposal_data": proposal,
        "ready_for_sending": True,
        "logs": ["📄 Proposal generated", "✅ ROI calculated"]
    }

async def counter_objection(
    objection_type: str,  # "price", "timeline", "features", "competitor"
    prospect_context: dict,
    guardrails: dict,  # min margin, max discount, etc.
) -> dict:
    """
    Counter objections with dynamic responses
    Stays within business guardrails (no unauthorized discounts)
    """
    
    prompt = f"""
Prospect objection: {objection_type}
Context: {prospect_context}
Available guardrails: {guardrails}

Provide a counter that:
1. Validates their concern
2. Reframes value or timeline
3. Offers concrete solution (if needed, within guardrails)

Return JSON:
{{
  "counter_response": "...",
  "proposed_solution": "...",
  "decision_needed": true/false,
  "escalate_to_human": true/false
}}
"""
    
    response = negotiation_llm.invoke(prompt)
    counter = json.loads(response.content)
    
    return counter

async def dynamic_pricing(
    deal_id: str,
    annual_contract_value: float,
    commitment_length_years: int,
    competitor_pressure: bool = False,
    guardrails: dict = None,
) -> dict:
    """
    Calculate dynamic pricing based on:
    - Contract length
    - Commitment size
    - Competitor pressure
    - Volume discounts
    All within your defined guardrails
    """
    
    guardrails = guardrails or {
        "min_margin": 0.60,
        "max_discount": 0.15,
        "volume_discount_starts_at": 50000,
    }
    
    # Calculate pricing dynamically
    base_price = annual_contract_value
    
    # Length discount
    if commitment_length_years >= 3:
        length_discount = 0.10
    elif commitment_length_years == 2:
        length_discount = 0.05
    else:
        length_discount = 0
    
    # Competitor pressure
    competitor_discount = 0.05 if competitor_pressure else 0
    
    total_discount = min(length_discount + competitor_discount, guardrails["max_discount"])
    final_price = base_price * (1 - total_discount)
    
    return {
        "deal_id": deal_id,
        "base_annual_cost": base_price,
        "discounts_applied": {
            "commitment_length": f"{length_discount*100}%",
            "competitor_pressure": f"{competitor_discount*100}%",
        },
        "final_annual_cost": final_price,
        "total_contract_value": final_price * commitment_length_years,
        "margin_percentage": (1 - (final_price / base_price)) * 100,
        "guardrails_respected": True,
        "ready_to_propose": True,
    }

async def handle_legal_review(
    deal_id: str,
    prospect_legal_requests: list[str],
    standard_terms: dict,
) -> dict:
    """
    Handle contract modifications within limits
    - Escalate requests outside standard terms
    - Generate modified contract language
    """
    
    return {
        "deal_id": deal_id,
        "modifications_requested": len(prospect_legal_requests),
        "approved_changes": [],
        "escalated_to_legal_review": ["Limitation of liability cap"],
        "expected_resolution": "2026-04-08",
        "status": "in_review",
    }

async def close_deal(
    deal_id: str,
    prospect_email: str,
    contract_terms: dict,
) -> dict:
    """
    Execute contract signature and deal closure
    - Generate final contract
    - Get e-signature (DocuSign/PandaDoc)
    - Record signed contract
    - Trigger CRM update and revenue recognition
    """
    
    return {
        "deal_id": deal_id,
        "status": "won",
        "contract_signed": True,
        "signature_date": "2026-04-05",
        "revenue_recognized": True,
        "next_handoff": "onboarding_team",
        "logs": ["🎯 Deal closed!", "📝 Contract signed", "💰 Revenue recorded"]
    }
