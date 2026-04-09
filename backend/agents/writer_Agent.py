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

def write_outreach(company: str, goal: str, analysis: dict) -> dict:
    llm = get_llm()
    pain_points = analysis.get("pain_points", [])
    if isinstance(pain_points, list):
        pain_points_str = ", ".join(pain_points[:2])
    else:
        pain_points_str = str(pain_points)
    
    first_pain = pain_points[0] if isinstance(pain_points, list) and len(pain_points) > 0 else "growth"
    key_fact = analysis.get('key_fact', f'{company} is growing')
    tone = analysis.get('tone', 'Professional')
    decision_maker = analysis.get('decision_maker', 'Decision Maker')

    response = llm.invoke(f"""
You are an expert B2B sales copywriter. Generate 3 professional emails.

Company: {company}
Goal: {goal}
Pain Point: {first_pain}
Key Fact: {key_fact}
Tone: {tone}

Write 3 emails (subject and 3-4 sentence body each).

Return ONLY valid JSON (no markdown, no extra text):
{{
  "email_1": {{"subject": "email subject", "body": "email body text"}},
  "email_2": {{"subject": "email subject", "body": "email body text"}},
  "email_3": {{"subject": "email subject", "body": "email body text"}},
  "summary": "Brief strategy summary"
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
            # Ensure all required keys exist
            return {
                "email_1": parsed.get("email_1", {"subject": "Subject 1", "body": "Body 1"}),
                "email_2": parsed.get("email_2", {"subject": "Subject 2", "body": "Body 2"}),
                "email_3": parsed.get("email_3", {"subject": "Subject 3", "body": "Body 3"}),
                "summary": parsed.get("summary", "Professional outreach sequence")
            }
        else:
            raise ValueError("No JSON found in response")
    except Exception as e:
        print(f"Writer parse failed: {e}\nRaw: {response.content[:200]}")
        return {
            "email_1": {"subject": f"Quick question about {company}", "body": f"Hi {decision_maker}, I noticed {key_fact}. Would love to discuss how we can help with {first_pain}."},
            "email_2": {"subject": f"Following up - {goal}", "body": f"Hi {decision_maker}, wanted to share a resource about {first_pain} that might be helpful for {company}."},
            "email_3": {"subject": f"Last touch - opportunity for {company}", "body": f"Hi {decision_maker}, just checking if now is a better time to chat about {goal}."},
            "summary": "Three-email professional outreach sequence"
        }