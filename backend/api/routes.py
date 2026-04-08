from fastapi import APIRouter, HTTPException
from api.schema import (
    GoalRequest, AgentResponse, SendEmailRequest, 
    SendProfessionalEmailRequest, EmailSendResponse, 
    EmailStats, GmailAuthStatus, BulkEmailRequest,
    ScheduleCampaignRequest, ScheduleFollowupRequest,
    GetMembersRequest, GenerateMessagesRequest, GenerateSingleMessageRequest
)
from graph.workflow import pipeline, AgentState
from services.email_channel import generate_email_templates, send_campaign_email, create_follow_up_schedule
from services.gmail_service_pro import get_gmail_service
from datetime import datetime

router = APIRouter()

# ============ CAMPAIGN ENDPOINTS ============
@router.post("/run", response_model=AgentResponse)
async def run_agent(request: GoalRequest):
    """Run the AI agent campaign generator"""
    result = pipeline.invoke(AgentState(
        company=request.company,
        goal=request.goal,
        tasks=[],
        research={},
        analysis={},
        emails={},
        email_templates={},
        variants={},
        logs=[],
        analytics={},
        follow_up_schedule={}
    ))
    
    # Generate professional email templates
    email_templates = generate_email_templates(
        request.company,
        result["analysis"],
        result["emails"]
    )
    
    # Create follow-up schedule
    follow_up_schedule = create_follow_up_schedule(
        request.company,
        result["analysis"].get("decision_maker", "Team")
    )
    
    return AgentResponse(
        emails=result["emails"],
        email_templates=email_templates,
        analysis=result["analysis"],
        variants=result["variants"],
        logs=result["logs"],
        tasks=result["tasks"],
        analytics=result["analytics"],
        follow_up_schedule=follow_up_schedule
    )

# ============ EMAIL SENDING ENDPOINTS ============
@router.post("/send-email", response_model=EmailSendResponse)
async def send_email(request: SendEmailRequest):
    """Send a professional email via Gmail with tracking"""
    try:
        gmail = get_gmail_service()
        
        if not gmail.authenticate():
            raise HTTPException(status_code=401, detail="Gmail authentication failed")
        
        success, message, message_id = gmail.send_email(
            to=request.to_email,
            subject=request.subject,
            html_body=request.html_body,
            cc=request.cc,
            bcc=request.bcc,
            priority=request.priority.value
        )
        
        return EmailSendResponse(
            success=success,
            message=message,
            email_id=f"{request.to_email}_{datetime.now().timestamp()}",
            message_id=message_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/send-professional-email", response_model=EmailSendResponse)
async def send_professional_email(request: SendProfessionalEmailRequest):
    """Send a professional formatted email with company branding"""
    try:
        gmail = get_gmail_service()
        
        if not gmail.authenticate():
            raise HTTPException(status_code=401, detail="Gmail authentication failed")
        
        success, message, message_id = gmail.send_professional_email(
            to=request.to_email,
            company=request.company,
            subject_line=request.subject_line,
            body_content=request.body_content,
            decision_maker=request.decision_maker
        )
        
        return EmailSendResponse(
            success=success,
            message=message,
            email_id=f"{request.to_email}_{datetime.now().timestamp()}",
            message_id=message_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============ EMAIL STATUS & TRACKING ============
@router.get("/email-stats", response_model=EmailStats)
async def get_email_statistics():
    """Get email sending statistics and status"""
    try:
        gmail = get_gmail_service()
        
        sent = gmail.get_sent_emails()
        pending = gmail.get_pending_emails()
        failed = gmail.get_failed_emails()
        
        total_sent = len(sent)
        success_rate = (total_sent / (total_sent + len(failed)) * 100) if (total_sent + len(failed)) > 0 else 0
        
        return EmailStats(
            total_sent=total_sent,
            pending=len(pending),
            failed=len(failed),
            success_rate=success_rate,
            sent_emails=sent[:10],
            pending_emails=pending[:10],
            failed_emails=failed[:10]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/gmail-auth-status", response_model=GmailAuthStatus)
async def get_gmail_auth_status():
    """Get Gmail authentication status"""
    try:
        gmail = get_gmail_service()
        authenticated = gmail.authenticate()
        
        if authenticated:
            user_info = gmail.get_authenticated_user()
            return GmailAuthStatus(
                is_authenticated=True,
                email=user_info.get("email"),
                message_count=user_info.get("message_count"),
                threads_count=user_info.get("threads"),
                status="✅ Connected to Gmail"
            )
        else:
            return GmailAuthStatus(
                is_authenticated=False,
                status="❌ Not authenticated"
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============ BULK OPERATIONS ============
@router.post("/bulk-send-emails", response_model=dict)
async def bulk_send_emails(request: BulkEmailRequest):
    """Send emails to multiple recipients with tracking"""
    try:
        gmail = get_gmail_service()
        
        if not gmail.authenticate():
            raise HTTPException(status_code=401, detail="Gmail authentication failed")
        
        results = []
        for recipient in request.recipients:
            success, message, msg_id = gmail.send_email(
                to=recipient.get("email"),
                subject=request.subject,
                html_body=request.html_body,
                priority="normal"
            )
            results.append({
                "email": recipient.get("email"),
                "success": success,
                "message": message,
                "message_id": msg_id
            })
        
        sent_count = sum(1 for r in results if r["success"])
        return {
            "total": len(request.recipients),
            "sent": sent_count,
            "failed": len(request.recipients) - sent_count,
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============ HEALTH CHECK ============
@router.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "ok",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

# ============ GOOGLE CALENDAR ENDPOINTS ============
@router.post("/calendar/schedule-campaign")
async def schedule_campaign(request: ScheduleCampaignRequest):
    """Schedule a campaign to send at specific time"""
    try:
        from services.calendar_service import CalendarService
        from datetime import datetime as dt
        
        calendar = CalendarService()
        if not calendar.authenticate():
            raise HTTPException(status_code=401, detail="Calendar authentication failed")
        
        send_datetime = dt.fromisoformat(request.send_time)
        result = calendar.schedule_campaign(request.campaign_name, send_datetime)
        
        if result['success']:
            return {
                "status": "scheduled",
                "campaign": request.campaign_name,
                "scheduled_time": request.send_time,
                "event_id": result.get('event_id'),
                "message": "✅ Campaign scheduled successfully"
            }
        else:
            raise HTTPException(status_code=400, detail=result['error'])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/calendar/schedule-followup")
async def schedule_followup(request: ScheduleFollowupRequest):
    """Schedule a follow-up email for a campaign"""
    try:
        from services.calendar_service import CalendarService
        from datetime import datetime as dt
        
        calendar = CalendarService()
        if not calendar.authenticate():
            raise HTTPException(status_code=401, detail="Calendar authentication failed")
        
        initial_datetime = dt.fromisoformat(request.initial_time)
        result = calendar.schedule_followup(request.campaign_name, initial_datetime, request.followup_days)
        
        if result['success']:
            return {
                "status": "scheduled",
                "campaign": request.campaign_name,
                "followup_date": initial_datetime.isoformat(),
                "followup_days": request.followup_days,
                "event_id": result.get('event_id'),
                "message": f"✅ Follow-up scheduled for {request.followup_days} days later"
            }
        else:
            raise HTTPException(status_code=400, detail=result['error'])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/calendar/available-slots")
async def get_available_slots(start_date: str, num_days: int = 7):
    """Get available calendar slots for scheduling"""
    try:
        from services.calendar_service import CalendarService
        from datetime import datetime as dt
        
        calendar = CalendarService()
        if not calendar.authenticate():
            raise HTTPException(status_code=401, detail="Calendar authentication failed")
        
        start_datetime = dt.fromisoformat(start_date)
        slots = calendar.get_available_slots(start_datetime, num_days)
        
        return {
            "available_slots": slots,
            "total_slots": len(slots),
            "period": f"{num_days} days starting {start_date}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/calendar/auth-status")
async def get_calendar_auth_status():
    """Check Calendar authentication status"""
    try:
        from services.calendar_service import CalendarService
        
        calendar = CalendarService()
        authenticated = calendar.authenticate()
        
        return {
            "authenticated": authenticated,
            "service": "Google Calendar",
            "status": "✅ Connected" if authenticated else "❌ Not connected"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============ LINKEDIN ENDPOINTS ============
@router.post("/linkedin/get-members")
async def get_company_members(request: GetMembersRequest):
    """Get members from a specific company and department"""
    try:
        from services.linkedin_service import LinkedInService
        
        linkedin = LinkedInService()
        members = await linkedin.get_company_members(request.company_name, request.department, request.limit)
        
        return {
            "company": request.company_name,
            "department": request.department or "All",
            "total_found": len(members),
            "members": members,
            "success": True
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/linkedin/generate-messages")
async def generate_outreach_messages(request: GenerateMessagesRequest):
    """Generate personalized LinkedIn message drafts for company members"""
    try:
        from services.linkedin_service import LinkedInService
        
        if not request.company_name:
            raise ValueError("company_name is required")
        
        linkedin = LinkedInService()
        batch = linkedin.generate_outreach_batch(
            company_name=request.company_name,
            department=request.department,
            campaign_topic=request.campaign_topic,
            tone=request.tone,
            limit=request.limit
        )
        
        return batch
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/linkedin/generate-single-message")
async def generate_single_message(request: GenerateSingleMessageRequest):
    """Generate a single personalized message"""
    try:
        from services.linkedin_service import LinkedInService
        
        linkedin = LinkedInService()
        member = {
            "name": request.member_name,
            "title": request.member_title,
            "headline": ""
        }
        
        result = linkedin.generate_message_draft(
            member=member,
            campaign_topic=request.campaign_topic,
            company_name=request.company_name,
            tone=request.tone
        )
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))