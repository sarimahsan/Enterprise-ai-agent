# 🚀 API Keys Setup Guide

Everything is now ready - you only need to add API keys!

## Quick Start (< 5 minutes)

### 1. Copy the .env template
```bash
cp .env.example .env
```

### 2. Add your REQUIRED API keys (minimum setup)
```bash
# Edit .env and add these:
GROQ_API_KEY=your_groq_key
TAVILY_API_KEY=your_tavily_key
```

### 3. Start the backend
```bash
cd backend
source ../venv/bin/activate
python3 main.py
```

**That's it!** Your system is now working with mock data for all other integrations.

---

## Adding Integrations One by One

### ✅ Already Built & Ready
- ✓ **Apollo.io** (lead discovery) - add `APOLLO_API_KEY`
- ✓ **SendGrid** (email sending) - add `SENDGRID_API_KEY`
- ✓ **Google Calendar** (meeting booking) - add credentials file
- ✓ **Twilio** (SMS/voice) - add `TWILIO_*` keys
- ✓ **LinkedIn** (messaging) - add `LINKEDIN_*` keys
- ✓ **HubSpot** (CRM) - add `HUBSPOT_API_KEY`

### How It Works

**Without API Key:** All integrations return mock/demo data
**With API Key:** Real APIs are called automatically

No code changes needed - just add the key and it works!

---

## Phase 1 Priority (This Week)

Add these 3 to go live:

### 1️⃣ Apollo.io (Find Real Leads)
**Time:** 5 minutes  
**Cost:** Free tier available ($0-500/month)

1. Go to https://apollo.io/developers
2. Sign up and get API key
3. Add to `.env`:
```env
APOLLO_API_KEY=your_apollo_key
```

**Test it:**
```bash
# The next API call will find real leads from Apollo
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

### 2️⃣ SendGrid (Send Real Emails)
**Time:** 5 minutes  
**Cost:** Free tier: 100 emails/day

1. Go to https://sendgrid.com
2. Sign up and create API key
3. Add to `.env`:
```env
SENDGRID_API_KEY=your_sendgrid_key
SENDGRID_FROM_EMAIL=campaigns@yourcompany.com
```

**Test it:**
```bash
curl -X POST http://localhost:8000/api/campaigns/execute \
  -H "Content-Type: application/json" \
  -d '{
    "campaign_name": "Salesforce Outreach",
    "target_company": "Acme Corp",
    "value_prop": "Sales automation",
    "tone": "professional"
  }'
```

---

### 3️⃣ Google Calendar (Book Real Meetings)
**Time:** 10 minutes  
**Cost:** Free (Google Workspace)

1. **Enable Google Calendar API:**
   - Go to https://console.cloud.google.com
   - Search "Google Calendar API"
   - Click "Enable"

2. **Create Service Account:**
   - In left sidebar: "Service Accounts"
   - Click "Create Service Account"
   - Name: "Flowforge"
   - Go to Keys tab → Add Key → JSON
   - Save as `backend/config/google-credentials.json`

3. **Share Calendar:**
   - In Google Calendar, click settings (⚙️)
   - Go to "Share with specific people or groups"
   - Add the service account email
   - Make them an Editor

4. **Add to `.env`:**
```env
GOOGLE_CALENDAR_CREDENTIALS_PATH=./config/google-credentials.json
GOOGLE_CALENDAR_EMAIL=your-email@gmail.com
```

**Test it:**
```bash
curl -X GET http://localhost:8000/api/meetings/available-slots
```

---

## After Phase 1 (Next Week)

Once email + lead finding work:

### 4️⃣ LinkedIn (Find + Message Prospects)
```env
LINKEDIN_API_KEY=your_linkedin_key
LINKEDIN_OAUTH_TOKEN=your_oauth_token
```

### 5️⃣ Twilio (SMS + Voice Calls)
```env
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=+1234567890
```

### 6️⃣ HubSpot (CRM Sync)
```env
HUBSPOT_API_KEY=your_hubspot_key
```

---

## How the System Gracefully Handles Missing Keys

**Example: Calling Apollo without API key**

```python
# In lead_service.py, when you call:
apollo_contacts = await apollo.search_people(company_name="Salesforce")

# If API_KEY = "" (empty):
# Returns mock data with 10 demo leads
# "contact1@salesforce.com", "contact2@salesforce.com", etc.

# If API_KEY = "valid_key":
# Calls real Apollo API
# Returns 50 actual leads from Salesforce
```

**Zero code changes** - it just works!

---

## Troubleshooting

### "ModuleNotFoundError"
```bash
# Make sure you're in the right directory
cd backend
source ../venv/bin/activate
python3 main.py
```

### API key not working
1. Check `.env` file path (should be in `backend/`)
2. Verify key is correct (copy-paste from provider)
3. Check environment loading:
```python
from core.config import settings
print(settings.APOLLO_API_KEY)  # Should show your key (first 10 chars visible)
```

### Google Calendar credentials error
- Make sure JSON file is in `backend/config/Google-credentials.json`
- Check file path matches `GOOGLE_CALENDAR_CREDENTIALS_PATH`

---

## Your Timeline

| Phase | Week | Status | API Keys Needed |
|-------|------|--------|-----------------|
| Core Setup | This Week | ✅ Full scaffolding done | GROQ, TAVILY |
| **Phase 1 MVP** | **This Week** | **Start here** | + Apollo, SendGrid, Google Calendar |
| Phase 2 Prep | Next Week | Awaiting integrations | + Twilio, LinkedIn, HubSpot |
| Production | 2 Weeks | Full system | All keys + DB migration |

---

## You're All Set! 🎉

1. Add your API keys to `.env`
2. Run `python3 main.py`
3. Test endpoints at `http://localhost:8000`
4. Frontend at `http://localhost:5173`

**Everything else is automated.** 🚀

Have questions? Check the integration docs in each service file - they have detailed comments on what each API does.
