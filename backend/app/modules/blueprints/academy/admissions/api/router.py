from datetime import datetime
from typing import Any, Optional, cast
from uuid import UUID

from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel, ConfigDict

from app.api.dependencies import get_current_user
from app.modules.blueprints.academy.admissions.application.service import (
    AdmissionsService,
    CreateLeadCommand,
    CreateEnquiryCommand,
    RecordFollowUpCommand,
    AdmitEnquiryCommand,
    MarkEnquiryLostCommand,
)
from app.modules.blueprints.academy.admissions.application.queries import (
    AdmissionsQueryService,
    EnquiryPipelineItemView,
    EnquiryDetailsView,
)

router = APIRouter(prefix="/admissions", tags=["academy.admissions"])

def get_admissions_service(request: Request) -> AdmissionsService:
    container = request.app.state.container
    return cast(AdmissionsService, container.resolve(AdmissionsService))

def get_admissions_query_service(request: Request) -> AdmissionsQueryService:
    container = request.app.state.container
    return cast(AdmissionsQueryService, container.resolve(AdmissionsQueryService))

class CreateLeadRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    first_name: str
    phone: str
    last_name: Optional[str] = None
    email: Optional[str] = None

class CreateLeadResponse(BaseModel):
    id: UUID

@router.post("/leads", response_model=CreateLeadResponse, status_code=201)
async def create_lead(
    request: CreateLeadRequest,
    current_user: dict[str, Any] = Depends(get_current_user),
    service: AdmissionsService = Depends(get_admissions_service),
) -> CreateLeadResponse:
    cmd = CreateLeadCommand(
        organization_id=UUID(current_user["organization"]["id"]),
        first_name=request.first_name,
        phone=request.phone,
        last_name=request.last_name,
        email=request.email,
    )
    lead_id = await service.create_lead(cmd)
    return CreateLeadResponse(id=lead_id)

class CreateEnquiryRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    lead_id: UUID
    course_id: UUID
    source: str
    notes: Optional[str] = None

class CreateEnquiryResponse(BaseModel):
    id: UUID

@router.post("/enquiries", response_model=CreateEnquiryResponse, status_code=201)
async def create_enquiry(
    request: CreateEnquiryRequest,
    current_user: dict[str, Any] = Depends(get_current_user),
    service: AdmissionsService = Depends(get_admissions_service),
) -> CreateEnquiryResponse:
    cmd = CreateEnquiryCommand(
        organization_id=UUID(current_user["organization"]["id"]),
        lead_id=request.lead_id,
        course_id=request.course_id,
        source=request.source,
        notes=request.notes,
    )
    enquiry_id = await service.create_enquiry(cmd)
    return CreateEnquiryResponse(id=enquiry_id)

class RecordFollowUpRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    next_follow_up_at: datetime
    notes: str

@router.post("/enquiries/{enquiry_id}/follow-up", status_code=200)
async def record_follow_up(
    enquiry_id: UUID,
    request: RecordFollowUpRequest,
    current_user: dict[str, Any] = Depends(get_current_user),
    service: AdmissionsService = Depends(get_admissions_service),
) -> dict[str, str]:
    cmd = RecordFollowUpCommand(
        organization_id=UUID(current_user["organization"]["id"]),
        enquiry_id=enquiry_id,
        next_follow_up_at=request.next_follow_up_at,
        notes=request.notes,
    )
    await service.record_follow_up(cmd)
    return {"status": "success"}

class AdmitEnquiryResponse(BaseModel):
    student_id: UUID

@router.post("/enquiries/{enquiry_id}/admit", response_model=AdmitEnquiryResponse, status_code=200)
async def admit_enquiry(
    enquiry_id: UUID,
    current_user: dict[str, Any] = Depends(get_current_user),
    service: AdmissionsService = Depends(get_admissions_service),
) -> AdmitEnquiryResponse:
    cmd = AdmitEnquiryCommand(
        organization_id=UUID(current_user["organization"]["id"]),
        enquiry_id=enquiry_id,
        admitted_by=UUID(current_user["user"]["id"]),
    )
    student_id = await service.admit_enquiry(cmd)
    return AdmitEnquiryResponse(student_id=student_id)

class MarkEnquiryLostRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    reason: str

@router.post("/enquiries/{enquiry_id}/mark-lost", status_code=200)
async def mark_lost(
    enquiry_id: UUID,
    request: MarkEnquiryLostRequest,
    current_user: dict[str, Any] = Depends(get_current_user),
    service: AdmissionsService = Depends(get_admissions_service),
) -> dict[str, str]:
    cmd = MarkEnquiryLostCommand(
        organization_id=UUID(current_user["organization"]["id"]),
        enquiry_id=enquiry_id,
        reason=request.reason,
    )
    await service.mark_lost(cmd)
    return {"status": "success"}

@router.get("/pipeline", response_model=list[EnquiryPipelineItemView])
async def get_pipeline(
    status: Optional[str] = None,
    current_user: dict[str, Any] = Depends(get_current_user),
    query: AdmissionsQueryService = Depends(get_admissions_query_service),
) -> list[EnquiryPipelineItemView]:
    return await query.get_pipeline(UUID(current_user["organization"]["id"]), status)

@router.get("/enquiries/{enquiry_id}", response_model=EnquiryDetailsView)
async def get_enquiry_details(
    enquiry_id: UUID,
    current_user: dict[str, Any] = Depends(get_current_user),
    query: AdmissionsQueryService = Depends(get_admissions_query_service),
) -> EnquiryDetailsView:
    from fastapi import HTTPException
    view = await query.get_enquiry_details(UUID(current_user["organization"]["id"]), enquiry_id)
    if not view:
        raise HTTPException(status_code=404, detail="Enquiry not found")
    return view
