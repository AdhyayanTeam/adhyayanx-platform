from typing import Optional, Protocol
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.postgres.academy_tables import LeadModel, EnquiryModel
from app.modules.blueprints.academy.admissions.domain.entities import Lead, Enquiry, EnquiryStatus, EnquirySource

class AdmissionsRepository(Protocol):
    async def get_lead(self, org_id: UUID, lead_id: UUID) -> Optional[Lead]: ...
    async def save_lead(self, lead: Lead) -> None: ...
    async def get_enquiry(self, org_id: UUID, enquiry_id: UUID) -> Optional[Enquiry]: ...
    async def save_enquiry(self, enquiry: Enquiry) -> None: ...

class PostgresAdmissionsRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_lead(self, org_id: UUID, lead_id: UUID) -> Optional[Lead]:
        result = await self._session.execute(
            select(LeadModel).where(LeadModel.organization_id == org_id, LeadModel.id == lead_id)
        )
        model = result.scalar_one_or_none()
        if not model:
            return None
        return Lead(
            id=model.id,
            organization_id=model.organization_id,
            first_name=model.first_name,
            last_name=model.last_name,
            phone=model.phone,
            email=model.email,
            created_at=model.created_at,
        )

    async def save_lead(self, lead: Lead) -> None:
        result = await self._session.execute(
            select(LeadModel).where(LeadModel.id == lead.id)
        )
        model = result.scalar_one_or_none()
        if not model:
            model = LeadModel(
                id=lead.id,
                organization_id=lead.organization_id,
                first_name=lead.first_name,
                last_name=lead.last_name,
                phone=lead.phone,
                email=lead.email,
            )
            self._session.add(model)
        else:
            model.first_name = lead.first_name
            model.last_name = lead.last_name
            model.phone = lead.phone
            model.email = lead.email

    async def get_enquiry(self, org_id: UUID, enquiry_id: UUID) -> Optional[Enquiry]:
        result = await self._session.execute(
            select(EnquiryModel).where(EnquiryModel.organization_id == org_id, EnquiryModel.id == enquiry_id)
        )
        model = result.scalar_one_or_none()
        if not model:
            return None
        return Enquiry(
            id=model.id,
            organization_id=model.organization_id,
            lead_id=model.lead_id,
            course_id=model.course_id,
            status=EnquiryStatus(model.status),
            source=EnquirySource(model.source),
            assigned_to=model.assigned_to,
            next_follow_up_at=model.next_follow_up_at,
            notes=model.notes,
            admitted_at=model.admitted_at,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    async def save_enquiry(self, enquiry: Enquiry) -> None:
        result = await self._session.execute(
            select(EnquiryModel).where(EnquiryModel.id == enquiry.id)
        )
        model = result.scalar_one_or_none()
        if not model:
            model = EnquiryModel(
                id=enquiry.id,
                organization_id=enquiry.organization_id,
                lead_id=enquiry.lead_id,
                course_id=enquiry.course_id,
                status=enquiry.status.value,
                source=enquiry.source.value,
                assigned_to=enquiry.assigned_to,
                next_follow_up_at=enquiry.next_follow_up_at,
                notes=enquiry.notes,
                admitted_at=enquiry.admitted_at,
            )
            self._session.add(model)
        else:
            model.status = enquiry.status.value
            model.source = enquiry.source.value
            model.assigned_to = enquiry.assigned_to
            model.next_follow_up_at = enquiry.next_follow_up_at
            model.notes = enquiry.notes
            model.admitted_at = enquiry.admitted_at
