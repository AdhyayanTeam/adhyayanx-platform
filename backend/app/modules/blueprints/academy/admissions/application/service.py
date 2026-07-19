from dataclasses import dataclass
from datetime import datetime, UTC
from typing import Optional
from uuid import UUID, uuid4
import json

from app.modules.blueprints.academy.admissions.domain.entities import Lead, Enquiry, EnquiryStatus, EnquirySource
from app.modules.blueprints.academy.admissions.infrastructure.unit_of_work import AdmissionsUnitOfWork

@dataclass
class CreateLeadCommand:
    organization_id: UUID
    first_name: str
    phone: str
    last_name: Optional[str] = None
    email: Optional[str] = None

@dataclass
class CreateEnquiryCommand:
    organization_id: UUID
    lead_id: UUID
    course_id: UUID
    source: str
    notes: Optional[str] = None

@dataclass
class RecordFollowUpCommand:
    organization_id: UUID
    enquiry_id: UUID
    next_follow_up_at: datetime
    notes: str

@dataclass
class AdmitEnquiryCommand:
    organization_id: UUID
    enquiry_id: UUID
    admitted_by: UUID

@dataclass
class MarkEnquiryLostCommand:
    organization_id: UUID
    enquiry_id: UUID
    reason: str

class AdmissionsService:
    def __init__(self, uow: AdmissionsUnitOfWork) -> None:
        self._uow = uow

    async def create_lead(self, cmd: CreateLeadCommand) -> UUID:
        async with self._uow:
            lead_id = uuid4()
            lead = Lead(
                id=lead_id,
                organization_id=cmd.organization_id,
                first_name=cmd.first_name,
                last_name=cmd.last_name,
                phone=cmd.phone,
                email=cmd.email,
            )
            await self._uow.repository.save_lead(lead)
            await self._uow.commit()
            return lead_id

    async def create_enquiry(self, cmd: CreateEnquiryCommand) -> UUID:
        async with self._uow:
            lead = await self._uow.repository.get_lead(cmd.organization_id, cmd.lead_id)
            if not lead:
                raise ValueError("Lead not found")
            
            enquiry_id = uuid4()
            enquiry = Enquiry(
                id=enquiry_id,
                organization_id=cmd.organization_id,
                lead_id=cmd.lead_id,
                course_id=cmd.course_id,
                status=EnquiryStatus.NEW,
                source=EnquirySource(cmd.source.upper()),
                notes=cmd.notes,
            )
            await self._uow.repository.save_enquiry(enquiry)
            await self._uow.commit()
            return enquiry_id

    async def record_follow_up(self, cmd: RecordFollowUpCommand) -> None:
        async with self._uow:
            enquiry = await self._uow.repository.get_enquiry(cmd.organization_id, cmd.enquiry_id)
            if not enquiry:
                raise ValueError("Enquiry not found")
            
            enquiry.record_follow_up(cmd.next_follow_up_at, cmd.notes)
            await self._uow.repository.save_enquiry(enquiry)
            await self._uow.commit()

    async def mark_lost(self, cmd: MarkEnquiryLostCommand) -> None:
        async with self._uow:
            enquiry = await self._uow.repository.get_enquiry(cmd.organization_id, cmd.enquiry_id)
            if not enquiry:
                raise ValueError("Enquiry not found")
            
            enquiry.mark_lost(cmd.reason)
            await self._uow.repository.save_enquiry(enquiry)
            await self._uow.commit()

    async def admit_enquiry(self, cmd: AdmitEnquiryCommand) -> None:
        async with self._uow:
            enquiry = await self._uow.repository.get_enquiry(cmd.organization_id, cmd.enquiry_id)
            if not enquiry:
                raise ValueError("Enquiry not found")

            lead = await self._uow.repository.get_lead(cmd.organization_id, enquiry.lead_id)
            if not lead:
                raise ValueError("Lead not found")

            # Validate
            if enquiry.status in (EnquiryStatus.ADMITTED, EnquiryStatus.LOST):
                raise ValueError("Enquiry cannot be admitted")

            # 1. Resolve Identity
            student_id = await self._uow.student_queries.find_by_phone(cmd.organization_id, lead.phone)
            
            # 2. Upsert Student
            if not student_id:
                student_id = await self._uow.student_commands.create_student(
                    org_id=cmd.organization_id,
                    name=f"{lead.first_name} {lead.last_name or ''}".strip(),
                    phone=lead.phone,
                    email=lead.email,
                )

            # 3. Enroll
            await self._uow.enrollment_commands.enroll_student(
                org_id=cmd.organization_id,
                student_id=student_id,
                course_id=enquiry.course_id,
            )

            # 4. Finalize
            enquiry.admit(admitted_at=datetime.now(UTC))
            await self._uow.repository.save_enquiry(enquiry)

            # 5. Publish Event
            from app.modules.blueprints.academy.admissions.domain.events import EnquiryAdmitted
            event = EnquiryAdmitted.create(
                enquiry_id=enquiry.id,
                organization_id=cmd.organization_id,
                student_id=student_id,
                course_id=enquiry.course_id,
                admitted_by=cmd.admitted_by,
            )
            self._uow.record(event)

            # 6. Commit
            await self._uow.commit()
