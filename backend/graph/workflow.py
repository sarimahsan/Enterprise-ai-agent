from langgraph.graph import StateGraph, END
from typing import TypedDict, List
from agents.orchestrator import orchestrate
from agents.research_agent import research_company
from agents.analyst_agent import analyze
from agents.write_agent import write_outreach

class AgentState(TypedDict):
    company: str
    goal: str
    tasks: List[str]
    research: dict
    analysis: dict
    emails: dict
    logs: List[str]

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
        "logs": state["logs"] + [f"🔍 Research Agent: Found news, pain points and context for {state['company']}"]
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

# Build the graph
graph = StateGraph(AgentState)
graph.add_node("orchestrator", orchestrator_node)
graph.add_node("research", research_node)
graph.add_node("analyst", analyst_node)
graph.add_node("writer", writer_node)

graph.set_entry_point("orchestrator")
graph.add_edge("orchestrator", "research")
graph.add_edge("research", "analyst")
graph.add_edge("analyst", "writer")
graph.add_edge("writer", END)

pipeline = graph.compile()