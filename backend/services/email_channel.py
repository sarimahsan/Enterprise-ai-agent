"""
Email Channel - Generate and send professional email templates
"""
from langchain_groq import ChatGroq
from core.config import settings
from services.gmail_service import get_gmail_service
import json

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=settings.GROQ_API_KEY
).bind(response_format={"type": "json_object"})

def generate_email_templates(company: str, analysis: dict, emails: dict) -> dict:
    """
    Generate professional HTML email templates for multi-channel distribution.
    Takes writer agent emails and creates proper templates.
    """
    pain_points = ", ".join(analysis["pain_points"])
    
    response = llm.invoke(f"""
You are an expert email template designer creating professional B2B sales emails.

Company: {company}
Key Fact: {analysis['key_fact']}
Pain Points: {pain_points}
Decision Maker: {analysis['decision_maker']}

Email 1 Subject: {emails['email_1']['subject']}
Email 2 Subject: {emails['email_2']['subject']}
Email 3 Subject: {emails['email_3']['subject']}

Create 3 professional HTML email templates. Each should:
- Use modern responsive design
- Include clear CTA buttons
- Have professional formatting
- Include signature

Return EXACTLY this JSON:
{{
  "email_1": {{
    "html": "<html>...</html> (full HTML with inline styles)",
    "preview": "Preview text for inbox",
    "cta_text": "Button text",
    "cta_url": "https://calendly.com/demo"
  }},
  "email_2": {{
    "html": "<html>...</html>",
    "preview": "Preview text",
    "cta_text": "Button text",
    "cta_url": "https://calendly.com/demo"
  }},
  "email_3": {{
    "html": "<html>...</html>",
    "preview": "Preview text",
    "cta_text": "Button text",
    "cta_url": "https://calendly.com/demo"
  }},
  "send_schedule": ["Day 1", "Day 4", "Day 7"]
}}
""")

    try:
        return json.loads(response.content)
    except Exception as e:
        print(f"Email template generation failed: {e}")
        return {
            "email_1": {
                "html": f"<html><body><p>Subject: {emails['email_1']['subject']}</p><p>{emails['email_1']['body']}</p></body></html>",
                "preview": emails['email_1']['subject'][:50],
                "cta_text": "Learn More",
                "cta_url": "https://calendly.com"
            },
            "email_2": {
                "html": f"<html><body><p>Subject: {emails['email_2']['subject']}</p><p>{emails['email_2']['body']}</p></body></html>",
                "preview": emails['email_2']['subject'][:50],
                "cta_text": "Let's Talk",
                "cta_url": "https://calendly.com"
            },
            "email_3": {
                "html": f"<html><body><p>Subject: {emails['email_3']['subject']}</p><p>{emails['email_3']['body']}</p></body></html>",
                "preview": emails['email_3']['subject'][:50],
                "cta_text": "Quick Call?",
                "cta_url": "https://calendly.com"
            },
            "send_schedule": ["Day 1", "Day 4", "Day 7"]
        }

def send_campaign_email(email_to: str, email_subject: str, html_body: str, user_email: str = None) -> dict:
    """
    Send campaign email via Gmail
    """
    try:
        gmail = get_gmail_service()
        
        # Check if Google libraries are available
        if not gmail.available:
            return {
                "success": False,
                "message": "❌ Gmail not configured. Install: pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client",
                "action": "Install dependencies and restart"
            }
        
        # If not authenticated yet, attempt authentication
        if not gmail.service:
            authed = gmail.authenticate()
            if not authed:
                return {
                    "success": False,
                    "message": "❌ Gmail authentication failed. Please set up OAuth2 credentials.",
                    "action": "Set up credentials at https://console.cloud.google.com/apis/credentials"
                }
        
        # Get sender email
        if not user_email:
            profile = gmail.get_authenticated_user()
            if not profile:
                return {"success": False, "message": "❌ Failed to get Gmail user profile"}
            user_email = profile["email"]
        
        # Send the email
        success = gmail.send_email(
            to=email_to,
            subject=email_subject,
            body=html_body
        )
        
        return {
            "success": success,
            "message": f"✅ Email sent to {email_to}" if success else f"❌ Failed to send email to {email_to}",
            "from": user_email,
            "to": email_to
        }
    
    except Exception as e:
        return {
            "success": False,
            "message": f"❌ Email service error: {str(e)}"
        }

def create_follow_up_schedule(company: str, decision_maker: str) -> dict:
    """
    Create automated follow-up schedule
    """
    return {
        "email_1": {
            "day": 0,
            "status": "sent",
            "open_rate": 0,
            "click_rate": 0
        },
        "email_2": {
            "day": 4,
            "status": "pending",
            "open_rate": 0,
            "click_rate": 0
        },
        "email_3": {
            "day": 7,
            "status": "pending",
            "open_rate": 0,
            "click_rate": 0
        }
    }
