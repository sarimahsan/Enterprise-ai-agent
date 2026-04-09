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

def generate_variants(company: str, analysis: dict) -> dict:
    llm = get_llm()
    """Generate A/B variants and multi-channel outreach"""
    pain_points = analysis.get("pain_points", ["growth challenges"])
    if isinstance(pain_points, list):
        pain_points = ", ".join(pain_points[:2])
    
    key_fact = analysis.get("key_fact", f"{company} is looking to scale")

    response = llm.invoke(f"""
Generate A/B testing variants and multi-channel outreach for {company}.

Pain Points: {pain_points}
Key Fact: {key_fact}

Respond with ONLY valid JSON (no markdown, no extra text):
{{
  "ab_variants": {{
    "subject_a": "Professional email subject about growth",
    "subject_b": "Curiosity-driven email subject",
    "tone_a": "Professional and consultative",
    "tone_b": "Casual and conversational"
  }},
  "channels": {{
    "linkedin": {{
      "headline": "LinkedIn connection message",
      "follow_up": "Follow up message after connection"
    }},
    "sms": {{
      "message": "Brief SMS message"
    }}
  }},
  "strategy": "Brief description of the multi-channel approach"
}}
""")

    try:
        # Extract JSON from response (in case there's extra text)
        content = response.content
        # Try to find JSON object in the response
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            json_str = json_match.group(0)
            # Clean up any escaped newlines
            json_str = json_str.replace('\\n', ' ')
            return json.loads(json_str)
        else:
            raise ValueError("No JSON found in response")
    except Exception as e:
        print(f"Variant generation failed: {e}, using fallback")
        return {
            "ab_variants": {
                "subject_a": f"Quick insight for {company}",
                "subject_b": f"Addressing your {pain_points.split(',')[0]} challenges",
                "tone_a": "Professional",
                "tone_b": "Friendly"
            },
            "channels": {
                "linkedin": {
                    "headline": f"Hi! Noticed {company}'s recent growth. Have ideas to help.",
                    "follow_up": "Would love to discuss growth strategies that work for companies like yours."
                },
                "sms": {
                    "message": f"Quick idea about {company}'s expansion. Free 15min?"
                }
            },
            "strategy": "Multi-touch approach across email, LinkedIn, and SMS for maximum reach"
        }
