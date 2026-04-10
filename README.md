# 🚀 FlowForge AI - Enterprise Sales Automation Platform

> **Intelligent AI-powered sales automation platform that generates personalized email campaigns, scores leads, handles objections, and tracks analytics — all with a beautiful, professional UI.**

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-Production%20Ready-brightgreen.svg)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Screenshots](#screenshots)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Environment Setup](#environment-setup)
- [Running Locally](#running-locally)
- [Docker Deployment](#docker-deployment)
- [API Documentation](#api-documentation)
- [Features in Detail](#features-in-detail)
- [Database Schema](#database-schema)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

**FlowForge AI** is an enterprise-grade sales automation platform that leverages artificial intelligence to help sales teams:

- 🤖 **Generate** intelligent, personalized email campaigns
- 📊 **Score** leads based on opportunity potential
- 💬 **Pre-handle** objections with AI-generated responses
- 📈 **Track** campaign performance with comprehensive analytics
- 📧 **Manage** email sequences and follow-ups
- 🔗 **Integrate** with Gmail, LinkedIn, and external data sources
- 📱 **Export** campaigns as professional PDF reports

Built with modern web technologies and designed for scalability, FlowForge AI transforms cold outreach into a data-driven, intelligent process.

---

## ✨ Key Features

### 🎨 Campaign Generation
- **AI-Powered Email Writer** - Generate highly personalized email sequences
- **Multi-Variant Testing** - Create A/B variants (aggressive vs. soft approach)
- **Company Research** - Automatic company analysis and research
- **Personalization Engine** - Dynamic personalization based on prospect data

### 📊 Analytics & Insights
- **Real-time Dashboard** - Track campaign performance live
- **Email Tracking** - Monitor opens, clicks, and engagement
- **Lead Scoring** - Visual dashboard with color-coded urgency levels
- **Performance Metrics** - 15+ analytics metrics per campaign
- **Conversion Tracking** - End-to-end funnel analysis

### 🤖 AI Agents
- **Quality Assurance Agent** - Scores emails 0-100 with specific feedback
- **Objection Handler Agent** - Pre-generates responses to likely objections
- **Research Agent** - Deep research on companies and prospects
- **Analytics Agent** - Advanced analytics and insights generation
- **Variant Agent** - Creates A/B test variations

### 💬 Objection Handling
- **3 Most Likely Objections** - AI-identified top objections with likelihood scores
- **Multiple Response Approaches** - Pre-written responses for each objection
- **Alternative Fallbacks** - 2 backup responses per objection
- **Trigger Identification** - Common objection triggers listed

### 📧 Email Management
- **Gmail Integration** - Native Gmail integration with OAuth2
- **Email History** - Complete email tracking and history
- **Template Management** - Save and reuse email templates
- **Follow-up Automation** - Scheduled follow-up sequences
- **Email Status Tracking** - Draft, sent, opened, clicked states

### 📈 Lead Management
- **Lead Scoring Dashboard** - Visual grid of all companies with scores
- **Color-Coded Urgency** - Red (urgent) → Yellow (medium) → Green (low priority)
- **Opportunity Levels** - Scored 0-100 based on fit and timing
- **LinkedIn Integration** - Direct LinkedIn outreach capabilities
- **Lead Database** - Complete prospect and company database

### 📱 Export & Reporting
- **PDF Export** - Professional PDF reports with charts and metrics
- **Campaign Summary** - Complete campaign details and results
- **Email Analytics** - Detailed email-level performance
- **Data Export** - Export campaigns for external use

### 🎨 Modern UI/UX
- **Professional Dark Theme** - Pitch black background with glass morphism
- **Responsive Design** - Works on desktop, tablet, and mobile
- **Fixed Sidebar Navigation** - 7-tab navigation with active states
- **Real-time Agent Logs** - Terminal-style agent activity viewer
- **Intuitive Dashboard** - All key metrics at a glance

---

## 📸 Screenshots

### 1. Campaign Generator Dashboard
```
[Screenshot Placeholder: Main dashboard with campaign form]
- Company name input
- Sales goal input
- Campaign generation button
- Loading animation with AI spinner
```

### 2. Generated Emails Display
```
[Screenshot Placeholder: Email sequence view]
- Email 1 (Day 0)
- Email 2 (Day 3)
- Email 3 (Day 7)
- Follow-up options
```

### 3. Email Quality Review
```
[Screenshot Placeholder: Quality scores breakdown]
- Overall score: 78/100
- Subject line quality
- Personalization score
- Body quality
- CTA effectiveness
- Issues and recommendations
```

### 4. Objection Handler
```
[Screenshot Placeholder: Objection cards]
- Objection 1: "That's too expensive" (82% likely)
- Objection 2: "We already have something" (65% likely)
- Objection 3: "Let me think about it" (58% likely)
- With expandable response cards
```

### 5. Email Variants (A/B Testing)
```
[Screenshot Placeholder: Side-by-side variant comparison]
- Variant A: Aggressive approach
- Variant B: Soft approach
- Performance metrics
- Toggle to switch between variants
```

### 6. Lead Scoring Dashboard
```
[Screenshot Placeholder: Grid of company cards]
- Company name and industry
- Opportunity score (0-100)
- Color coding by urgency
- Quick action buttons
- Filter and sort options
```

### 7. Campaign Analytics
```
[Screenshot Placeholder: Analytics dashboard with charts]
- Line chart: Opens over time
- Bar chart: Email performance
- Pie chart: Engagement breakdown
- Stats: Open rate, Click rate, Reply rate
- Conversion funnel
```

### 8. Email Management Panel
```
[Screenshot Placeholder: Email history view]
- Email list with status badges
- Recipient, subject, date
- Opens, clicks, replies indicators
- Gmail sync status
```

### 9. LinkedIn Outreach
```
[Screenshot Placeholder: LinkedIn integration screen]
- Message template
- Recipient list
- Send schedule
- Connection requests tracking
```

### 10. Terminal-Style Agent Activity Log
```
[Screenshot Placeholder: Agent activity viewer]
- Black terminal background
- Green text output
- Real-time event logging
- Color-coded messages (✅ success, ❌ error)
- Event counter
```

### 11. PDF Export
```
[Screenshot Placeholder: Generated PDF preview]
- Campaign summary
- Email sequences
- Analytics charts
- Professional formatting
- Export quality
```

### 12. Professional Dark UI
```
[Screenshot Placeholder: Full app interface]
- Pitch black background
- Glass morphism effects
- Sidebar navigation
- Responsive layout
- Header with Gmail status
```

---

## 🛠 Tech Stack

### Frontend
| Technology | Version | Purpose |
|-----------|---------|---------|
| **React** | 19.2.4 | UI framework |
| **Vite** | 8.0.1 | Build tool & dev server |
| **Tailwind CSS** | 4.2.2 | Styling & responsive design |
| **Lucide React** | 1.7.0 | Icon library |
| **Recharts** | 3.8.1 | Charts & analytics |
| **jsPDF** | 4.2.1 | PDF generation |
| **html2canvas** | 1.4.1 | HTML to image conversion |

### Backend
| Technology | Version | Purpose |
|-----------|---------|---------|
| **FastAPI** | 0.111.0+ | Web framework |
| **Uvicorn** | 0.30.0+ | ASGI server |
| **SQLAlchemy** | 2.0.0+ | ORM |
| **SQLModel** | 0.0.14 | SQL database model |
| **Pydantic** | 2.7.0+ | Data validation |
| **LangChain** | 0.0.300+ | LLM orchestration |
| **LangChain Groq** | 0.0.1+ | Groq LLM integration |
| **Tavily** | 0.5.0+ | Web search API |
| **Google Auth** | 2.25.0+ | Gmail OAuth |
| **psycopg2** | 2.9.0+ | PostgreSQL driver |

### Databases
| Technology | Version | Purpose |
|-----------|---------|---------|
| **PostgreSQL** | 15 | Primary database |
| **SQLite** | Built-in | Local development |

### External Services
- **Gmail API** - Email sending and tracking
- **Google OAuth 2.0** - Authentication
- **OpenAI API** - LLM for content generation
- **Groq API** - Fast LLM inference
- **Tavily API** - Web search and research
- **LinkedIn API** - Outreach integration

### DevOps & Deployment
| Technology | Version | Purpose |
|-----------|---------|---------|
| **Docker** | Latest | Containerization |
| **Docker Compose** | 3.8+ | Orchestration |
| **Nginx** | Alpine | Reverse proxy |
| **Python** | 3.11 | Backend runtime |
| **Node.js** | 18 | Frontend runtime |

---

## 📦 Prerequisites

Before you begin, ensure you have the following installed:

### Required
- **Node.js** (v18 or higher) - [Download](https://nodejs.org/)
- **Python** (v3.11 or higher) - [Download](https://www.python.org/)
- **Git** - [Download](https://git-scm.com/)

### Optional (for Docker deployment)
- **Docker** (v20.10 or higher) - [Download](https://www.docker.com/)
- **Docker Compose** (v3.8 or higher)

### System Requirements
- **RAM**: Minimum 4GB (8GB recommended)
- **Disk Space**: Minimum 5GB
- **OS**: Windows, macOS, or Linux
- **Internet Connection**: Required for API integrations

---

## 📥 Installation

### Step 1: Clone the Repository

```bash
# Clone repository
git clone https://github.com/yourusername/flowforge-ai.git
cd flowforge-ai

# Or download as ZIP
# Unzip and navigate to directory
```

### Step 2: Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Return to project root
cd ..
```

### Step 3: Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Return to project root
cd ..
```

### Step 4: Environment Variables

```bash
# Copy environment template
cp .env.example .env

# Edit with your values
# Windows: notepad .env
# macOS/Linux: nano .env
```

---

## 🔑 Environment Setup

Create a `.env` file in the project root and configure the following API keys:

### Database Configuration
```env
# PostgreSQL (optional - uses SQLite by default)
DATABASE_URL=postgresql://user:password@localhost:5432/flowforge_db
DB_USER=flowforge
DB_PASSWORD=your_secure_password
DB_NAME=flowforge_db
DB_PORT=5432
```

### Gmail Integration

**Step 1: Create Google OAuth Credentials**

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project: "FlowForge AI"
3. Enable APIs:
   - Gmail API
   - Google Drive API
   - Google Calendar API
4. Create OAuth 2.0 credentials (Desktop App):
   - Authorized redirect URI: `http://localhost:8000/auth/callback`
5. Download credentials as JSON

**Step 2: Add to Environment**

```env
# Gmail OAuth
GMAIL_CLIENT_ID=xxxxx-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx.apps.googleusercontent.com
GMAIL_CLIENT_SECRET=GOCSPX-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
GOOGLE_REDIRECT_URI=http://localhost:8000/auth/callback
```

### OpenAI API

**Step 1: Get API Key**

1. Visit [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in
3. Navigate to API Keys
4. Create new secret key
5. Copy the key

**Step 2: Add to Environment**

```env
# OpenAI
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
OPENAI_MODEL=gpt-4  # or gpt-3.5-turbo for faster, cheaper responses
```

### Groq API (Alternative LLM - Faster & Free)

**Step 1: Get API Key**

1. Visit [Groq Console](https://console.groq.com/)
2. Sign up or log in
3. Create API key
4. Copy the key

**Step 2: Add to Environment**

```env
# Groq (for faster, free LLM inference)
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
GROQ_MODEL=mixtral-8x7b-32768  # or other available models
```

### Tavily Search API

**Step 1: Get API Key**

1. Visit [Tavily AI](https://tavily.com/)
2. Sign up
3. Get API key from dashboard
4. Copy the key

**Step 2: Add to Environment**

```env
# Tavily Search
TAVILY_API_KEY=tvly-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### LinkedIn Integration (Optional)

```env
# LinkedIn
LINKEDIN_CLIENT_ID=your_linkedin_client_id
LINKEDIN_CLIENT_SECRET=your_linkedin_client_secret
LINKEDIN_ACCESS_TOKEN=your_linkedin_access_token
```

### Application Settings

```env
# Backend
DEBUG=true  # Set to false in production
SECRET_KEY=your-super-secret-key-change-in-production
CORS_ORIGINS=http://localhost:3000,http://localhost:5174

# Frontend
VITE_API_URL=http://localhost:8000/api
NODE_ENV=development

# Server
ENVIRONMENT=development  # development, staging, production
```

### Complete `.env` Example

```env
# === DATABASE ===
DATABASE_URL=postgresql://flowforge:password@localhost:5432/flowforge_db
DB_USER=flowforge
DB_PASSWORD=secure_password_here
DB_NAME=flowforge_db
DB_PORT=5432

# === GMAIL ===
GMAIL_CLIENT_ID=xxxx-xxxx.apps.googleusercontent.com
GMAIL_CLIENT_SECRET=GOCSPX-xxxxx
GOOGLE_REDIRECT_URI=http://localhost:8000/auth/callback

# === LLM (One of below)===
OPENAI_API_KEY=sk-proj-xxxxx
OPENAI_MODEL=gpt-4
# OR
GROQ_API_KEY=gsk_xxxxx
GROQ_MODEL=mixtral-8x7b-32768

# === SEARCH ===
TAVILY_API_KEY=tvly-xxxxx

# === LINKEDIN ===
LINKEDIN_CLIENT_ID=xxxxx
LINKEDIN_CLIENT_SECRET=xxxxx
LINKEDIN_ACCESS_TOKEN=xxxxx

# === APPLICATION ===
DEBUG=true
SECRET_KEY=your-secret-key-here
CORS_ORIGINS=http://localhost:3000,http://localhost:5174
VITE_API_URL=http://localhost:8000/api
NODE_ENV=development
ENVIRONMENT=development
```

---

## 🚀 Running Locally

### Option 1: Manual Setup (Development)

#### Terminal 1: Backend

```bash
# Navigate to backend
cd backend

# Activate virtual environment
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# Start FastAPI server
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Server will be available at: http://localhost:8000
# API docs at: http://localhost:8000/docs
```

#### Terminal 2: Frontend

```bash
# Navigate to frontend
cd frontend

# Start development server
npm run dev

# Application will be available at: http://localhost:5174
```

#### Verify Services

```bash
# Check backend health
curl http://localhost:8000/api/health

# Check frontend
open http://localhost:5174
# or navigate to http://localhost:5174 in browser
```

### Option 2: Docker Deployment (Production)

```bash
# Copy environment file
cp .env.example .env

# Edit with your configuration
nano .env  # or edit .env with your editor

# Start all services
# Linux/macOS
./deploy.sh up

# Windows
deploy.bat up

# Verify services running
./deploy.sh status

# Access application
# Frontend: http://localhost
# API: http://localhost/api
# Database: localhost:5432
```

See [DOCKER_DEPLOYMENT.md](./DOCKER_DEPLOYMENT.md) for detailed Docker instructions.

---

## 🐳 Docker Deployment

### Quick Start

```bash
# 1. Setup environment
cp .env.example .env
nano .env  # Edit with your configuration

# 2. Start services
./deploy.sh up    # Linux/macOS
deploy.bat up     # Windows

# 3. Verify running
./deploy.sh status

# 4. Access application
# Frontend: http://localhost
# API: http://localhost/api

# 5. View logs
./deploy.sh logs backend

# 6. Stop services
./deploy.sh down
```

### Useful Docker Commands

```bash
# View logs for specific service
./deploy.sh logs backend      # Backend logs
./deploy.sh logs frontend     # Frontend logs
./deploy.sh logs db           # Database logs

# SSH into containers
./deploy.sh shell-backend     # Backend shell
./deploy.sh shell-db          # Database shell

# Rebuild images
./deploy.sh rebuild           # Full rebuild

# Clean everything
./deploy.sh clean             # Remove all containers/volumes
```

See [DOCKER_DEPLOYMENT.md](./DOCKER_DEPLOYMENT.md) for complete Docker documentation.

---

## 📚 API Documentation

### Base URL
```
http://localhost:8000/api
```

### Authentication
All endpoints are currently open. In production, add JWT authentication.

### Campaign Endpoints

#### Generate Campaign
```http
POST /api/campaigns/generate
Content-Type: application/json

{
  "company_name": "Acme Corp",
  "goal": "Schedule a demo with VP of Sales",
  "prospect_info": {
    "name": "Sarah Johnson",
    "title": "VP of Sales",
    "company": "Acme Corp",
    "industry": "SaaS"
  }
}

Response:
{
  "campaign_id": "uuid-here",
  "emails": [
    {
      "email_id": "uuid-here",
      "subject": "Re: Acme's Sales Growth Strategy",
      "body": "Hi Sarah...",
      "day": 0
    }
  ],
  "analysis": {...}
}
```

#### Get Campaign
```http
GET /api/campaigns/{campaign_id}

Response:
{
  "campaign_id": "uuid",
  "company_name": "Acme Corp",
  "goal": "Schedule a demo",
  "emails": [...],
  "analytics": {...},
  "created_at": "2024-01-15T10:30:00Z"
}
```

#### List Campaigns
```http
GET /api/campaigns

Response:
{
  "campaigns": [
    {
      "campaign_id": "uuid",
      "company_name": "Acme Corp",
      "goal": "Schedule demo",
      "email_count": 3,
      "created_at": "2024-01-15T10:30:00Z"
    }
  ],
  "total": 15,
  "page": 1
}
```

### Email Quality Review

#### Review Single Email
```http
POST /api/quality/review-email
Content-Type: application/json

{
  "email_subject": "Re: Partnership Opportunity",
  "email_body": "Hi Sarah, I noticed Acme...",
  "company": "Acme Corp",
  "prospect_info": {
    "title": "VP Sales",
    "industry": "SaaS"
  }
}

Response:
{
  "overall_score": 78,
  "subject_score": 7,
  "body_score": 8,
  "personalization_score": 6,
  "cta_score": 8,
  "issues": [
    "Subject line is too generic",
    "Could reference Series B funding"
  ],
  "recommendations": [
    "Make subject line more specific to company",
    "Add more personalization details"
  ]
}
```

### Objection Handling

#### Generate Objections
```http
POST /api/objections/generate
Content-Type: application/json

{
  "company": "Acme Corp",
  "industry": "SaaS",
  "prospect_title": "VP Sales",
  "emails": ["Email 1...", "Email 2..."]
}

Response:
{
  "objections": [
    {
      "objection": "That's too expensive",
      "likelihood": 82,
      "approach": "value-focused",
      "primary_response": "I understand budget is tight...",
      "alternatives": [
        "Many CFOs see ROI in 90 days...",
        "Most save $50K annually..."
      ],
      "triggers": ["Budget cuts", "Failed fundraise"]
    }
  ]
}
```

### Email Variants

#### Create Variant
```http
POST /api/emails/{email_id}/variants
Content-Type: application/json

{
  "approach": "aggressive",
  "subject": "Alert: You're Missing Out",
  "body": "Sarah, your competitors..."
}

Response:
{
  "variant_id": "uuid",
  "email_id": "uuid",
  "approach": "aggressive",
  "variant_letter": "B"
}
```

### Analytics

#### Get Campaign Analytics
```http
GET /api/analytics/campaign/{campaign_id}

Response:
{
  "campaign_id": "uuid",
  "total_emails": 3,
  "total_sends": 45,
  "total_opens": 18,
  "open_rate": 40,
  "total_clicks": 9,
  "click_rate": 50,
  "total_replies": 3,
  "reply_rate": 33,
  "conversion_rate": 6.7,
  "metrics": {
    "avg_open_time": "2 hours",
    "peak_open_time": "9:00 AM",
    "best_performing_email": 2,
    "worst_performing_email": 1
  }
}
```

### Health Check

#### Server Health
```http
GET /api/health

Response:
{
  "status": "ok",
  "database": "connected",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

---

## 🎯 Features in Detail

### 1. Campaign Generation
- Analyzes company and prospect data
- Generates personalized email sequences (typically 3-5 emails)
- Creates follow-up schedules
- Includes social proof and specific company references
- Adapts tone based on prospect profile

### 2. Email Quality Scoring
- Rates emails 0-100 overall
- Breaks down into 5 key metrics:
  - Subject line effectiveness (0-10)
  - Body copy quality (0-10)
  - Personalization level (0-10)
  - Call-to-action strength (0-10)
- Identifies specific issues
- Provides actionable recommendations

### 3. Objection Handling
- Identifies 3 most likely objections
- Calculates likelihood percentage for each
- Provides primary response strategy
- Includes 2 alternative responses
- Suggests optimal approach (empathetic, logical, social_proof, value-focused)
- Lists common triggers for each objection

### 4. Lead Scoring Dashboard
- Visual grid of all companies researched
- Color-coded by urgency (Red/Yellow/Green)
- Scores 0-100 based on:
  - Company industry fit
  - Timing and budget availability
  - Decision-maker accessibility
  - Market opportunity
- Quick action buttons for next steps

### 5. Email Variants (A/B Testing)
- Creates aggressive vs. soft variations
- Tracks performance by variant:
  - Send count
  - Open rate
  - Click rate
  - Reply rate
  - Conversion rate
- Visual comparison interface
- Winner identification (automatic or manual)

### 6. Gmail Integration
- Native Gmail OAuth2 integration
- Send emails directly from application
- Automatic open/click tracking
- Read receipt integration
- Email history and threading
- Calendar integration for scheduling

### 7. Analytics Dashboard
- Real-time campaign metrics
- 15+ trackable metrics:
  - Send rate
  - Open rate
  - Click rate
  - Reply rate
  - Conversion rate
  - Cost per lead
  - Time to first open
  - Time to first click
  - Time to reply
  - Peak open time
  - Best performing email
  - Engagement by day
  - Device breakdown
  - Link performance
  - Geographic distribution

### 8. PDF Export
- Professional report generation
- Includes:
  - Campaign summary
  - Email sequences
  - Performance analytics
  - Charts and visualizations
  - Company information
  - Prospect details
- Ready to share with stakeholders

### 9. Terminal-Style Agent Logs
- Real-time agent activity display
- Color-coded messages:
  - ✅ Green: Success
  - ❌ Red: Errors
  - 📧 Cyan: Email events
  - ⚡ Yellow: Processing
- CRT scanline effect
- Event counter
- Monospace terminal font

---

## 🗄 Database Schema

### Main Tables

#### Campaigns
```sql
campaigns {
  campaign_id: UUID (PK)
  company_name: VARCHAR(255)
  goal: TEXT
  status: VARCHAR(50) -- active, completed, archived
  analysis: JSONB
  emails: JSONB
  variants: JSONB
  follow_up_schedule: JSONB
  created_at: TIMESTAMP
  updated_at: TIMESTAMP
}
```

#### Emails
```sql
emails {
  email_id: UUID (PK)
  campaign_id: UUID (FK)
  recipient_email: VARCHAR(255)
  subject: TEXT
  body: TEXT
  variant_type: VARCHAR(100)
  quality_score: FLOAT
  status: VARCHAR(50) -- draft, sent, opened, clicked
  sent_at: TIMESTAMP
  opens: INT
  clicks: INT
  created_at: TIMESTAMP
  updated_at: TIMESTAMP
}
```

#### Email Variants
```sql
email_variants {
  variant_id: UUID (PK)
  email_id: UUID (FK)
  campaign_id: UUID (FK)
  approach: VARCHAR(100) -- aggressive, soft
  subject_variant: TEXT
  body_variant: TEXT
  send_count: INT
  open_count: INT
  click_count: INT
  reply_count: INT
  conversion_count: INT
  open_rate: FLOAT
  click_rate: FLOAT
  reply_rate: FLOAT
  created_at: TIMESTAMP
}
```

#### Objections
```sql
objections {
  objection_id: UUID (PK)
  campaign_id: UUID (FK)
  objection_text: TEXT
  response_approach: VARCHAR(100)
  response_text: TEXT
  alternatives: JSONB
  likelihood: INT
  created_at: TIMESTAMP
}
```

#### Analytics
```sql
analytics {
  analytics_id: UUID (PK)
  campaign_id: UUID (FK)
  metric_name: VARCHAR(100)
  metric_value: FLOAT
  recorded_at: TIMESTAMP
}
```

---

## 📁 Project Structure

```
flowforge-ai/
├── README.md                      # This file
├── DOCKER_DEPLOYMENT.md           # Docker setup guide
├── DOCKER_FILES_SUMMARY.md        # Docker file documentation
├── DOCKER_SETUP.md               # Docker quick reference
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment template
├── docker-compose.yml            # Docker Compose config
├── init-db.sql                   # Database initialization
├── nginx.conf                    # Nginx configuration
├── deploy.sh                     # Linux/macOS deployment script
├── deploy.bat                    # Windows deployment script
│
├── backend/
│   ├── main.py                   # FastAPI app entry point
│   ├── requirements.txt          # Python packages
│   ├── Dockerfile               # Backend containerization
│   ├── .dockerignore            # Docker exclusions
│   │
│   ├── core/
│   │   ├── config.py            # Configuration management
│   │   └── database.py          # Database setup
│   │
│   ├── api/
│   │   ├── routes.py            # Main API routes
│   │   ├── extended_routes.py   # Additional routes
│   │   └── schema.py            # Pydantic models
│   │
│   ├── agents/
│   │   ├── orchestrator.py      # Agent orchestration
│   │   ├── writer_Agent.py      # Email writer
│   │   ├── qa_agent.py          # Quality assurance
│   │   ├── research_agent.py    # Company research
│   │   ├── analytics_agent.py   # Analytics engine
│   │   └── variant_agent.py     # A/B variant creation
│   │
│   ├── services/
│   │   ├── database_service.py  # Database operations
│   │   ├── gmail_service.py     # Gmail integration
│   │   ├── email_channel.py     # Email channel
│   │   ├── calendar_service.py  # Calendar integration
│   │   ├── linkedin_service.py  # LinkedIn API
│   │   ├── export_service.py    # Export functionality
│   │   └── gmail_service_pro.py # Advanced Gmail
│   │
│   ├── models/
│   │   ├── database_models.py   # SQLModel definitions
│   │   ├── campaign.py          # Campaign model
│   │   ├── email.py             # Email model
│   │   ├── lead.py              # Lead model
│   │   ├── interaction.py       # Interaction model
│   │   ├── deal.py              # Deal model
│   │   └── __init__.py
│   │
│   ├── graph/
│   │   └── workflow.py          # LangChain workflow
│   │
│   └── gmail_*.json             # Gmail credentials (local)
│
├── frontend/
│   ├── package.json             # Node.js dependencies
│   ├── vite.config.js          # Vite configuration
│   ├── tailwind.config.js       # Tailwind CSS config
│   ├── postcss.config.js        # PostCSS configuration
│   ├── eslint.config.js         # ESLint rules
│   ├── index.html               # HTML entry
│   ├── Dockerfile               # Frontend containerization
│   ├── .dockerignore            # Docker exclusions
│   │
│   └── src/
│       ├── main.jsx             # React entry
│       ├── App.jsx              # Main app component
│       ├── App1.jsx             # Alternate app version
│       ├── index.css            # Global styles
│       │
│       └── components/
│           ├── CampaignGenerator.jsx         # Generator UI
│           ├── EmailVariants.jsx             # A/B testing
│           ├── EmailQualityReview.jsx        # Quality scores
│           ├── ObjectionHandler.jsx          # Objection responses
│           ├── LeadScoringDashboard.jsx      # Lead scoring
│           ├── CampaignAnalytics.jsx         # Analytics dashboard
│           ├── EmailManagementPanel.jsx      # Email management
│           ├── EmailStatusTracker.jsx        # Email tracking
│           ├── ExportPanel.jsx               # PDF export
│           ├── AgentActivityLog.jsx          # Agent logs
│           ├── CalendarScheduler.jsx         # Calendar UI
│           ├── LinkedInOutreach.jsx          # LinkedIn UI
│           ├── IntelligenceCards.jsx         # Info cards
│           └── Logo.jsx                      # Brand logo
│
└── nginx/
    └── nginx.conf               # Nginx configuration
```

---

## ⚙️ Configuration

### Backend Configuration (`backend/core/config.py`)

```python
DATABASE_URL = "postgresql://user:pass@localhost/db"
DEBUG = False
SECRET_KEY = "your-secret"
CORS_ORIGINS = ["http://localhost:3000"]
```

### Frontend Configuration (`frontend/vite.config.js`)

```javascript
export default {
  server: {
    port: 5174,
    host: 'localhost'
  },
  build: {
    outDir: 'dist',
    sourcemap: false
  }
}
```

### Database Connection

**PostgreSQL (Production)**
```env
DATABASE_URL=postgresql://flowforge:password@localhost:5432/flowforge_db
```

**SQLite (Development)**
```env
DATABASE_URL=sqlite:///./flowforge.db
```

---

## 🐛 Troubleshooting

### Common Issues

#### Port Already in Use
```bash
# Find process on port 8000
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :8000
kill -9 <PID>

# Or change port in .env
PORT=8001
```

#### Database Connection Error
```bash
# Check PostgreSQL is running
# PostgreSQL should be accessible at localhost:5432

# Test connection
psql -U flowforge -h localhost -d flowforge_db

# Initialize database if needed
python -c "from core.database import init_db; init_db()"
```

#### Gmail Auth Fails
1. Verify `GMAIL_CLIENT_ID` and `GMAIL_CLIENT_SECRET` in `.env`
2. Check redirect URI matches settings: `http://localhost:8000/auth/callback`
3. Go to [Google Cloud Console](https://console.cloud.google.com/)
4. Verify OAuth consent screen is configured
5. Add test user to OAuth consent screen

#### API Shows "Connection Refused"
```bash
# Verify backend running
curl http://localhost:8000/api/health

# Check CORS settings
# Update CORS_ORIGINS in .env if needed
CORS_ORIGINS=http://localhost:5174
```

#### Frontend won't Load
```bash
# Check frontend is running
npm run dev

# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Check port 5174 isn't in use
# Change port in vite.config.js if needed
```

#### Docker Container Won't Start
```bash
# Check logs
docker-compose logs backend

# Rebuild image
docker-compose build --no-cache backend

# Force recreate
docker-compose up -d --force-recreate backend
```

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/flowforge-ai.git
   cd flowforge-ai
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow existing code style
   - Add comments for complex logic
   - Update README if needed

4. **Test your changes**
   ```bash
   # Backend tests
   pytest backend/tests/

   # Frontend tests
   npm test
   ```

5. **Commit with clear messages**
   ```bash
   git commit -m "Add: description of feature"
   ```

6. **Push and create Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```

### Contribution Guidelines
- Follow PEP 8 for Python
- Follow React best practices
- Add unit tests for new features
- Update documentation
- Keep commits atomic and focused

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

```
MIT License

Copyright (c) 2024 FlowForge AI

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

## 🔗 Quick Links

- **GitHub**: [FlowForge AI](https://github.com/yourusername/flowforge-ai)
- **Issues**: [Report a Bug](https://github.com/yourusername/flowforge-ai/issues)
- **Discussions**: [Ask a Question](https://github.com/yourusername/flowforge-ai/discussions)
- **Documentation**: [Full Docs](./docs/)

---

## 👨‍💼 Support

Need help? Here are your options:

1. **Check the Docs**
   - [DOCKER_DEPLOYMENT.md](./DOCKER_DEPLOYMENT.md) - Docker setup
   - [QUICK_START.md](./QUICK_START.md) - Quick start guide
   - [API_INTEGRATION_GUIDE.md](./API_INTEGRATION_GUIDE.md) - API usage

2. **Search Existing Issues**
   - Browse [GitHub Issues](https://github.com/yourusername/flowforge-ai/issues)
   - Check [Discussions](https://github.com/yourusername/flowforge-ai/discussions)

3. **Create an Issue**
   - Include error message and logs
   - Describe steps to reproduce
   - Include environment details

4. **Community Help**
   - Discord: [Join Our Server](#)
   - Twitter: [@FlowForgeAI](#)
   - Email: support@flowforge.ai

---

## 🎉 Acknowledgments

Built with ❤️ using:
- [FastAPI](https://fastapi.tiangolo.com/)
- [React](https://react.dev/)
- [LangChain](https://www.langchain.com/)
- [Tailwind CSS](https://tailwindcss.com/)
- [PostgreSQL](https://www.postgresql.org/)

---

## 📊 Project Stats

- **Language**: Python, JavaScript, React
- **Lines of Code**: 10,000+
- **API Endpoints**: 25+
- **React Components**: 12+
- **Agents**: 5 (Writer, QA, Research, Analytics, Variant)
- **Features**: 20+
- **Database Tables**: 8

---

## 🚀 Roadmap

### Q1 2024
- ✅ Core campaign generation
- ✅ Email quality scoring
- ✅ Lead scoring dashboard
- ✅ Docker deployment

### Q2 2024
- 🔄 Advanced analytics
- 🔄 Team collaboration
- 🔄 Custom integrations
- 🔄 Multi-user support

### Q3 2024
- 📋 CRM integrations (Salesforce, HubSpot)
- 📋 Advanced reporting
- 📋 AI model fine-tuning
- 📋 Mobile app

### Q4 2024
- 📋 Marketplace
- 📋 Enterprise SSO
- 📋 Advanced security
- 📋 Global scaling

---

## 📞 Contact

- **Email**: contact@flowforge.ai
- **Twitter**: [@FlowForgeAI](https://twitter.com)
- **LinkedIn**: [FlowForge AI](https://linkedin.com)
- **Website**: [flowforge.ai](https://flowforge.ai)

---

**Made with 💙 by FlowForge AI Team**

Last Updated: April 2024 | Version: 1.0.0
