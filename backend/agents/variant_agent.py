from langchain_groq import ChatGroq
from core.config import settings
import json

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=settings.GROQ_API_KEY
).bind(response_format={"type": "json_object"})

def generate_variants(company: str, analysis: dict) -> dict:
    """Generate A/B variants and multi-channel outreach"""
    pain_points = ", ".join(analysis["pain_points"])

    response = llm.invoke(f"""
You are a growth marketing strategist expert in A/B testing and multi-channel campaigns.

Company: {company}
Pain Points: {pain_points}
Key Fact: {analysis['key_fact']}

Generate A/B testing variants AND multi-channel outreach options.

Return EXACTLY this JSON (no variations):
{{
  "ab_variants": {{
    "subject_a": "Direct subject focusing on pain point",
    "subject_b": "Curiosity-driven subject line",
    "tone_a": "Professional and consultative",
    "tone_b": "Casual and conversational"
  }},
  "channels": {{
    "linkedin": {{
      "headline": "Quick LinkedIn connection request message (2-3 sentences)",
      "follow_up": "Value-add follow-up after connection"
    }},
    "sms": {{
      "message": "SMS outreach (max 160 chars, conversational)"
    }}
  }},
  "strategy": "One sentence explaining the multi-channel approach"
}}
""")

    try:
        return json.loads(response.content)
    except Exception as e:
        print(f"Variant generation failed: {e}")
        return {
            "ab_variants": {
                "subject_a": f"Quick insight for {company}",
                "subject_b": f"Are you facing {analysis['pain_points'][0]}?",
                "tone_a": "Professional",
                "tone_b": "Friendly"
            },
            "channels": {
                "linkedin": {
                    "headline": f"Hi! Noticed {company}'s recent moves. Have an idea.",
                    "follow_up": "Would love to share a quick insight on your growth strategy."
                },
                "sms": {
                    "message": f"Quick idea about {company}'s expansion. Free 15min?"
                }
            },
            "strategy": "Multi-touch approach across email, LinkedIn, and SMS for maximum reach"
        }
