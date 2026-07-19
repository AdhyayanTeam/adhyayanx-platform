from typing import Optional
from uuid import UUID

from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.blueprints.academy.admissions.application.queries import (
    AdmissionsQueryService,
    EnquiryPipelineItemView,
    EnquiryDetailsView,
)

class PostgresAdmissionsQueryService(AdmissionsQueryService):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_pipeline(self, org_id: UUID, status: Optional[str] = None) -> list[EnquiryPipelineItemView]:
        sql = """
            SELECT 
                e.id as enquiry_id,
                l.id as lead_id,
                TRIM(l.first_name || ' ' || COALESCE(l.last_name, '')) as lead_name,
                l.phone as lead_phone,
                c.name as course_name,
                e.status,
                e.assigned_to,
                e.next_follow_up_at
            FROM academy_enquiries e
            JOIN academy_leads l ON e.lead_id = l.id
            JOIN academy_courses c ON e.course_id = c.id
            WHERE e.organization_id = :org_id
        """
        params = {"org_id": org_id}
        if status:
            sql += " AND e.status = :status"
            params["status"] = status
            
        sql += " ORDER BY e.next_follow_up_at ASC NULLS LAST, e.created_at DESC"
        
        result = await self._session.execute(text(sql), params)
        rows = result.fetchall()
        
        return [
            EnquiryPipelineItemView(
                enquiry_id=row.enquiry_id,
                lead_id=row.lead_id,
                lead_name=row.lead_name,
                lead_phone=row.lead_phone,
                course_name=row.course_name,
                status=row.status,
                assigned_to=row.assigned_to,
                next_follow_up_at=row.next_follow_up_at,
            ) for row in rows
        ]

    async def get_enquiry_details(self, org_id: UUID, enquiry_id: UUID) -> Optional[EnquiryDetailsView]:
        sql = """
            SELECT 
                e.id as enquiry_id,
                e.lead_id,
                s.id as student_id,
                TRIM(l.first_name || ' ' || COALESCE(l.last_name, '')) as lead_name,
                l.phone as lead_phone,
                l.email as lead_email,
                e.course_id,
                c.name as course_name,
                e.status,
                e.source,
                e.assigned_to,
                e.next_follow_up_at,
                e.notes,
                e.created_at
            FROM academy_enquiries e
            JOIN academy_leads l ON e.lead_id = l.id
            LEFT JOIN academy_students s ON l.phone = s.phone AND l.organization_id = s.organization_id
            JOIN academy_courses c ON e.course_id = c.id
            WHERE e.organization_id = :org_id AND e.id = :enquiry_id
        """
        result = await self._session.execute(text(sql), {"org_id": org_id, "enquiry_id": enquiry_id})
        row = result.fetchone()
        
        if not row:
            return None
            
        return EnquiryDetailsView(
            enquiry_id=row.enquiry_id,
            lead_id=row.lead_id,
            student_id=row.student_id,
            lead_name=row.lead_name,
            lead_phone=row.lead_phone,
            lead_email=row.lead_email,
            course_id=row.course_id,
            course_name=row.course_name,
            status=row.status,
            source=row.source,
            assigned_to=row.assigned_to,
            next_follow_up_at=row.next_follow_up_at,
            notes=row.notes,
            created_at=row.created_at,
        )
