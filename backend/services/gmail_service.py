"""
Gmail Service - Handle OAuth2 authentication and email sending
"""
import os
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Try to import Google libraries
GOOGLE_INSTALLED = False
try:
    from google.auth.transport.requests import Request
    print("✓ Imported: google.auth.transport.requests")
except ImportError as e:
    print(f"❌ Missing: google.auth.transport.requests - {e}")

try:
    from google.oauth2.service_account import Credentials as ServiceAccountCredentials
    print("✓ Imported: google.oauth2.service_account")
except ImportError as e:
    print(f"❌ Missing: google.oauth2.service_account - {e}")

try:
    from google_auth_oauthlib.flow import InstalledAppFlow
    print("✓ Imported: google_auth_oauthlib.flow")
except ImportError as e:
    print(f"❌ Missing: google_auth_oauthlib.flow - {e}")

try:
    from googleapiclient.discovery import build
    print("✓ Imported: googleapiclient.discovery")
except ImportError as e:
    print(f"❌ Missing: googleapiclient.discovery - {e}")

try:
    from google.oauth2.credentials import Credentials as UserCredentials
    print("✓ Imported: google.oauth2.credentials")
except ImportError as e:
    print(f"❌ Missing: google.oauth2.credentials - {e}")

# Check if all critical imports succeeded
try:
    Request
    ServiceAccountCredentials
    InstalledAppFlow
    build
    UserCredentials
    GOOGLE_INSTALLED = True
except NameError as e:
    print(f"⚠️ Google Auth libraries not fully installed: {e}")
    print("Gmail integration will be disabled. To enable:")
    print("  pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client")
    GOOGLE_INSTALLED = False

import json

# Gmail OAuth2 scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

class GmailService:
    def __init__(self, credentials_path: str = "gmail_credentials.json", token_path: str = "gmail_token.json"):
        self.credentials_path = credentials_path
        self.token_path = token_path
        self.service = None
        self.credentials = None
        self.available = GOOGLE_INSTALLED

    def authenticate(self):
        """Authenticate using OAuth2 flow"""
        if not GOOGLE_INSTALLED:
            print("❌ Gmail functionality not available - Google libraries not installed")
            return False
            
        creds = None
        
        # Load existing token if available
        if os.path.exists(self.token_path):
            try:
                creds = UserCredentials.from_authorized_user_file(self.token_path, SCOPES)
            except Exception as e:
                print(f"❌ Failed to load token: {e}")
                creds = None

        # If no valid credentials, create new OAuth flow
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(self.credentials_path):
                    print(f"⚠️ {self.credentials_path} not found. Please set up OAuth2 credentials.")
                    print("Get credentials from: https://console.cloud.google.com/apis/credentials")
                    return False
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, SCOPES
                )
                creds = flow.run_local_server(port=0)
            
            # Save token for future use
            with open(self.token_path, 'w') as token:
                token.write(creds.to_json())

        self.credentials = creds
        self.service = build('gmail', 'v1', credentials=creds)
        return True

    def send_email(self, to: str, subject: str, body: str, cc: str = None, bcc: str = None) -> bool:
        """Send email via Gmail"""
        try:
            if not self.service:
                if not self.authenticate():
                    return False

            # Create message
            message = MIMEMultipart("alternative")
            message["to"] = to
            message["subject"] = subject
            
            if cc:
                message["cc"] = cc
            if bcc:
                message["bcc"] = bcc

            # Use HTML for rich formatting
            html_body = f"""
            <html>
              <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto;">
                  {body}
                </div>
              </body>
            </html>
            """

            part = MIMEText(html_body, "html")
            message.attach(part)

            # Encode message
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
            send_message = {'raw': raw_message}

            # Send
            result = self.service.users().messages().send(userId='me', body=send_message).execute()
            print(f"✅ Email sent to {to}. Message ID: {result['id']}")
            return True

        except Exception as e:
            print(f"❌ Failed to send email: {e}")
            return False

    def get_authenticated_user(self) -> dict:
        """Get authenticated user info"""
        try:
            if not self.service:
                if not self.authenticate():
                    return None
            
            profile = self.service.users().getProfile(userId='me').execute()
            return {
                "email": profile.get('emailAddress'),
                "message_count": profile.get('messagesTotal', 0)
            }
        except Exception as e:
            print(f"❌ Failed to get user profile: {e}")
            return None


# Global instance
gmail_service = None

def init_gmail_service():
    """Initialize Gmail service"""
    global gmail_service
    gmail_service = GmailService()
    return gmail_service

def get_gmail_service():
    """Get Gmail service instance"""
    global gmail_service
    if gmail_service is None:
        return init_gmail_service()
    return gmail_service
