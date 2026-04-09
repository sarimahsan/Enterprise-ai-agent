from typing import TypedDict, List
from agents.orchestrator import orchestrate
from agents.research_agent import research_company
from agents.analytics_agent import analyze
from agents.writer_Agent import write_outreach
from agents.variant_agent import generate_variants


class AgentState(TypedDict):
    company: str
    goal: str
    tasks: List[str]
    research: dict
    analysis: dict
    emails: dict
    email_templates: dict
    variants: dict
    logs: List[str]
    analytics: dict
    follow_up_schedule: dict


def orchestrator_node(state: AgentState) -> AgentState:
    try:
        tasks = orchestrate(f"Outreach campaign for {state['company']}: {state['goal']}")
    except Exception as e:
        error_msg = f"Orchestrator failed: {str(e)}"
        print(f"❌ {error_msg}")
        return {**state, "logs": state["logs"] + [f"❌ {error_msg}"]}
    return {
        **state,
        "tasks": tasks,
        "logs": state["logs"] + [f"🧠 Orchestrator: Planning outreach for {state['company']}"]
    }


def research_node(state: AgentState) -> AgentState:
    try:
        result = research_company(state["company"], state["goal"])
    except Exception as e:
        error_msg = f"Research failed: {str(e)}"
        print(f"❌ {error_msg}")
        result = {"news": "", "about": "", "goal_context": ""}
        return {**state, "research": result, "logs": state["logs"] + [f"❌ {error_msg} - Using fallback data"]}
    return {
        **state,
        "research": result,
        "logs": state["logs"] + [f"🔍 Research Agent: Found data for {state['company']}"]
    }


def analyst_node(state: AgentState) -> AgentState:
    try:
        result = analyze(state["company"], state["goal"], state["research"])
    except Exception as e:
        error_msg = f"Analysis failed: {str(e)}"
        print(f"❌ {error_msg}")
        result = {"opportunity": "Unknown", "industry": "Unknown", "urgency": "medium"}
        return {**state, "analysis": result, "logs": state["logs"] + [f"❌ {error_msg} - Using defaults"]}
    return {
        **state,
        "analysis": result,
        "logs": state["logs"] + [f"📊 Analyst Agent: Identified opportunity — {result.get('opportunity', '')}"]
    }


def writer_node(state: AgentState) -> AgentState:
    try:
        result = write_outreach(state["company"], state["goal"], state["analysis"])
    except Exception as e:
        error_msg = f"Writer failed: {str(e)}"
        print(f"❌ {error_msg}")
        result = {
            "subject": "Partnership Opportunity",
            "body": "We'd like to discuss a potential partnership.",
            "type": "default"
        }
        return {**state, "emails": result, "logs": state["logs"] + [f"❌ {error_msg} - Using template"]}
    return {
        **state,
        "emails": result,
        "logs": state["logs"] + ["✍️ Writer Agent: 3-email sequence ready ✅"]
    }


def variant_node(state: AgentState) -> AgentState:
    try:
        result = generate_variants(state["company"], state["analysis"])
    except Exception as e:
        error_msg = f"Variant generation failed: {str(e)}"
        print(f"❌ {error_msg}")
        result = []
        return {**state, "variants": result, "logs": state["logs"] + [f"❌ {error_msg} - Skipping variants"]}
    return {
        **state,
        "variants": result,
        "logs": state["logs"] + ["🎯 Variant Agent: A/B testing & multi-channel ready ✅"]
    }


def analytics_node(state: AgentState) -> AgentState:
    """Generate mock analytics for dashboard"""
    try:
        analytics = {
            "campaigns_sent": 0,
            "total_emails": 3,
            "open_rate": 0,
            "response_rate": 0,
            "channels": ["Email", "LinkedIn", "SMS"],
            "estimated_reach": 12,
            "optimization_score": 85,
            "best_channel": "Email",
            "peak_send_time": "Tuesday 10:00 AM"
        }
    except Exception as e:
        error_msg = f"Analytics failed: {str(e)}"
        print(f"❌ {error_msg}")
        analytics = {}
        return {**state, "analytics": analytics, "logs": state["logs"] + [f"❌ {error_msg}"]}
    return {
        **state,
        "analytics": analytics,
        "logs": state["logs"] + ["📊 Analytics: Campaign metrics calculated ✅"]
    }


class SimplePipeline:
    """Simple sequential pipeline without langgraph dependency"""
    
    def invoke(self, state: AgentState) -> AgentState:
        """Execute pipeline sequentially through all agents"""
        # Execute agents in sequence
        state = orchestrator_node(state)
        state = research_node(state)
        state = analyst_node(state)
        state = writer_node(state)
        state = variant_node(state)
        state = analytics_node(state)
        return state


# Create pipeline instance
pipeline = SimplePipeline()