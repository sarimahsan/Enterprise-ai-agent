from langgraph.graph import StateGraph, END
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
    tasks = orchestrate(f"Outreach campaign for {state['company']}: {state['goal']}")
    return {
        **state,
        "tasks": tasks,
        "logs": state["logs"] + [f"🧠 Orchestrator: Planning outreach for {state['company']}"]
    }

def research_node(state: AgentState) -> AgentState:
    result = research_company(state["company"], state["goal"])
    return {
        **state,
        "research": result,
        "logs": state["logs"] + [f"🔍 Research Agent: Found data for {state['company']}"]
    }

def analyst_node(state: AgentState) -> AgentState:
    result = analyze(state["company"], state["goal"], state["research"])
    return {
        **state,
        "analysis": result,
        "logs": state["logs"] + [f"📊 Analyst Agent: Identified opportunity — {result.get('opportunity', '')}"]
    }

def writer_node(state: AgentState) -> AgentState:
    result = write_outreach(state["company"], state["goal"], state["analysis"])
    return {
        **state,
        "emails": result,
        "logs": state["logs"] + ["✍️ Writer Agent: 3-email sequence ready ✅"]
    }

def variant_node(state: AgentState) -> AgentState:
    result = generate_variants(state["company"], state["analysis"])
    return {
        **state,
        "variants": result,
        "logs": state["logs"] + ["🎯 Variant Agent: A/B testing & multi-channel ready ✅"]
    }

def analytics_node(state: AgentState) -> AgentState:
    """Generate mock analytics for dashboard"""
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
    return {
        **state,
        "analytics": analytics,
        "logs": state["logs"] + ["📊 Analytics: Campaign metrics calculated ✅"]
    }

graph = StateGraph(AgentState)
graph.add_node("orchestrator", orchestrator_node)
graph.add_node("research", research_node)
graph.add_node("analyst", analyst_node)
graph.add_node("writer", writer_node)
graph.add_node("variant", variant_node)
graph.add_node("analytics", analytics_node)

graph.set_entry_point("orchestrator")
graph.add_edge("orchestrator", "research")
graph.add_edge("research", "analyst")
graph.add_edge("analyst", "writer")
graph.add_edge("writer", "variant")
graph.add_edge("variant", "analytics")
graph.add_edge("analytics", END)

pipeline = graph.compile()