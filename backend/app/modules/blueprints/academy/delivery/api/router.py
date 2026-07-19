from datetime import datetime
from typing import Annotated, Any, cast
from uuid import UUID

from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel, ConfigDict

from app.api.dependencies import get_current_user
from app.modules.blueprints.academy.delivery.application.service import CreateBatchCommand, BatchService

router = APIRouter(prefix="/delivery/batches", tags=["academy.delivery"])

def get_batch_service(request: Request) -> BatchService:
    container = request.app.state.container
    return cast(BatchService, container.resolve(BatchService))

class CreateBatchRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    course_id: UUID
    name: str
    start_date: datetime | None = None

class BatchResponse(BaseModel):
    id: UUID

@router.post("", response_model=BatchResponse, status_code=201)
async def create_batch(
    request: CreateBatchRequest,
    current_user: dict[str, Any] = Depends(get_current_user),
    service: BatchService = Depends(get_batch_service),
) -> BatchResponse:
    cmd = CreateBatchCommand(
        organization_id=UUID(current_user["organization"]["id"]),
        course_id=request.course_id,
        name=request.name,
        start_date=request.start_date,
    )
    batch_id = await service.create_batch(cmd)
    return BatchResponse(id=batch_id)

from app.modules.blueprints.academy.delivery.application.service import (
    DeliveryService, 
    CreateSessionCommand, 
    SubmitAttendanceCommand, 
    CorrectAttendanceCommand,
    StudentAttendanceCmd
)

sessions_router = APIRouter(prefix="/delivery", tags=["academy.delivery"])

def get_delivery_service(request: Request) -> DeliveryService:
    container = request.app.state.container
    return cast(DeliveryService, container.resolve(DeliveryService))

class CreateSessionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    starts_at: datetime
    ends_at: datetime

class SessionResponse(BaseModel):
    id: UUID

@sessions_router.post("/batches/{batch_id}/sessions", response_model=SessionResponse, status_code=201)
async def create_session(
    batch_id: UUID,
    request: CreateSessionRequest,
    current_user: dict[str, Any] = Depends(get_current_user),
    service: DeliveryService = Depends(get_delivery_service),
) -> SessionResponse:
    cmd = CreateSessionCommand(
        organization_id=UUID(current_user["organization"]["id"]),
        batch_id=batch_id,
        starts_at=request.starts_at,
        ends_at=request.ends_at,
    )
    session_id = await service.create_session(cmd)
    return SessionResponse(id=session_id)

class StudentAttendanceReq(BaseModel):
    model_config = ConfigDict(extra="forbid")
    student_id: UUID
    status: str

class SubmitAttendanceRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    records: list[StudentAttendanceReq]

@sessions_router.post("/sessions/{session_id}/attendance", status_code=200)
async def submit_attendance(
    session_id: UUID,
    request: SubmitAttendanceRequest,
    current_user: dict[str, Any] = Depends(get_current_user),
    service: DeliveryService = Depends(get_delivery_service),
) -> dict[str, str]:
    cmd = SubmitAttendanceCommand(
        organization_id=UUID(current_user["organization"]["id"]),
        session_id=session_id,
        submitted_by=UUID(current_user["user"]["id"]),
        records=[StudentAttendanceCmd(student_id=r.student_id, status=r.status) for r in request.records]
    )
    await service.submit_attendance(cmd)
    return {"status": "success"}

class CorrectAttendanceRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    status: str

@sessions_router.put("/sessions/{session_id}/attendance/{student_id}", status_code=200)
async def correct_attendance(
    session_id: UUID,
    student_id: UUID,
    request: CorrectAttendanceRequest,
    current_user: dict[str, Any] = Depends(get_current_user),
    service: DeliveryService = Depends(get_delivery_service),
) -> dict[str, str]:
    cmd = CorrectAttendanceCommand(
        organization_id=UUID(current_user["organization"]["id"]),
        session_id=session_id,
        student_id=student_id,
        new_status=request.status,
        corrected_by=UUID(current_user["user"]["id"])
    )
    await service.correct_attendance(cmd)
    return {"status": "success"}

from datetime import date
from typing import Optional
from app.modules.blueprints.academy.delivery.application.queries import (
    BatchOperationsQuery,
    TodaySessionView,
    BatchOverviewView,
    BatchRosterView,
    SessionAttendanceSheetView,
    BatchSessionSummaryView,
)

def get_batch_operations_query(request: Request) -> BatchOperationsQuery:
    container = request.app.state.container
    return cast(BatchOperationsQuery, container.resolve(BatchOperationsQuery))

@sessions_router.get("/sessions", response_model=list[TodaySessionView])
async def get_todays_sessions(
    date: date | None = None,
    current_user: dict[str, Any] = Depends(get_current_user),
    query: BatchOperationsQuery = Depends(get_batch_operations_query),
) -> list[TodaySessionView]:
    return await query.get_todays_sessions(UUID(current_user["organization"]["id"]), date)

@sessions_router.get("/batches/{batch_id}", response_model=BatchOverviewView)
async def get_batch_overview(
    batch_id: UUID,
    current_user: dict[str, Any] = Depends(get_current_user),
    query: BatchOperationsQuery = Depends(get_batch_operations_query),
) -> BatchOverviewView:
    view = await query.get_batch_overview(UUID(current_user["organization"]["id"]), batch_id)
    if not view:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Batch not found")
    return view

@sessions_router.get("/batches/{batch_id}/roster", response_model=list[BatchRosterView])
async def get_batch_roster(
    batch_id: UUID,
    current_user: dict[str, Any] = Depends(get_current_user),
    query: BatchOperationsQuery = Depends(get_batch_operations_query),
) -> list[BatchRosterView]:
    return await query.get_batch_roster(UUID(current_user["organization"]["id"]), batch_id)

@sessions_router.get("/batches/{batch_id}/attendance-summary", response_model=list[BatchSessionSummaryView])
async def get_batch_attendance_summary(
    batch_id: UUID,
    current_user: dict[str, Any] = Depends(get_current_user),
    query: BatchOperationsQuery = Depends(get_batch_operations_query),
) -> list[BatchSessionSummaryView]:
    return await query.get_batch_attendance_summary(UUID(current_user["organization"]["id"]), batch_id)

@sessions_router.get("/sessions/{session_id}/attendance", response_model=list[SessionAttendanceSheetView])
async def get_session_attendance(
    session_id: UUID,
    current_user: dict[str, Any] = Depends(get_current_user),
    query: BatchOperationsQuery = Depends(get_batch_operations_query),
) -> list[SessionAttendanceSheetView]:
    return await query.get_session_attendance(UUID(current_user["organization"]["id"]), session_id)
