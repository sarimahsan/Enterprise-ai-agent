# 🚀 Quick Start Guide - New Features

## Installation (5 minutes)

### 1. Install Python Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Install Node Dependencies
```bash
cd frontend
npm install
```

### 3. Initialize Database
```bash
python -c "from core.database import init_db; init_db()"
```

### 4. Set Environment Variables
Create `.env` file in project root:
```env
# Database (optional - defaults to SQLite)
DATABASE_URL=sqlite:///./flowforge.db

# Notion (optional - for Notion export)
NOTION_API_KEY=ntn_xxxxxxxxxxxxx

# Google (optional - for Google Docs)
GOOGLE_CLIENT_ID=xxxxx.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=xxxxx
```

### 5. Start Backend
```bash
cd backend
python -m uvicorn main:app --reload
# Server running at http://localhost:8000
```

### 6. Start Frontend
```bash
cd frontend
npm run dev
# App running at http://localhost:5174
```

---

## Using New Features

### 1. **Quality Score Review**

**Code:**
```javascript
// React component - already included in frontend
import EmailQualityReview from './components/EmailQualityReview'

<EmailQualityReview emails={emails} company="Acme Corp" />
```

**What it does:**
- Scores each email 0-100
- Shows specific issues found
- Provides recommendations
- Takes 2-3 seconds per email

---

### 2. **Objection Handler**

**Code:**
```javascript
// React component - already included
import ObjectionHandler from './components/ObjectionHandler'

<ObjectionHandler 
  company="Acme Corp" 
  goal="Sell software license"
  analysis={analysisData}
/>
```

**What it does:**
- Generates 3 likely objections
- Pre-writes responses
- Shows alternatives
- Copy-paste ready responses

---

### 3. **Lead Scoring Dashboard**

**Code:**
```javascript
// React component - use as new tab
import LeadScoringDashboard from './components/LeadScoringDashboard'

// Add to App.jsx tabs
{activeTab === "leads" && <LeadScoringDashboard />}
```

**What it does:**
- Shows all companies ranked by opportunity
- Color-coded by urgency (red=critical)
- Quick filtering and sorting
- Updates in real-time

---

### 4. **Follow-up Timeline**

**API Call:**
```javascript
const response = await fetch('/api/followup/generate-timeline', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    campaign_id: 1,
    industry: "saas",  // or "financial", "manufacturing", etc
    initial_send_date: "2024-04-15T09:00:00"
  })
})
const timeline = await response.json()
// Returns: [Day1, Day4, Day8, Day15] with dates + rationale
```

**What it does:**
- Auto-generates follow-up dates
- Based on industry best practices
- Can add to Google Calendar
- Tracks if scheduled/sent

---

### 5. **Export to Notion**

**Code:**
```javascript
const response = await fetch('/api/export/to-notion', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    campaign_id: 1,
    notion_database_id: "abc123def456...",  // user's Notion DB
    include_emails: true,
    include_objections: true
  })
})
const result = await response.json()
// Returns: notion_page_id and link to Notion page
```

**What it does:**
- Creates new Notion page
- Fills with campaign data
- Includes email sequence
- Includes objection guide
- Shareable with team

**How to get Notion Database ID:**
1. Create database in Notion
2. Go to database settings → Share
3. Copy ID from URL (32 characters)

---

### 6. **Export to Google Docs**

**Code:**
```javascript
const response = await fetch('/api/export/to-google-docs', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    campaign_id: 1,
    include_emails: true,
    include_objections: true
  })
})
const result = await response.json()
// Returns: google_doc_id and direct link
// Automatically opens in new tab!
```

**What it does:**
- Creates formatted Google Doc
- Auto-opens in browser
- Includes all campaign info
- Shareable with link

---

## Database Structure (Simplified)

```
companies
├─ id, name, industry
├─ opportunity_score (0-100)
├─ urgency_level (critical/high/medium/low)
└─ research_data (JSON)

campaigns
├─ id, company_id, goal
├─ analysis_data
└─ status

emails
├─ id, campaign_id
├─ subject, body
├─ confidence_score (0-100)
├─ personalization_score (0-10)
└─ quality_feedback

objections
├─ id, campaign_id
├─ objection_text
├─ likelihood_percentage
├─ response_text
└─ alternatives[]

followups
├─ id, campaign_id
├─ sequence_day (1,4,8,15)
├─ suggested_send_time
└─ calendar_event_id
```

---

## Common Tasks

### Check if Backend is Running
```bash
curl http://localhost:8000/api/health
# Should return: {"status":"ok",...}
```

### Review What's in Database
```python
from core.database import SessionLocal
from models.database_models import Company, Campaign

db = SessionLocal()
companies = db.query(Company).all()
for c in companies:
    print(f"{c.name}: {c.opportunity_score}/100")
```

### Export Campaign to Notion
```python
import requests

response = requests.post(
    'http://localhost:8000/api/export/to-notion',
    json={
        'campaign_id': 1,
        'notion_database_id': 'YOUR_DB_ID_HERE',
        'include_emails': True,
        'include_objections': True
    }
)
print(response.json())
```

### Get Lead Dashboard
```python
import requests

response = requests.get('http://localhost:8000/api/dashboard/leads')
leads = response.json()
print(f"Total companies: {leads['total_companies']}")
print(f"Critical priority: {leads['high_priority_count']}")
```

---

## Troubleshooting

**Error: "Database is locked"**
- Solution: SQLite issue, use PostgreSQL for production
- Or: Close other connections to database

**Error: "Module not found"**
- Solution: Run `pip install -r requirements.txt`
- Or: Check Python version is 3.9+

**Error: "Notion API key invalid"**
- Solution: Check NOTION_API_KEY is set correctly
- Or: Generate new key at notion.so/my-integrations

**Frontend components not showing**
- Solution: Run `npm install` in frontend folder
- Or: Clear browser cache (Ctrl+Shift+Delete)

**Quality scores seem low**
- This is normal! Use recommendations to improve
- Resubmit email after changes
- Aim for 75+ score before sending

---

## Next: Integrate into Existing App

### Add New Tabs to App.jsx
```javascript
const [activeTab, setActiveTab] = useState("dashboard")

// Add to tabs
<Tab id="leads" label="Leads" icon={Globe} />
<Tab id="quality" label="Quality" icon={CheckCircle} />

// Add content
{activeTab === "leads" && <LeadScoringDashboard />}
{activeTab === "quality" && <EmailQualityReview emails={emails} company={company} />}
```

### Import Components
```javascript
import LeadScoringDashboard from './components/LeadScoringDashboard'
import EmailQualityReview from './components/EmailQualityReview'
import ObjectionHandler from './components/ObjectionHandler'
import ExportPanel from './components/ExportPanel'
```

---

## API Reference (All Endpoints)

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/quality/review-email` | POST | Score one email |
| `/quality/score-email-sequence` | POST | Score all emails |
| `/objections/generate` | POST | Generate objections |
| `/objections/save-for-campaign` | POST | Save to database |
| `/objections/campaign/{id}` | GET | Get saved objections |
| `/dashboard/leads` | GET | Show all leads |
| `/dashboard/update-lead-score` | PUT | Update lead scores |
| `/followup/generate-timeline` | POST | Create follow-up dates |
| `/followup/schedule-to-calendar` | POST | Add to Google Calendar |
| `/export/save-to-database` | POST | Save campaign to DB |
| `/export/to-notion` | POST | Export to Notion |
| `/export/to-google-docs` | POST | Export to Google Docs |

---

## Performance Notes

- Quality scoring: ~2-3 seconds per email
- Objection generation: ~3-5 seconds
- Dashboard load: <1 second
- Export to Notion: ~2-3 seconds
- Export to Google Docs: ~2-3 seconds

All requests are async and won't block the UI!

---

## Support / Documentation

Full documentation available in:
- `NEW_FEATURES_DOCUMENTATION.md` - Complete feature guide
- `API_INTEGRATION_GUIDE.md` - All API examples
- `FEATURE_CHECKLIST.md` - Feature breakdown
- `IMPLEMENTATION_SUMMARY.md` - What's included

---

## You're Ready! 🎉

All features are implemented and ready to use. Start with:
1. Initialize database
2. Run backend
3. Run frontend
4. Try quality review on an email
5. Generate objections
6. Check lead dashboard
7. Export to Notion/Google Docs

Enjoy! 🚀
