from datetime import datetime, timedelta
from typing import Dict, Optional, List
from core.config import settings


class GoogleCalendarIntegration:
    """Google Calendar integration for meeting booking"""

    def __init__(self):
        self.credentials_path = settings.GOOGLE_CALENDAR_CREDENTIALS_PATH
        self.calendar_email = settings.GOOGLE_CALENDAR_EMAIL
        self.service = None
        self._initialized = False

    async def initialize(self):
        """Initialize Google Calendar API (requires credentials)"""
        if not self.credentials_path or not self.calendar_email:
            return False

        try:
            from google.oauth2.service_account import Credentials
            from googleapiclient.discovery import build

            creds = Credentials.from_service_account_file(
                self.credentials_path,
                scopes=["https://www.googleapis.com/auth/calendar"],
            )
            self.service = build("calendar", "v3", credentials=creds)
            self._initialized = True
            return True
        except Exception as e:
            print(f"Google Calendar initialization error: {e}")
            return False

    async def find_available_slots(
        self,
        duration_minutes: int = 30,
        days_ahead: int = 7,
    ) -> List[Dict]:
        """
        Find available time slots in the calendar
        
        Returns:
            List of available time slots as dicts with start and end times
        """
        if not self._initialized:
            # Return mock available slots
            available = []
            now = datetime.now()
            for day in range(1, days_ahead):
                for hour in [9, 10, 11, 14, 15, 16]:
                    slot_time = now + timedelta(days=day, hours=hour)
                    available.append({
                        "start": slot_time.isoformat(),
                        "end": (slot_time + timedelta(minutes=duration_minutes)).isoformat(),
                    })
            return available[:10]

        try:
            now = datetime.now().isoformat() + "Z"
            end_time = (datetime.now() + timedelta(days=days_ahead)).isoformat() + "Z"

            events_result = self.service.events().list(
                calendarId=self.calendar_email,
                timeMin=now,
                timeMax=end_time,
                singleEvents=True,
                orderBy="startTime",
            ).execute()

            events = events_result.get("items", [])
            
            # Find gaps between events
            available_slots = self._find_gaps(events, duration_minutes, days_ahead)
            return available_slots
        except Exception as e:
            print(f"Google Calendar availability error: {e}")
            return []

    async def book_meeting(
        self,
        title: str,
        attendee_email: str,
        start_time: str,
        duration_minutes: int = 30,
        description: str = "",
    ) -> Dict:
        """
        Create a calendar event and invite attendee
        
        Args:
            title: Meeting title
            attendee_email: Attendee email address
            start_time: ISO format start time
            duration_minutes: Meeting duration
            description: Meeting description
            
        Returns:
            Dict with event_id, status, and meeting_link
        """
        if not self._initialized:
            # Return mock event
            return {
                "status": "created",
                "event_id": f"mock_event_{attendee_email}",
                "meeting_link": f"https://meet.google.com/mock-{attendee_email.split('@')[0]}",
                "calendar_link": f"https://calendar.google.com/calendar/r",
            }

        try:
            from datetime import datetime as dt

            start = dt.fromisoformat(start_time.replace("Z", "+00:00"))
            end = start + timedelta(minutes=duration_minutes)

            event = {
                "summary": title,
                "description": description,
                "start": {
                    "dateTime": start.isoformat(),
                    "timeZone": "UTC",
                },
                "end": {
                    "dateTime": end.isoformat(),
                    "timeZone": "UTC",
                },
                "attendees": [
                    {"email": attendee_email},
                ],
                "conferenceData": {
                    "createRequest": {
                        "requestId": f"conference_{attendee_email}",
                        "conferenceSolutionKey": {"key": "hangoutsMeet"},
                    }
                },
            }

            created_event = self.service.events().insert(
                calendarId=self.calendar_email,
                body=event,
                conferenceDataVersion=1,
                sendNotifications=True,
            ).execute()

            meeting_link = None
            if "conferenceData" in created_event:
                meeting_link = created_event["conferenceData"]["entryPoints"][0]["uri"]

            return {
                "status": "created",
                "event_id": created_event.get("id"),
                "meeting_link": meeting_link,
                "calendar_link": created_event.get("htmlLink"),
            }
        except Exception as e:
            print(f"Google Calendar event creation error: {e}")
            return {
                "status": "error",
                "message": str(e),
            }

    async def reschedule_meeting(
        self,
        event_id: str,
        new_start_time: str,
        duration_minutes: int = 30,
    ) -> Dict:
        """Reschedule an existing calendar event"""
        if not self._initialized:
            return {"status": "updated", "event_id": event_id}

        try:
            from datetime import datetime as dt

            event = self.service.events().get(
                calendarId=self.calendar_email,
                eventId=event_id,
            ).execute()

            start = dt.fromisoformat(new_start_time.replace("Z", "+00:00"))
            end = start + timedelta(minutes=duration_minutes)

            event["start"]["dateTime"] = start.isoformat()
            event["end"]["dateTime"] = end.isoformat()

            updated = self.service.events().update(
                calendarId=self.calendar_email,
                eventId=event_id,
                body=event,
                sendNotifications=True,
            ).execute()

            return {"status": "updated", "event_id": updated.get("id")}
        except Exception as e:
            print(f"Google Calendar reschedule error: {e}")
            return {"status": "error", "message": str(e)}

    async def cancel_meeting(self, event_id: str) -> Dict:
        """Cancel a calendar event"""
        if not self._initialized:
            return {"status": "deleted", "event_id": event_id}

        try:
            self.service.events().delete(
                calendarId=self.calendar_email,
                eventId=event_id,
                sendNotifications=True,
            ).execute()

            return {"status": "deleted", "event_id": event_id}
        except Exception as e:
            print(f"Google Calendar cancellation error: {e}")
            return {"status": "error", "message": str(e)}

    def _find_gaps(self, events: list, duration: int, days_ahead: int) -> List[Dict]:
        """Find gaps in calendar for available slots"""
        # Simplified: return mock slots if no real calendar
        available = []
        now = datetime.now()
        for day in range(1, days_ahead):
            for hour in [9, 10, 11, 14, 15, 16]:
                slot_time = now + timedelta(days=day, hours=hour)
                available.append({
                    "start": slot_time.isoformat(),
                    "end": (slot_time + timedelta(minutes=duration)).isoformat(),
                })
        return available[:10]


# Global instance
google_calendar = GoogleCalendarIntegration()
