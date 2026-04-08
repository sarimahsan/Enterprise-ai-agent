from langchain_groq import ChatGroq
from core.config import settings
import json

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=settings.GROQ_API_KEY
).bind(response_format={"type": "json_object"})

def analyze(company: str, goal: str, research: dict) -> dict:
    response = llm.invoke(f"""
You are a senior business analyst and sales strategist.

Company: {company}
Goal: {goal}

Research:
NEWS: {research['news']}
ABOUT: {research['about']}
GOAL CONTEXT: {research['goal_context']}

Return this exact JSON:
{{
  "pain_points": ["pain point 1", "pain point 2", "pain point 3"],
  "opportunity": "one sentence describing the key opportunity",
  "tone": "professional",
  "key_fact": "one specific recent fact about this company to reference in outreach",
  "decision_maker": "likely job title of the person to contact"
}}
""")

    try:
        return json.loads(response.content)
    except Exception as e:
        print(f"Analyst parse failed: {e}\nRaw: {response.content}")
        return {
            "pain_points": ["operational efficiency", "scaling challenges", "competitive pressure"],
            "opportunity": f"Help {company} achieve {goal}",
            "tone": "professional",
            "key_fact": f"{company} is actively expanding its market presence",
            "decision_maker": "VP of Sales"
        }