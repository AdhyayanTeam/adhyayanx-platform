from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Protocol
from uuid import UUID

@dataclass
class EnquiryPipelineItemView:
    enquiry_id: UUID
    lead_id: UUID
    lead_name: str
    lead_phone: str
    course_name: str
    status: str
    assigned_to: Optional[UUID]
    next_follow_up_at: Optional[datetime]

@dataclass
class EnquiryDetailsView:
    enquiry_id: UUID
    lead_id: UUID
    student_id: Optional[UUID]
    lead_name: str
    lead_phone: str
    lead_email: Optional[str]
    course_id: UUID
    course_name: str
    status: str
    source: str
    assigned_to: Optional[UUID]
    next_follow_up_at: Optional[datetime]
    notes: Optional[str]
    created_at: datetime
    
class AdmissionsQueryService(Protocol):
    async def get_pipeline(self, org_id: UUID, status: Optional[str] = None) -> list[EnquiryPipelineItemView]:
        ...
    async def get_enquiry_details(self, org_id: UUID, enquiry_id: UUID) -> Optional[EnquiryDetailsView]:
        ...
