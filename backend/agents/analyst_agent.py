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

Research about the company:
NEWS: {research['news']}
ABOUT: {research['about']}
GOAL CONTEXT: {research['goal_context']}

Based on this research, return ONLY a JSON object with these exact fields:
{{
  "pain_points": ["pain point 1", "pain point 2", "pain point 3"],
  "opportunity": "one sentence describing the key opportunity",
  "tone": "professional/friendly/urgent",
  "key_fact": "one recent specific fact about this company to reference in outreach",
  "decision_maker": "likely job title of the person to contact"
}}

Return ONLY the JSON. No explanation. No markdown.
""")

    text = response.content.strip()
    text = text.replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(text)
    except Exception:
        return {
            "pain_points": ["operational efficiency", "scaling challenges", "competitive pressure"],
            "opportunity": f"Help {company} achieve {goal} through targeted outreach",
            "tone": "professional",
            "key_fact": f"{company} is actively expanding its market presence",
            "decision_maker": "VP of Sales"
        }