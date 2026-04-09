# API Integration Guide - New Features

## Quick Reference

### Base URL
```
http://localhost:8000/api
```

## Quality Assurance Endpoints

### Review Single Email
```http
POST /quality/review-email
Content-Type: application/json

{
  "email_subject": "Re: Partnership Opportunity at Acme",
  "email_body": "Hi Sarah,\n\nI came across Acme Corp's expansion into Europe...",
  "company": "Acme Corp",
  "prospect_info": {
    "title": "VP Sales",
    "company": "Acme Corp",
    "industry": "SaaS"
  }
}
```

**Response:**
```json
{
  "overall_score": 78,
  "subject_line_score": 7.5,
  "body_quality_score": 8.2,
  "personalization_score": 7.0,
  "call_to_action_score": 8.5,
  "issues_found": [
    {
      "issue": "Subject line lacks urgency indicators",
      "severity": "medium"
    }
  ],
  "recommendations": [
    {
      "recommendation": "Add time-sensitive element to subject",
      "example": "Quick question: Acme's Q2 expansion strategy"
    }
  ]
}
```

### Score Email Sequence
```http
POST /quality/score-email-sequence
Content-Type: application/json

{
  "emails": [
    {
      "subject": "Email 1 subject",
      "body": "Email 1 body",
      "prospect_info": {}
    },
    {
      "subject": "Email 2 subject",
      "body": "Email 2 body",
      "prospect_info": {}
    }
  ],
  "company": "Acme Corp"
}
```

**Response:**
```json
{
  "total_emails": 2,
  "average_confidence_score": 76.5,
  "emails": [
    {
      "subject": "Email 1 subject",
      "body": "Email 1 body",
      "confidence_score": 75,
      "personalization_score": 7,
      "feedback": { ... }
    },
    {
      "subject": "Email 2 subject",
      "body": "Email 2 body",
      "confidence_score": 78,
      "personalization_score": 8,
      "feedback": { ... }
    }
  ]
}
```

## Objection Handler Endpoints

### Generate Objections
```http
POST /objections/generate
Content-Type: application/json

{
  "company": "Acme Corp",
  "goal": "Sell enterprise software license",
  "analysis": {
    "market_share": 0.15,
    "avg_deal_size": 50000,
    "growth_rate": 0.25,
    "pain_points": ["Manual processes", "Team hiring"]
  }
}
```

**Response:**
```json
{
  "objections": [
    {
      "objection": "That's too expensive for our budget right now",
      "likelihood_percentage": 82,
      "context": "Early-stage growth companies are budget-conscious",
      "triggers": ["Budget constraints", "New fiscal year", "After failed round"],
      "response": "I understand budget is tight. Most companies see ROI within 90 days. Can we explore a pilot program?",
      "approach": "value-focused",
      "alternatives": [
        "Many CFOs I work with implemented this as a cost-saving measure, not expense.",
        "What if I could show you how this saves you $X annually vs your current solution?"
      ]
    },
    {
      "objection": "We already have a solution for this",
      "likelihood_percentage": 65,
      "context": "Most companies have legacy tools they're invested in",
      "triggers": ["Existing competitor", "Built in-house", "Recent implementation"],
      "response": "Great question. Most teams we work with initially thought the same. But our unique angle is X...",
      "approach": "social_proof",
      "alternatives": [
        "Can I show you how we handle X better?",
        "5/10 of your competitors have switched. Want to see why?"
      ]
    },
    {
      "objection": "Let me think about it and get back to you",
      "likelihood_percentage": 58,
      "context": "Common brush-off when prospect is not convinced",
      "triggers": ["No urgency created", "Too much information", "Bad timing"],
      "response": "Absolutely, happy to. To help, what's one thing I could clarify right now?",
      "approach": "empathetic",
      "alternatives": [
        "What timeframe works best for a follow-up?",
        "What specific concern can I address for you?"
      ]
    }
  ],
  "generated_at": "2024-04-15T10:30:00Z"
}
```

### Save Objections to Campaign
```http
POST /objections/save-for-campaign
Content-Type: application/json

{
  "campaign_id": 1,
  "objections": [
    { "objection": "...", "response": "...", ... }
  ]
}
```

**Response:**
```json
{
  "campaign_id": 1,
  "objections_saved": 3,
  "objections": [
    {
      "id": 1,
      "objection": "That's too expensive",
      "likelihood": 82,
      "response": "..."
    }
  ]
}
```

### Get Campaign Objections
```http
GET /objections/campaign/{campaign_id}
```

**Response:**
```json
{
  "campaign_id": 1,
  "total_objections": 3,
  "objections": [
    {
      "id": 1,
      "objection": "That's too expensive",
      "likelihood": 82,
      "response": "...",
      "alternatives": ["...", "..."]
    }
  ]
}
```

## Lead Scoring Dashboard Endpoints

### Get All Leads
```http
GET /dashboard/leads
```

**Response:**
```json
{
  "companies": [
    {
      "id": 1,
      "name": "Acme Corp",
      "industry": "SaaS",
      "opportunity_score": 87,
      "urgency_level": "critical",
      "color_code": "#FF0000",
      "fit_score": 92,
      "decision_maker": "Sarah Chen"
    },
    {
      "id": 2,
      "name": "TechFlow Inc",
      "industry": "FinTech",
      "opportunity_score": 64,
      "urgency_level": "medium",
      "color_code": "#FFFF00",
      "fit_score": 71,
      "decision_maker": "John Smith"
    }
  ],
  "total_companies": 45,
  "high_priority_count": 12,
  "avg_opportunity_score": 72.3
}
```

### Update Lead Score
```http
PUT /dashboard/update-lead-score
Content-Type: application/json

{
  "company_id": 1,
  "opportunity_score": 90,
  "urgency_level": "critical"
}
```

**Response:**
```json
{
  "company_id": 1,
  "opportunity_score": 90,
  "urgency_level": "critical",
  "message": "✅ Lead score updated"
}
```

## Follow-up Timeline Endpoints

### Generate Timeline
```http
POST /followup/generate-timeline
Content-Type: application/json

{
  "campaign_id": 1,
  "industry": "saas",
  "initial_send_date": "2024-04-15T09:00:00"
}
```

**Response:**
```json
{
  "campaign_id": 1,
  "industry": "saas",
  "initial_send_date": "2024-04-15T09:00:00",
  "followups": [
    {
      "id": 1,
      "sequence": 1,
      "suggested_date": "2024-04-16T09:00:00",
      "days_from_initial": 1,
      "rationale": "Initial outreach"
    },
    {
      "id": 2,
      "sequence": 2,
      "suggested_date": "2024-04-19T09:00:00",
      "days_from_initial": 4,
      "rationale": "Re-engagement after initial contact"
    },
    {
      "id": 3,
      "sequence": 3,
      "suggested_date": "2024-04-23T09:00:00",
      "days_from_initial": 8,
      "rationale": "Persistence window (peak response time)"
    },
    {
      "id": 4,
      "sequence": 4,
      "suggested_date": "2024-04-30T09:00:00",
      "days_from_initial": 15,
      "rationale": "Final push before moving on"
    }
  ],
  "total_followups": 4
}
```

### Schedule to Calendar
```http
POST /followup/schedule-to-calendar
Content-Type: application/json

{
  "campaign_id": 1,
  "followup_ids": [1, 2, 3, 4]
}
```

**Response:**
```json
{
  "campaign_id": 1,
  "scheduled_count": 4,
  "scheduled_followups": [
    {
      "followup_id": 1,
      "calendar_event_id": "abc123xyz",
      "status": "scheduled"
    }
  ]
}
```

## Export Endpoints

### Save to Database
```http
POST /export/save-to-database
Content-Type: application/json

{
  "campaign_id": 1,
  "company": "Acme Corp",
  "goal": "Sell enterprise software",
  "analysis": { "key": "value" },
  "emails": [
    {
      "subject": "Email subject",
      "body": "Email body",
      "confidence_score": 78,
      "personalization_score": 8,
      "feedback": {}
    }
  ],
  "objections": [
    {
      "objection": "...",
      "response": "...",
      "likelihood_percentage": 82
    }
  ]
}
```

**Response:**
```json
{
  "status": "saved",
  "company_id": 1,
  "campaign_id": 1,
  "emails_saved": 3,
  "objections_saved": 3,
  "message": "✅ Campaign data saved to database"
}
```

### Export to Notion
```http
POST /export/to-notion
Content-Type: application/json

{
  "campaign_id": 1,
  "notion_database_id": "abc123def456abc123def456abc123de",
  "include_emails": true,
  "include_objections": true
}
```

**Response:**
```json
{
  "status": "exported",
  "notion_page_id": "xyz789xyz789xyz789xyz789xyz789xy",
  "campaign_id": 1,
  "message": "✅ Campaign exported to Notion"
}
```

### Export to Google Docs
```http
POST /export/to-google-docs
Content-Type: application/json

{
  "campaign_id": 1,
  "include_emails": true,
  "include_objections": true
}
```

**Response:**
```json
{
  "status": "exported",
  "google_doc_id": "1YYY-ZZZ-BBB",
  "campaign_id": 1,
  "google_docs_url": "https://docs.google.com/document/d/1YYY-ZZZ-BBB/edit",
  "message": "✅ Campaign exported to Google Docs"
}
```

## Error Responses

### 404 Not Found
```json
{
  "detail": "Campaign not found"
}
```

### 401 Unauthorized
```json
{
  "detail": "Gmail authentication failed"
}
```

### 400 Bad Request
```json
{
  "detail": "Notion API not configured"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Error message describing what went wrong"
}
```

## Implementation Examples

### React Hook for Quality Review
```javascript
const useEmailQualityReview = () => {
  const [scores, setScores] = useState(null)
  const [loading, setLoading] = useState(false)

  const reviewEmail = async (subject, body, company) => {
    setLoading(true)
    try {
      const response = await fetch('/api/quality/review-email', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email_subject: subject, email_body: body, company })
      })
      const data = await response.json()
      setScores(data)
    } finally {
      setLoading(false)
    }
  }

  return { scores, loading, reviewEmail }
}
```

### Python Request for Objection Generation
```python
import requests

def generate_objections(company, goal, analysis=None):
    response = requests.post(
        'http://localhost:8000/api/objections/generate',
        json={
            'company': company,
            'goal': goal,
            'analysis': analysis or {}
        }
    )
    return response.json()

objections = generate_objections(
    'Acme Corp',
    'Sell enterprise software',
    {'market_share': 0.15}
)
```

## Rate Limiting & Best Practices

- Batch quality reviews when possible
- Cache lead scoring results (refresh every hour)
- Use follow-up timeline generation once per campaign
- Export operations should be user-initiated
- Store API responses in local state to reduce calls

## Troubleshooting

**Q: Notion export fails**
- Check NOTION_API_KEY is set
- Verify database ID is correct (copy from Notion URL)
- Ensure API key has database access

**Q: Google Docs won't open**
- Verify OAuth2 credentials are configured
- Check user has Google account active
- Allow pop-ups in browser settings

**Q: Quality scores are low**
- Review feedback for specific issues
- Use recommendations to improve
- Re-score after revisions
