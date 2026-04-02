from langchain_groq import ChatGroq
from core.config import settings

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=settings.GROQ_API_KEY
)

def orchestrate(goal: str) -> list[str]:
    response = llm.invoke(f"""
You are a business operations orchestrator.
Break the following goal into 2-4 clear, actionable tasks.
Return ONLY a numbered list. No explanations.

Goal: {goal}
""")
    lines = response.content.strip().split("\n")
    tasks = [l.strip() for l in lines if l.strip()]
    return tasks