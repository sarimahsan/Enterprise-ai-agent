"""
Meeting Service - Books discovery calls and manages calendars
Integrates with Google Calendar, Outlook, and Calendly
"""

from typing import Optional, Dict
from datetime import datetime
from integrations.google_calendar_integration import google_calendar

class MeetingSlot:
    def __init__(
        self,
        id: str,
        lead_id: str,
        scheduled_time: datetime,
        duration_minutes: int = 30,
        meeting_type: str = "discovery",  # discovery, demo, negotiation
        calendar_link: Optional[str] = None,
        zoom_link: Optional[str] = None,
    ):
        self.id = id
        self.lead_id = lead_id
        self.scheduled_time = scheduled_time
        self.duration_minutes = duration_minutes
        self.meeting_type = meeting_type
        self.calendar_link = calendar_link
        self.zoom_link = zoom_link
        self.status = "scheduled"  # scheduled, in_progress, completed, cancelled
        self.notes = ""

class MeetingService:
    def __init__(self):
        self.meetings_db = {}  # In production: PostgreSQL
        
    async def find_available_slots(
        self,
        lead_id: str,
        date_range_days: int = 7,
        preferred_time: Optional[str] = None,  # "morning", "afternoon"
    ) -> list:
        """
        Find available time slots from your calendar
        Checks Google Calendar for conflicts
        """
        slots = await google_calendar.find_available_slots(
            duration_minutes=30,
            days_ahead=date_range_days,
        )
        
        # Filter by preferred time if specified
        if preferred_time == "morning":
            slots = [s for s in slots if int(s["start"].split("T")[1][:2]) < 12]
        elif preferred_time == "afternoon":
            slots = [s for s in slots if int(s["start"].split("T")[1][:2]) >= 12]
        
        return slots

    async def book_meeting(
        self,
        lead_id: str,
        lead_email: str,
        lead_name: str,
        slot_datetime: datetime,
        meeting_type: str = "discovery",
    ) -> Optional[MeetingSlot]:
        """
        Book a meeting directly to both calendars
        - Create event in Google Calendar
        - Send invite to lead
        - Generate meeting link
        - Return confirmation
        """
        # Book in Google Calendar
        booking_result = await google_calendar.book_meeting(
            title=f"{meeting_type.capitalize()} Call - {lead_name}",
            attendee_email=lead_email,
            start_time=slot_datetime.isoformat(),
            duration_minutes=30,
            description=f"Discovery call with {lead_name} from {lead_id}",
        )
        
        if booking_result["status"] != "created":
            return None
        
        meeting = MeetingSlot(
            id=booking_result.get("event_id", f"meeting_{datetime.now().timestamp()}"),
            lead_id=lead_id,
            scheduled_time=slot_datetime,
            meeting_type=meeting_type,
            calendar_link=booking_result.get("calendar_link"),
            zoom_link=booking_result.get("meeting_link"),
        )
        
        self.meetings_db[meeting.id] = meeting
        return meeting

    async def reschedule_meeting(
        self,
        meeting_id: str,
        new_datetime: datetime,
    ) -> bool:
        """Reschedule an existing meeting"""
        if meeting_id in self.meetings_db:
            self.meetings_db[meeting_id].scheduled_time = new_datetime
            # TODO: Update calendar and notify lead
            return True
        return False

    async def send_reminder(self, meeting_id: str) -> bool:
        """Send meeting reminder to lead (24h before, 1h before)"""
        # TODO: Send email/SMS reminder
        return True

    async def cancel_meeting(self, meeting_id: str, reason: Optional[str] = None) -> bool:
        """Cancel a meeting and notify the lead"""
        if meeting_id in self.meetings_db:
            self.meetings_db[meeting_id].status = "cancelled"
            # TODO: Remove from calendars and notify
            return True
        return False

# Global instance
meeting_service = MeetingService()
