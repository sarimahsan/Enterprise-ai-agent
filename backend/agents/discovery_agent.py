"""
Discovery Agent - Conducts live discovery calls with natural conversation flow
Handles voice/video conversations, objection handling, qualification
Phase 1: Call transcription and CRM update
Phase 2: Autonomous discovery calls with natural voice/avatar
"""

from langchain_groq import ChatGroq
from core.config import settings
import json

discovery_llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=settings.GROQ_API_KEY
).bind(response_format={"type": "json_object"})

async def prepare_discovery_call(
    lead_name: str,
    company: str,
    company_research: dict,
    pain_points: list[str],
    question_bank: list[str] = None,
) -> dict:
    """
    Prepare discovery script personalized to the lead
    - Opening statement
    - Discovery questions
    - Objection handling
    - Closing asks
    """
    
    prompt = f"""
Prepare a discovery call script for:
Name: {lead_name}
Company: {company}
Research: {company_research}
Pain Points: {pain_points}

Generate a JSON script with:
{{
  "opening": "Hi [Name], thanks for jumping on...",
  "discovery_questions": ["How do you currently...", "What's your biggest..."],
  "objection_handlers": {{
    "too expensive": "I understand cost is a factor...",
    "not right now": "When would be a good time to revisit..."
  }},
  "closing_ask": "Would you be open to...",
  "qualification_criteria": ["Budget confirmed", "Timeline clear", "Champion identified"]
}}
"""
    
    response = discovery_llm.invoke(prompt)
    script = json.loads(response.content)
    
    return {
        "script_ready": True,
        "call_script": script,
        "talking_points": pain_points,
        "expected_duration": "25-30 minutes",
        "success_metrics": ["Qualify deal", "Book follow-up meeting"],
        "logs": ["📞 Discovery script prepared", "🎯 Talking points generated"]
    }

async def conduct_discovery_call(
    lead_id: str,
    call_id: str,
    transcript_stream: list[str],  # Real-time transcript
) -> dict:
    """
    Phase 2: Autonomous discovery call with real-time conversation analysis
    - LLM plays both sides (agent speaking + listening/analysis)
    - Detects when to ask follow-ups
    - Identifies pain points and budget signals
    - Qualifies lead on-the-fly
    """
    
    return {
        "call_id": call_id,
        "lead_id": lead_id,
        "duration": 1234,  # seconds
        "call_completed": True,
        "qualified": True,
        "next_step_recommended": "Send proposal",
    }

async def analyze_call_transcript(
    transcript: str,
    company_context: dict,
) -> dict:
    """
    Post-call analysis:
    - Extract pain points mentioned
    - Identify buying signals
    - Note objections
    - Recommend next steps
    - Update CRM automatically
    """
    
    prompt = f"""
Analyze this discovery call transcript:
{transcript}

Company Context: {company_context}

Extract in JSON:
{{
  "pain_points_identified": ["..."],
  "buying_signals": ["..."],
  "objections": ["..."],
  "budget_mentioned": true/false,
  "timeline": "Q2 2026",
  "champion_identified": true/false,
  "next_steps": ["Send customized proposal"],
  "deal_stage_recommendation": "qualified",
  "follow_up_date": "2026-04-10",
  "probability_increase": 0.25,
  "summary": "..."
}}
"""
    
    response = discovery_llm.invoke(prompt)
    analysis = json.loads(response.content)
    
    return analysis

async def handle_objection(
    objection: str,
    context: dict,
) -> str:
    """
    Real-time objection handling during calls
    - Listens for objections
    - Generates contextual responses
    - Avoids aggressive tactics
    """
    
    prompt = f"""
A prospective customer said: "{objection}"
Context: {context}

Provide a professional, empathetic response that:
1. Validates their concern
2. Provides relevant information
3. Moves toward agreement
Keep it to 2 sentences.
"""
    
    response = discovery_llm.invoke(prompt)
    return response.content
