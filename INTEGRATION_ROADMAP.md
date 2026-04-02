# 🎯 Integration Priority Roadmap

## What to Build Next (Highest ROI First)

---

## Week 1: Critical Path Integrations (Highest Impact)

### 1. Apollo.io Integration (Score: 10/10)
**Why First:** Without real leads, nothing else matters
- Time estimate: 4-6 hours
- Impact: 50+ qualified leads per query
- Effort: Easy (REST API)

**What to do:**
```python
# In backend/services/lead_service.py, add:
import apollo  # pip install apollo-python

async def find_leads_apollo(company: str) -> List[Lead]:
    client = apollo.ApolloClient(api_key=APOLLO_KEY)
    response = client.search_leads(
        company_name=company,
        job_titles=["VP of Sales", "Sales Director"],
        employee_count_min=50
    )
    return [Lead(...) for contact in response]
```

### 2. SendGrid Integration (Score: 9/10)
**Why Second:** Campaign execution needs real email delivery
- Time estimate: 3-4 hours
- Impact: Real emails sent + open/click tracking
- Effort: Easy (Simple API)

**What to do:**
```python
# In backend/services/outreach_service.py, add:
import sendgrid
from sendgrid.helpers.mail import Mail

async def send_email(to: str, subject: str, body: str):
    message = Mail(
        from_email='campaigns@yourcompany.com',
        to_emails=to,
        subject=subject,
        plain_text_content=body
    )
    sg = sendgrid.SendGridAPIClient(SENDGRID_KEY)
    response = sg.send(message)
    # Track message ID for open/click tracking
```

### 3. Google Calendar Integration (Score: 8/10)
**Why Third:** Meeting booking closes deals
- Time estimate: 4-5 hours
- Impact: Auto-booked calls, no scheduling friction
- Effort: Medium (OAuth flow)

**What to do:**
```python
# In backend/services/meeting_service.py, add:
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

async def create_calendar_event(email: str, start_time: datetime):
    creds = Credentials.from_service_account_file('creds.json')
    service = build('calendar', 'v3', credentials=creds)
    body = {
        'summary': 'Discovery Call',
        'start': {'dateTime': start_time.isoformat()},
        'end': {'dateTime': (start_time + timedelta(minutes=30)).isoformat()},
        'attendees': [{'email': email}]
    }
    service.events().insert(calendarId='primary', body=body).execute()
```

---

## Week 2: Growth Integrations

### 4. LinkedIn API (Score: 7/10)
**Time:** 4-6 hours | **Impact:** Prospecting + messaging
```python
# Find prospects on LinkedIn
async def search_linkedin(company: str) -> List[Profile]:
    # Uses LinkedIn API (needs approval)
    pass
```

### 5. Twilio SMS (Score: 7/10)
**Time:** 2-3 hours | **Impact:** SMS follow-ups
```python
# Send SMS to prospects
import twilio

async def send_sms(phone: str, message: str):
    client = twilio.rest.Client(ACCOUNT_SID, AUTH_TOKEN)
    message = client.messages.create(
        body=message,
        from_=TWILIO_NUMBER,
        to=phone
    )
```

### 6. PostgreSQL Database (Score: 10/10)
**Time:** 5-6 hours | **Impact:** Data persistence
```python
# Replace in-memory dicts with real database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://user:password@localhost/flowforge"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

# Migrate all services to use sessions instead of self.dict
```

---

## Week 3: Essential Integrations

### 7. Salesforce/HubSpot Sync (Score: 8/10)
**Time:** 6-8 hours | **Impact:** Two-way CRM sync
```python
# Push/pull leads and deals to CRM
async def sync_lead_to_crm(lead: Lead):
    # Update or create in Salesforce/HubSpot
    pass

async def get_opportunities_from_crm():
    # Pull deals to update forecasts
    pass
```

### 8. Engagement Tracking (Score: 8/10)
**Time:** 4-5 hours | **Impact:** Real engagement data
```python
# Track email opens, clicks, replies
# Uses webhooks from SendGrid
@app.post("/webhooks/sendgrid")
async def handle_sendgrid_event(event: dict):
    if event['type'] == 'open':
        await update_interaction_status(event['email'], 'opened')
    elif event['type'] == 'click':
        await update_interaction_status(event['email'], 'clicked')
```

---

## Implementation Sequence (Fastest Path)

```
Week 1 (Phase 1 Functional):
├─ Day 1: Apollo.io integration
├─ Days 2-3: SendGrid integration
├─ Days 4-5: Google Calendar integration
└─ Test: Full end-to-end campaign

Week 2 (Phase 1 Polish):
├─ Day 1: PostgreSQL setup
├─ Days 2-3: LinkedIn API
├─ Days 4-5: Twilio SMS
└─ Test: Live pilots with 100 prospects

Week 3 (Phase 2 Ready):
├─ Days 1-2: CRM sync
├─ Days 3-4: Engagement tracking
├─ Day 5: Compliance logging
└─ Test: Full Phase 2 simulation

Week 4+: Scale & Optimize
├─ Run Phase 1 live at scale
├─ Measure real ROI
├─ Collect Phase 2 learnings
└─ Plan Phase 2 rollout
```

---

## Detailed Integration Examples

### Apollo.io (Easiest First Integration)

1. **Get API key:** [apollo.io/developers](https://apollo.io/developers)

2. **Add to .env:**
```env
APOLLO_API_KEY=your_apollo_key
```

3. **Create Apollo service:**
```python
# backend/services/apollo_service.py
import requests

class ApolloService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.apollo.io/v1"
    
    async def search_people(self, company: str, limit: int = 50):
        response = requests.get(
            f"{self.base_url}/people/search",
            headers={"Content-Type": "application/json"},
            params={
                "api_key": self.api_key,
                "q_organization_name": company,
                "page": 1,
                "per_page": limit
            }
        )
        
        people = []
        for contact in response.json()["contacts"]:
            people.append({
                "email": contact.get("email"),
                "name": contact.get("name"),
                "title": contact.get("title"),
                "company": company,
                "linkedin_url": contact.get("linkedin_url")
            })
        return people
```

4. **Use in prospector:**
```python
# In lead_service.py
from services.apollo_service import ApolloService

apollo = ApolloService(api_key=settings.APOLLO_API_KEY)

async def find_leads(self, company: str):
    contacts = await apollo.search_people(company)
    # Convert to Lead objects
    leads = [Lead(...) for contact in contacts]
    return leads
```

5. **Test in API:**
```bash
curl -X POST http://localhost:8000/api/prospecting/find-leads \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "Salesforce",
    "industry": "SaaS",
    "target_titles": ["VP of Sales"],
    "limit": 50
  }'
```

---

### SendGrid (Second Integration)

1. **Get API key:** [sendgrid.com/pricing](https://sendgrid.com/pricing)

2. **Add to .env:**
```env
SENDGRID_API_KEY=your_sendgrid_key
```

3. **Update outreach service:**
```python
# In services/outreach_service.py
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Cc, Bcc, Subject

async def send_personalized_email(
    to_email: str,
    to_name: str,
    subject: str,
    body: str,
    from_name: str = "Your Sales Team"
):
    message = Mail(
        from_email=f"{from_name} <noreply@yourcompany.com>",
        to_emails=to_email,
        subject=subject,
        plain_text_content=body,
        html_content=f"<html><body>{body}</body></html>"
    )
    
    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(message)
        return {
            "status": "sent",
            "message_id": response.headers.get('X-Message-ID')
        }
    except Exception as e:
        return {"status": "failed", "error": str(e)}
```

4. **Add webhook tracking:**
```python
@app.post("/webhooks/sendgrid")
async def handle_sendgrid_webhook(request: dict):
    """Handle open, click, bounce events from SendGrid"""
    event_type = request.get('event')
    email = request.get('email')
    
    if event_type == 'open':
        # Update interaction in DB as 'opened'
        await update_interaction(email, 'opened')
    elif event_type == 'click':
        await update_interaction(email, 'clicked')
    elif event_type == 'bounce':
        await update_interaction(email, 'bounced')
    
    return {"status": "ok"}
```

---

### PostgreSQL (Critical for Production)

1. **Install:**
```bash
brew install postgresql
psql --version
```

2. **Create database:**
```sql
CREATE DATABASE flowforge_prod;
```

3. **Add to .env:**
```env
DATABASE_URL=postgresql://user:password@localhost/flowforge_prod
```

4. **Create schema file:**
```python
# backend/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from core.config import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

5. **Create models:**
```python
# backend/models/database.py
from sqlalchemy import Column, String, Integer, Float, DateTime
from database import Base

class LeadDB(Base):
    __tablename__ = "leads"
    
    id = Column(String, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    company = Column(String)
    title = Column(String)
    score = Column(String)  # hot/warm/cold
    created_at = Column(DateTime)
    # ... more fields
```

---

## Success Metrics After Each Integration

### After Apollo (Week 1 Day 1):
- [ ] Can find 50+ leads per search
- [ ] Leads have email, name, title
- [ ] Leads scored for quality

### After SendGrid (Week 1 Day 3):
- [ ] Emails send without errors
- [ ] Open/click tracking working
- [ ] Reply detection in progress

### After Google Calendar (Week 1 Day 5):
- [ ] Can see your available slots
- [ ] Meeting invites auto-sent
- [ ] Leads confirm attendance

### After All Week 1:
- [ ] Full end-to-end: Find → Email → Book call
- [ ] Metrics showing: 50 leads → 50% open → 10% clicks → 3 booked

---

## Budget Estimate

| Service | Monthly Cost | What You Get |
|---------|-------------|-------------|
| Apollo.io | $100-500 | 5K-25K leads/month |
| SendGrid | $30-300 | 10K-100K emails/month |
| Google Workspace | $12/user | Calendar + Gmail |
| LinkedIn API | Free-500 | Prospecting + messaging |
| Twilio | $50-200 | 1K-5K SMS/month |
| PostgreSQL | $30-300 | Managed database |
| **TOTAL** | **$222-1,800** | **Complete operation** |

**ROI:** One deal closes → pays for integrations for 6+ months ✅

---

## Quick Integration Checklist

For each integration:
- [ ] Get API key
- [ ] Add to .env
- [ ] Create service class
- [ ] Add to routes
- [ ] Add to schema
- [ ] Test with curl/Postman
- [ ] Update frontend
- [ ] Document usage

---

## Support Resources

**Apollo.io:**
- Docs: https://apollo.io/api-documentation
- Python SDK: None (REST only, that's fine)

**SendGrid:**
- Docs: https://docs.sendgrid.com/
- Python SDK: `pip install sendgrid`

**Google Calendar:**
- Docs: https://developers.google.com/calendar
- Python SDK: `pip install google-api-python-client`

**PostgreSQL:**
- Docs: https://www.postgresql.org/docs/
- Python Driver: `pip install psycopg2`

---

**Your integrations roadmap is clear. Execute in this sequence and you'll have a fully functional Phase 1 autonomous sales system in 3 weeks. 🚀**
