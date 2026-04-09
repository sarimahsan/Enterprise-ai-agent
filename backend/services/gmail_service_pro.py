"""
Professional Gmail Service - OAuth2 authentication, email tracking, and sending
Features: Email status tracking, retry logic, professional templates, detailed logging
"""
import os
import base64
import json
from datetime import datetime, timedelta
from typing import Dict, Optional, List, Tuple
from enum import Enum
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Google Libraries
try:
    from google.auth.transport.requests import Request
    from google.oauth2.service_account import Credentials as ServiceAccountCredentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from google.oauth2.credentials import Credentials as UserCredentials
    GOOGLE_INSTALLED = True
except ImportError as e:
    GOOGLE_INSTALLED = False
    print(f"⚠️ Google libraries not installed: {e}")

# ============ ENUMS ============
class EmailStatus(str, Enum):
    """Email lifecycle status"""
    DRAFT = "draft"
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"
    BOUNCED = "bounced"
    READ = "read"
    CLICKED = "clicked"

class EmailPriority(str, Enum):
    """Email priority levels"""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"

# ============ CONSTANTS ============
SCOPES = ['https://www.googleapis.com/auth/gmail.send', 'https://www.googleapis.com/auth/gmail.readonly']

# ============ EMAIL TRACKING ============
class EmailTracker:
    """Tracks email sending status and metadata"""
    def __init__(self, tracking_file: str = "email_tracking.json"):
        self.tracking_file = tracking_file
        self.data = self._load_tracking()
    
    def _load_tracking(self) -> Dict:
        """Load tracking data from file"""
        if os.path.exists(self.tracking_file):
            try:
                with open(self.tracking_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️ Failed to load tracking file: {e}")
                return {}
        return {}
    
    def _save_tracking(self):
        """Save tracking data to file"""
        try:
            with open(self.tracking_file, 'w') as f:
                json.dump(self.data, f, indent=2, default=str)
        except Exception as e:
            print(f"❌ Failed to save tracking: {e}")
    
    def add_email(self, email_id: str, to_email: str, subject: str, priority: str = "normal") -> Dict:
        """Add email to tracking"""
        email_data = {
            "id": email_id,
            "to_email": to_email,
            "subject": subject,
            "status": EmailStatus.PENDING.value,
            "priority": priority,
            "created_at": datetime.now().isoformat(),
            "sent_at": None,
            "failed_at": None,
            "attempts": 0,
            "message_id": None,
            "error": None
        }
        self.data[email_id] = email_data
        self._save_tracking()
        return email_data
    
    def update_status(self, email_id: str, status: EmailStatus, message_id: str = None, error: str = None):
        """Update email status"""
        if email_id in self.data:
            self.data[email_id]["status"] = status.value
            if status == EmailStatus.SENT:
                self.data[email_id]["sent_at"] = datetime.now().isoformat()
                self.data[email_id]["message_id"] = message_id
            elif status == EmailStatus.FAILED:
                self.data[email_id]["failed_at"] = datetime.now().isoformat()
                self.data[email_id]["error"] = error
            self.data[email_id]["attempts"] += 1
            self._save_tracking()
    
    def get_email(self, email_id: str) -> Optional[Dict]:
        """Get email tracking info"""
        return self.data.get(email_id)
    
    def get_by_status(self, status: EmailStatus) -> List[Dict]:
        """Get all emails with specific status"""
        return [email for email in self.data.values() if email["status"] == status.value]

# ============ GMAIL SERVICE ============
class GmailService:
    """Professional Gmail service with tracking and retry logic"""
    
    def __init__(self, credentials_path: str = "gmail_credentials.json", 
                 token_path: str = "gmail_token.json",
                 tracking_file: str = "email_tracking.json"):
        self.credentials_path = credentials_path
        self.token_path = token_path
        self.service = None
        self.credentials = None
        self.available = GOOGLE_INSTALLED
        self.tracker = EmailTracker(tracking_file)
        self.max_retries = 3
        self.retry_delay = 60  # seconds
    
    def authenticate(self) -> bool:
        """Authenticate using OAuth2 flow"""
        if not GOOGLE_INSTALLED:
            print("❌ Gmail functionality not available - Google libraries not installed")
            return False
        
        creds = None
        
        # Load existing token if available
        if os.path.exists(self.token_path):
            try:
                creds = UserCredentials.from_authorized_user_file(self.token_path, SCOPES)
                print("✅ Loaded existing credentials")
            except Exception as e:
                print(f"⚠️ Failed to load token: {e}")
                creds = None
        
        # If no valid credentials, create new OAuth flow
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                print("🔄 Refreshing credentials...")
                creds.refresh(Request())
            else:
                if not os.path.exists(self.credentials_path):
                    print(f"❌ {self.credentials_path} not found")
                    print("📋 Get credentials from: https://console.cloud.google.com/apis/credentials")
                    return False
                
                print("🔐 Starting OAuth2 flow...")
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, SCOPES
                )
                # Use fixed port 8080 for OAuth2 redirect (configure this in Google Cloud Console)
                creds = flow.run_local_server(port=8080, open_browser=True)
            
            # Save token for future use
            try:
                with open(self.token_path, 'w') as token:
                    token.write(creds.to_json())
                print("💾 Credentials saved for future use")
            except Exception as e:
                print(f"⚠️ Failed to save credentials: {e}")
        
        self.credentials = creds
        self.service = build('gmail', 'v1', credentials=creds)
        return True
    
    def send_email(self, to: str, subject: str, html_body: str, 
                   cc: str = None, bcc: str = None, 
                   priority: str = EmailPriority.NORMAL.value) -> Tuple[bool, str, Optional[str]]:
        """Send professional HTML email via Gmail with tracking
        
        Returns: (success, message, message_id)
        """
        try:
            if not self.service:
                if not self.authenticate():
                    return False, "❌ Gmail authentication failed", None
            
            # Validate email format
            if not self._is_valid_email(to):
                return False, f"❌ Invalid email address: {to}", None
            
            # Create tracking record
            email_id = f"{to}_{datetime.now().timestamp()}"
            self.tracker.add_email(email_id, to, subject, priority)
            
            # Create message
            message = MIMEMultipart("alternative")
            message["to"] = to
            message["subject"] = subject
            
            if cc:
                message["cc"] = cc
            if bcc:
                message["bcc"] = bcc
            
            # Attach HTML with professional styling
            part = MIMEText(html_body, "html")
            message.attach(part)
            
            # Encode and send
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
            send_message = {'raw': raw_message}
            
            result = self.service.users().messages().send(
                userId='me', 
                body=send_message
            ).execute()
            
            message_id = result.get('id')
            self.tracker.update_status(email_id, EmailStatus.SENT, message_id)
            
            success_msg = f"✅ Email sent to {to} | ID: {message_id}"
            print(success_msg)
            return True, success_msg, message_id
        
        except Exception as e:
            error_msg = f"❌ Failed to send email to {to}: {str(e)}"
            print(error_msg)
            self.tracker.update_status(email_id if 'email_id' in locals() else f"{to}_{datetime.now().timestamp()}", 
                                      EmailStatus.FAILED, error=str(e))
            return False, error_msg, None
    
    def send_professional_email(self, to: str, company: str, subject_line: str, 
                               body_content: str, decision_maker: str = "") -> Tuple[bool, str, Optional[str]]:
        """Send a professional email with structured HTML template"""
        
        html_template = f"""
        <html>
          <head>
            <meta charset="UTF-8">
            <style>
              body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                color: #333;
                background-color: #f9fafb;
              }}
              .container {{
                max-width: 600px;
                margin: 0 auto;
                background-color: #ffffff;
                border: 1px solid #e5e7eb;
                border-radius: 8px;
                padding: 40px;
              }}
              .header {{
                border-bottom: 3px solid #3b82f6;
                padding-bottom: 20px;
                margin-bottom: 30px;
              }}
              .header h2 {{
                color: #1f2937;
                margin: 0;
              }}
              .company {{
                color: #6b7280;
                font-size: 14px;
                margin-top: 5px;
              }}
              .content {{
                margin: 30px 0;
                color: #4b5563;
              }}
              .footer {{
                margin-top: 30px;
                padding-top: 20px;
                border-top: 1px solid #e5e7eb;
                font-size: 12px;
                color: #9ca3af;
              }}
              .button {{
                display: inline-block;
                background-color: #3b82f6;
                color: white;
                padding: 12px 30px;
                text-decoration: none;
                border-radius: 6px;
                margin-top: 15px;
              }}
            </style>
          </head>
          <body>
            <div class="container">
              <div class="header">
                <h2>👋 Hi {decision_maker or 'there'}</h2>
                <div class="company">📋 {company}</div>
              </div>
              
              <div class="content">
                {body_content}
              </div>
              
              <div class="footer">
                <p>This email was generated by FlowForge AI</p>
                <p>✨ Professional Email Campaign | Quality at Scale</p>
              </div>
            </div>
          </body>
        </html>
        """
        
        return self.send_email(to, subject_line, html_template, priority=EmailPriority.NORMAL.value)
    
    def get_authenticated_user(self) -> Optional[Dict]:
        """Get authenticated user info"""
        try:
            if not self.service:
                if not self.authenticate():
                    return None
            
            profile = self.service.users().getProfile(userId='me').execute()
            user_info = {
                "email": profile.get('emailAddress'),
                "message_count": profile.get('messagesTotal', 0),
                "threads": profile.get('threadsTotal', 0),
                "status": "✅ Connected"
            }
            return user_info
        except Exception as e:
            print(f"❌ Failed to get user profile: {e}")
            return None
    
    def get_email_status(self, email_id: str) -> Optional[Dict]:
        """Get status of a tracked email"""
        return self.tracker.get_email(email_id)
    
    def get_pending_emails(self) -> List[Dict]:
        """Get all pending emails"""
        return self.tracker.get_by_status(EmailStatus.PENDING)
    
    def get_sent_emails(self) -> List[Dict]:
        """Get all sent emails"""
        return self.tracker.get_by_status(EmailStatus.SENT)
    
    def get_failed_emails(self) -> List[Dict]:
        """Get all failed emails"""
        return self.tracker.get_by_status(EmailStatus.FAILED)
    
    @staticmethod
    def _is_valid_email(email: str) -> bool:
        """Validate email format"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

# ============ GLOBAL INSTANCES ============
gmail_service = None

def init_gmail_service() -> GmailService:
    """Initialize Gmail service"""
    global gmail_service
    gmail_service = GmailService()
    return gmail_service

def get_gmail_service() -> GmailService:
    """Get Gmail service instance"""
    global gmail_service
    if gmail_service is None:
        return init_gmail_service()
    return gmail_service
