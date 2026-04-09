from langchain_groq import ChatGroq
from core.config import settings

_llm = None

def get_llm():
    """Lazy load LLM to avoid initialization errors at import time"""
    global _llm
    if _llm is None:
        _llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            api_key=settings.GROQ_API_KEY
        )
    return _llm

def orchestrate(goal: str) -> list[str]:
    llm = get_llm()
    response = llm.invoke(f"""
You are a business operations orchestrator.
Break the following goal into 2-4 clear, actionable tasks.
Return ONLY a numbered list. No explanations.

Goal: {goal}
""")
    lines = response.content.strip().split("\n")
    tasks = [l.strip() for l in lines if l.strip()]
    return tasks