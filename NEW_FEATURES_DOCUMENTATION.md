# FlowForge AI - New Features Implementation

## Overview
This document outlines all new features added to FlowForge AI, including quality assurance, objection handling, lead scoring, follow-up automation, and export capabilities.

## ✨ New Features

### 1. **AI Confidence Score & Quality Review**
**Purpose:** Ensure every email meets quality standards before sending

**Components:**
- `backend/agents/qa_agent.py` - ConfidenceScoreAgent class
- `frontend/src/components/EmailQualityReview.jsx` - React component for displaying scores

**Features:**
- Overall score (0-100)
- Subject line effectiveness (0-10)
- Body copy quality (0-10)
- Personalization level (0-10)
- Call-to-action strength (0-10)
- Specific issues identified
- Actionable recommendations

**API Endpoints:**
- `POST /api/quality/review-email` - Review single email
- `POST /api/quality/score-email-sequence` - Score entire sequence

**Usage Example:**
```javascript
const response = await fetch('/api/quality/review-email', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email_subject: "Re: Partnership Opportunity",
    email_body: "Hi Sarah...",
    company: "Acme Corp",
    prospect_info: { title: "VP Sales", industry: "SaaS" }
  })
});
```

### 2. **Objection Handler Agent**
**Purpose:** Pre-generate responses to likely objections before the sales call

**Components:**
- `backend/agents/qa_agent.py` - ObjectionHandlerAgent class
- `frontend/src/components/ObjectionHandler.jsx` - React UI component

**Features:**
- Identifies 3 most likely objections
- Estimates likelihood percentage
- Provides primary response
- Includes 2 alternative responses
- Suggests best approach (empathetic, logical, social_proof, value-focused)
- Lists common triggers for each objection

**API Endpoints:**
- `POST /api/objections/generate` - Generate objections for campaign
- `POST /api/objections/save-for-campaign` - Save to database
- `GET /api/objections/campaign/{campaign_id}` - Retrieve saved objections

**Usage Example:**
```javascript
const response = await fetch('/api/objections/generate', {
  method: 'POST',
  body: JSON.stringify({
    company: "Acme Corp",
    goal: "Sell enterprise software license",
    analysis: { market_share: 0.15, avg_deal_size: 50000 }
  })
});
```

### 3. **Lead Scoring Dashboard**
**Purpose:** Visual ranking of all companies by opportunity level and urgency

**Components:**
- `frontend/src/components/LeadScoringDashboard.jsx` - Full dashboard UI

**Key Metrics:**
- **Opportunity Score** (0-100): Overall fit and revenue potential
- **Urgency Level** (critical, high, medium, low): Action priority
- **Fit Score** (0-100): Product-market fit
- **Color Coding:** Red (critical) → Orange (high) → Yellow (medium) → Green (low)

**Features:**
- Sort by opportunity score
- Filter by urgency level
- Progress bars for visual comparison
- Quick view of decision maker
- Industry targeting

**API Endpoint:**
- `GET /api/dashboard/leads` - Fetch all leads with scores
- `PUT /api/dashboard/update-lead-score` - Update scores

**Database Model:** Company table with opportunity_score, urgency_level, fit_score

### 4. **Follow-up Timeline Automation**
**Purpose:** Automatically suggest optimal follow-up timing based on industry best practices

**Components:**
- `backend/services/database_service.py` - FollowUpService class
- Calendar integration with Google Calendar

**Industry-Based Schedules:**
- **SaaS:** Day 1, 4, 8, 15
- **Financial:** Day 1, 3, 7, 14
- **Manufacturing:** Day 1, 5, 10, 20
- **Healthcare:** Day 1, 3, 7, 14
- **Retail:** Day 1, 2, 5, 10

**Features:**
- Automatic schedule generation
- Google Calendar integration
- Custom rationale for each follow-up
- Tracking of scheduled/sent status

**API Endpoints:**
- `POST /api/followup/generate-timeline` - Create follow-up schedule
- `POST /api/followup/schedule-to-calendar` - Add to Google Calendar

**Usage Example:**
```javascript
const response = await fetch('/api/followup/generate-timeline', {
  method: 'POST',
  body: JSON.stringify({
    campaign_id: 1,
    industry: "saas",
    initial_send_date: "2024-04-15T09:00:00"
  })
});
```

### 5. **Email Quality A/B Variants**
**Purpose:** Generate and compare aggressive vs soft email approaches

**Database Model:** EmailVariant table
- variant_letter (A, B)
- approach (aggressive, soft)
- Performance metrics (open_rate, click_rate, reply_rate)

**Features:**
- Automatic variant generation
- Performance tracking
- Statistical comparison
- Winner identification

### 6. **Export to Notion**
**Purpose:** One-click export of entire intelligence report to Notion

**Components:**
- `backend/services/export_service.py` - NotionExportService class
- `frontend/src/components/ExportPanel.jsx` - UI for exports

**Features:**
- Creates new Notion page
- Embeds email sequence
- Includes objection handling guide
- Formatted with company info and scores

**API Endpoint:**
- `POST /api/export/to-notion`

**Configuration:**
- Requires `NOTION_API_KEY` environment variable
- User provides Notion Database ID

**Usage:**
```javascript
const response = await fetch('/api/export/to-notion', {
  method: 'POST',
  body: JSON.stringify({
    campaign_id: 1,
    notion_database_id: "abc123...",
    include_emails: true,
    include_objections: true
  })
});
```

### 7. **Export to Google Docs**
**Purpose:** Create shareable Google Doc with complete campaign details

**Components:**
- `backend/services/export_service.py` - GoogleDocsExportService class
- `frontend/src/components/ExportPanel.jsx` - UI

**Features:**
- Formats report professionally
- Includes email sequence
- Adds objection handling guide
- Returns shareable URL
- Auto-opens in new tab

**API Endpoint:**
- `POST /api/export/to-google-docs`

**Configuration:**
- Requires Google OAuth2 credentials
- Credentials object needed from frontend

## 🗄️ Database Schema

### New Tables Created

1. **companies** - Lead/prospect companies
   - id, name, industry, website, revenue_range
   - opportunity_score, urgency_level, fit_score
   - decision_maker, decision_maker_email
   - research_data (JSON)

2. **campaigns** - Campaign instances
   - id, company_id, name, goal
   - analysis_data, status
   - discovered_pain_points, unique_angle

3. **emails** - Generated emails
   - id, campaign_id, company_id
   - subject, body, html_body
   - confidence_score, personalization_score
   - quality_feedback, recommended_changes
   - status (draft, scheduled, sent, failed, read)
   - tracking: open_count, click_count, reply_received_at

4. **email_variants** - A/B test variants
   - id, email_id, variant_letter (A/B)
   - approach (aggressive, soft)
   - Performance: open_count, click_count, reply_count, conversion_count
   - Calculated rates: open_rate, click_rate, reply_rate

5. **email_scores** - Quality reviews
   - id, email_id
   - overall_score, subject_line_score, body_quality_score
   - personalization_score, call_to_action_score
   - Detailed feedback for each element
   - Issues found and recommendations

6. **objections** - Likely objections & responses
   - id, campaign_id, objection_number
   - objection_text, likelihood_percentage
   - response_text, response_approach
   - alternative_responses, context, triggers

7. **followups** - Follow-up scheduling
   - id, campaign_id, email_id
   - sequence_day, suggested_send_time
   - calendar_event_id, industry, rationale
   - scheduled, sent status tracking

8. **exports** - Export history
   - id, campaign_id
   - export_type (notion, google_docs)
   - destination_url, destination_id
   - exported_at, last_synced_at

9. **analytics** - Campaign metrics
   - id, campaign_id
   - emails_sent, emails_opened, emails_clicked, emails_replied
   - All rates: open_rate, click_rate, reply_rate, bounce_rate, conversion_rate

## 🔧 Backend Implementation Details

### Services Created

1. **database_service.py**
   - CompanyService - CRUD for companies
   - CampaignService - Campaign management
   - EmailService - Email CRUD and status tracking
   - EmailScoreService - Quality score storage
   - ObjectionService - Objection management
   - FollowUpService - Timeline creation
   - AnalyticsService - Metrics aggregation
   - ExportService - Export tracking

2. **qa_agent.py**
   - ConfidenceScoreAgent - Email quality review
   - ObjectionHandlerAgent - Objection generation

3. **export_service.py**
   - NotionExportService - Notion integration
   - GoogleDocsExportService - Google Docs integration

### API Routes (extended_routes.py)

**Quality Assurance:**
- `POST /api/quality/review-email` - Single email review
- `POST /api/quality/score-email-sequence` - Batch scoring

**Objections:**
- `POST /api/objections/generate` - Generate objections
- `POST /api/objections/save-for-campaign` - Save to DB
- `GET /api/objections/campaign/{campaign_id}` - Retrieve

**Dashboard:**
- `GET /api/dashboard/leads` - Lead scoring dashboard
- `PUT /api/dashboard/update-lead-score` - Update scores

**Follow-ups:**
- `POST /api/followup/generate-timeline` - Create timeline
- `POST /api/followup/schedule-to-calendar` - Schedule emails

**Exports:**
- `POST /api/export/save-to-database` - Save to SQL
- `POST /api/export/to-notion` - Export to Notion
- `POST /api/export/to-google-docs` - Export to Google Docs

## 🎨 Frontend Components

1. **LeadScoringDashboard.jsx**
   - Grid layout with company cards
   - Multi-metric scoring visualization
   - Real-time filtering and sorting
   - Color-coded urgency levels

2. **EmailQualityReview.jsx**
   - Tab-based email viewing
   - Score breakdown (4 metrics)
   - Issue highlighting with severity
   - Actionable recommendations
   - Feedback summaries

3. **ObjectionHandler.jsx**
   - Expandable objection cards
   - Likelihood % display
   - Copy-to-clipboard for responses
   - Alternative response list
   - Trigger identification

4. **ExportPanel.jsx**
   - Three export options
   - Notion database ID input
   - Google Docs direct link
   - Status feedback
   - Export history

## 📦 Dependencies Added

```
sqlalchemy>=2.0.0,<3.0.0
alembic>=1.13.0
sqlmodel>=0.0.14
psycopg2-binary>=2.9.0
notion-client>=2.2.0
python-docx>=1.0.0
google-auth>=2.25.0
```

## 🚀 How to Use

### Setup

1. **Install dependencies:**
```bash
pip install -r requirements.txt
npm install --prefix frontend
```

2. **Initialize database:**
```python
from core.database import init_db
init_db()  # Creates all tables
```

3. **Configure environment variables:**
```bash
NOTION_API_KEY=ntn_xxxxx
GOOGLE_CLIENT_ID=xxx.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=xxxxx
DATABASE_URL=sqlite:///./flowforge.db  # or PostgreSQL
```

### Workflow

1. **Generate Campaign**
   - User inputs company & goal
   - System generates analysis & emails

2. **Review Quality**
   - Confidence scores automatically calculated
   - Objections pre-generated
   - Sales rep sees everything before sending

3. **Lead Scoring**
   - Dashboard shows all companies ranked by opportunity
   - Color-coded by urgency
   - Quick visual reference

4. **Export Intelligence**
   - Export to Notion for pipeline integration
   - Export to Google Docs for sharing
   - Save to database for tracking

5. **Schedule Follow-ups**
   - Auto-generate optimal follow-up dates
   - Add to Google Calendar
   - Track send status

## 📊 Metrics Tracked

**Email Level:**
- Confidence score (0-100)
- Personalization score (0-10)
- Subject effectiveness
- Body quality
- CTA strength

**Campaign Level:**
- Open rate %
- Click rate %
- Reply rate %
- Bounce rate %
- Conversion rate %

**Company Level:**
- Opportunity score
- Fit score
- Urgency level

## 🔐 Security Notes

- Never expose API keys in frontend code
- Use environment variables for all secrets
- Notion API key stored server-side only
- Google Docs uses OAuth2 for authentication
- Database credentials in environment

## 🎯 Next Steps (Optional Enhancements)

1. Real-time webhook tracking for email opens/clicks
2. Machine learning for score prediction
3. A/B test winner determination
4. Multi-language support
5. Hubspot/Salesforce CRM integration
6. Email template builder
7. Bulk campaign scheduling
8. Team collaboration features
