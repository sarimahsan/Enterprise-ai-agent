from langchain_groq import ChatGroq
from core.config import settings
import json
import re

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

def analyze(company: str, goal: str, research: dict) -> dict:
    llm = get_llm()
    news = research.get('news', f'{company} is active in the market')
    about = research.get('about', f'{company} is a growing company')
    goal_context = research.get('goal_context', f'{company} wants to {goal}')

    response = llm.invoke(f"""
You are a senior business analyst and sales strategist analyzing {company}.

Goal: {goal}

Research Summary:
- News: {news[:200]}
- About: {about[:200]}
- Context: {goal_context[:200]}

Generate analysis. Return ONLY valid JSON (no markdown, no extra text):
{{
  "pain_points": ["pain 1", "pain 2", "pain 3"],
  "opportunity": "key opportunity for this company",
  "tone": "professional",
  "key_fact": "one specific recent fact about this company",
  "decision_maker": "likely job title of decision maker"
}}
""")

    try:
        content = response.content
        # Extract JSON from response
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            json_str = json_match.group(0)
            # Clean up escape sequences
            json_str = json_str.replace('\\n', ' ').replace('\\"', '"')
            parsed = json.loads(json_str)
            # Ensure all required fields
            return {
                "pain_points": parsed.get("pain_points", ["operational efficiency", "scaling challenges", "competitive pressure"]),
                "opportunity": parsed.get("opportunity", f"Help {company} achieve {goal}"),
                "tone": parsed.get("tone", "professional"),
                "key_fact": parsed.get("key_fact", f"{company} is actively expanding"),
                "decision_maker": parsed.get("decision_maker", "VP of Sales")
            }
        else:
            raise ValueError("No JSON found in response")
    except Exception as e:
        print(f"Analyst parse failed: {e}\nRaw: {response.content[:200]}")
        return {
            "pain_points": ["operational efficiency", "scaling challenges", "competitive pressure"],
            "opportunity": f"Help {company} achieve {goal}",
            "tone": "professional",
            "key_fact": f"{company} is actively expanding its market presence",
            "decision_maker": "VP of Sales"
        }