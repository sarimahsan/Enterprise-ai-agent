"""Google Calendar service for scheduling campaigns and follow-ups."""

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import json
import os
from typing import Optional, Dict, List

SCOPES = [
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/calendar.events'
]

class CalendarService:
    def __init__(self, credentials_file: str = "gmail_credentials.json"):
        self.credentials_file = credentials_file
        self.service = None
        self.credentials = None

    def authenticate(self) -> bool:
        """Authenticate with Google Calendar API."""
        try:
            flow = InstalledAppFlow.from_client_secrets_file(
                self.credentials_file, 
                SCOPES
            )
            self.credentials = flow.run_local_server(port=0)
            self.service = build('calendar', 'v3', credentials=self.credentials)
            return True
        except Exception as e:
            print(f"Calendar auth failed: {e}")
            return False

    def schedule_event(
        self,
        summary: str,
        start_time: datetime,
        duration_minutes: int = 30,
        description: str = "",
        timezone: str = "UTC"
    ) -> Dict:
        """Schedule an event in Google Calendar."""
        if not self.service:
            return {"success": False, "error": "Not authenticated"}

        try:
            end_time = start_time + timedelta(minutes=duration_minutes)
            
            event = {
                'summary': summary,
                'description': description,
                'start': {
                    'dateTime': start_time.isoformat(),
                    'timeZone': timezone,
                },
                'end': {
                    'dateTime': end_time.isoformat(),
                    'timeZone': timezone,
                },
                'reminders': {
                    'useDefault': True,
                }
            }

            result = self.service.events().insert(
                calendarId='primary',
                body=event
            ).execute()

            return {
                "success": True,
                "event_id": result.get('id'),
                "event": result
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def schedule_campaign(
        self,
        campaign_name: str,
        start_time: datetime,
        timezone: str = "UTC"
    ) -> Dict:
        """Schedule a campaign to send emails at specific time."""
        return self.schedule_event(
            summary=f"🎯 Campaign: {campaign_name}",
            start_time=start_time,
            duration_minutes=60,
            description="Scheduled campaign email send",
            timezone=timezone
        )

    def schedule_followup(
        self,
        campaign_name: str,
        initial_send_time: datetime,
        followup_delay_days: int = 3,
        timezone: str = "UTC"
    ) -> Dict:
        """Schedule a follow-up event relative to initial campaign."""
        followup_time = initial_send_time + timedelta(days=followup_delay_days)
        
        return self.schedule_event(
            summary=f"📧 Follow-up: {campaign_name}",
            start_time=followup_time,
            duration_minutes=30,
            description=f"Follow-up email ({followup_delay_days} days after initial send)",
            timezone=timezone
        )

    def get_available_slots(
        self,
        start_date: datetime,
        num_days: int = 7,
        timezone: str = "UTC"
    ) -> List[Dict]:
        """Get available time slots from calendar."""
        if not self.service:
            return []

        try:
            end_date = start_date + timedelta(days=num_days)
            
            events_result = self.service.events().list(
                calendarId='primary',
                timeMin=start_date.isoformat(),
                timeMax=end_date.isoformat(),
                singleEvents=True,
                orderBy='startTime'
            ).execute()

            events = events_result.get('events', [])
            
            # Find gaps in the schedule
            available_slots = []
            current_time = start_date.replace(hour=9, minute=0, second=0, microsecond=0)
            end_of_day = current_time.replace(hour=18, minute=0)

            for event in events:
                event_start = datetime.fromisoformat(
                    event['start'].get('dateTime', event['start'].get('date'))
                )
                
                if current_time < event_start:
                    available_slots.append({
                        'start': current_time.isoformat(),
                        'end': event_start.isoformat(),
                        'duration_hours': (event_start - current_time).total_seconds() / 3600
                    })
                
                event_end = datetime.fromisoformat(
                    event['end'].get('dateTime', event['end'].get('date'))
                )
                current_time = event_end

            # Add remaining time until end of day
            if current_time < end_of_day:
                available_slots.append({
                    'start': current_time.isoformat(),
                    'end': end_of_day.isoformat(),
                    'duration_hours': (end_of_day - current_time).total_seconds() / 3600
                })

            return available_slots
        except Exception as e:
            print(f"Error fetching available slots: {e}")
            return []

    def is_authenticated(self) -> bool:
        """Check if authenticated with Calendar API."""
        return self.service is not None
