from typing import Any
from uuid import UUID

from pydantic import Field

from app.modules.platform.contracts.event import DomainEvent

class EnquiryAdmitted(DomainEvent):
    event_type: str = "EnquiryAdmitted"
    aggregate_type: str = "enquiry"
    
    @classmethod
    def create(cls, enquiry_id: UUID, organization_id: UUID, student_id: UUID, course_id: UUID, admitted_by: UUID) -> "EnquiryAdmitted":
        return cls(
            aggregate_id=enquiry_id,
            data={
                "enquiry_id": str(enquiry_id),
                "organization_id": str(organization_id),
                "student_id": str(student_id),
                "course_id": str(course_id),
                "admitted_by": str(admitted_by),
            }
        )
