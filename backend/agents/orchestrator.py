from langchain_google_genai import ChatGoogleGenerativeAI
from core.config import settings

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=settings.GEMINI_API_KEY
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