from langchain_groq import ChatGroq
from core.config import settings
import json

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=settings.GROQ_API_KEY
).bind(response_format={"type": "json_object"})

def write_outreach(company: str, goal: str, analysis: dict) -> dict:
    pain_points = ", ".join(analysis["pain_points"])

    response = llm.invoke(f"""
You are an expert B2B sales copywriter.

Company: {company}
Goal: {goal}
Pain Points: {pain_points}
Key Fact: {analysis['key_fact']}
Tone: {analysis['tone']}
Decision Maker: {analysis['decision_maker']}

Write a 3-email outreach sequence:
- email_1: Reference this exact fact: {analysis['key_fact']}. Soft CTA.
- email_2: Reference this pain point: {analysis['pain_points'][0]}. Stronger CTA.
- email_3: Short, honest, final attempt. Clear CTA.
- Each body max 5 sentences.

Return this exact JSON:
{{
  "email_1": {{"subject": "...", "body": "..."}},
  "email_2": {{"subject": "...", "body": "..."}},
  "email_3": {{"subject": "...", "body": "..."}},
  "summary": "2 sentence outreach strategy summary"
}}
""")

    try:
        return json.loads(response.content)
    except Exception as e:
        print(f"Writer parse failed: {e}\nRaw: {response.content}")
        return {
            "email_1": {"subject": f"Quick question about {company}", "body": ""},
            "email_2": {"subject": "Following up", "body": ""},
            "email_3": {"subject": "Last touch", "body": ""},
            "summary": ""
        }