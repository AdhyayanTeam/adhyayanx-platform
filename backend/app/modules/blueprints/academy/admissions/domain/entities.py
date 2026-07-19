from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

class EnquiryStatus(str, Enum):
    NEW = "NEW"
    CONTACTED = "CONTACTED"
    FOLLOW_UP = "FOLLOW_UP"
    ADMITTED = "ADMITTED"
    LOST = "LOST"

class EnquirySource(str, Enum):
    WEBSITE = "WEBSITE"
    WALKIN = "WALKIN"
    WHATSAPP = "WHATSAPP"
    REFERRAL = "REFERRAL"
    OTHER = "OTHER"

@dataclass
class Lead:
    id: UUID
    organization_id: UUID
    first_name: str
    phone: str
    last_name: Optional[str] = None
    email: Optional[str] = None
    created_at: Optional[datetime] = None

@dataclass
class Enquiry:
    id: UUID
    organization_id: UUID
    lead_id: UUID
    course_id: UUID
    status: EnquiryStatus
    source: EnquirySource
    assigned_to: Optional[UUID] = None
    next_follow_up_at: Optional[datetime] = None
    notes: Optional[str] = None
    admitted_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def record_follow_up(self, next_follow_up_at: datetime, notes: str) -> None:
        self.next_follow_up_at = next_follow_up_at
        if self.notes:
            self.notes = f"{self.notes}\n\n---\n{notes}"
        else:
            self.notes = notes
        if self.status == EnquiryStatus.NEW:
            self.status = EnquiryStatus.FOLLOW_UP

    def mark_lost(self, reason: str) -> None:
        self.status = EnquiryStatus.LOST
        if self.notes:
            self.notes = f"{self.notes}\n\nLost Reason: {reason}"
        else:
            self.notes = f"Lost Reason: {reason}"
        self.next_follow_up_at = None

    def admit(self, admitted_at: datetime) -> None:
        if self.status in (EnquiryStatus.ADMITTED, EnquiryStatus.LOST):
            raise ValueError("Cannot admit an enquiry that is already admitted or lost.")
        self.status = EnquiryStatus.ADMITTED
        self.admitted_at = admitted_at
        self.next_follow_up_at = None
