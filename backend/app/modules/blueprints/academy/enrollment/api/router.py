from typing import Annotated, Any, cast
from uuid import UUID

from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel, ConfigDict

from app.api.dependencies import get_current_user
from app.modules.blueprints.academy.enrollment.application.service import EnrollStudentCommand, AssignBatchCommand, EnrollmentService

router = APIRouter(prefix="/enrollments", tags=["academy.enrollments"])

def get_enrollment_service(request: Request) -> EnrollmentService:
    container = request.app.state.container
    return cast(EnrollmentService, container.resolve(EnrollmentService))

class EnrollStudentRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    student_id: UUID
    course_id: UUID

class AssignBatchRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    batch_id: UUID

class ResourceResponse(BaseModel):
    id: UUID

@router.post("", response_model=ResourceResponse, status_code=201)
async def enroll_student(
    request: EnrollStudentRequest,
    current_user: dict[str, Any] = Depends(get_current_user),
    service: EnrollmentService = Depends(get_enrollment_service),
) -> ResourceResponse:
    cmd = EnrollStudentCommand(
        organization_id=current_user["organization"]["id"],
        student_id=request.student_id,
        course_id=request.course_id,
    )
    enrollment_id = await service.enroll_student(cmd)
    return ResourceResponse(id=enrollment_id)

@router.post("/{enrollment_id}/assign", response_model=ResourceResponse)
async def assign_batch(
    enrollment_id: UUID,
    request: AssignBatchRequest,
    current_user: dict[str, Any] = Depends(get_current_user),
    service: EnrollmentService = Depends(get_enrollment_service),
) -> ResourceResponse:
    cmd = AssignBatchCommand(
        organization_id=current_user["organization"]["id"],
        enrollment_id=enrollment_id,
        batch_id=request.batch_id,
    )
    assignment_id = await service.assign_batch(cmd)
    return ResourceResponse(id=assignment_id)

from app.modules.blueprints.academy.enrollment.application.queries import EnrollmentQueryService, StudentEnrollmentView

students_router = APIRouter(prefix="/students", tags=["academy.enrollments"])

def get_enrollment_query(request: Request) -> EnrollmentQueryService:
    container = request.app.state.container
    return cast(EnrollmentQueryService, container.resolve(EnrollmentQueryService))

@students_router.get("/{student_id}/enrollments", response_model=list[StudentEnrollmentView])
async def get_student_enrollments(
    student_id: UUID,
    current_user: dict[str, Any] = Depends(get_current_user),
    query: EnrollmentQueryService = Depends(get_enrollment_query),
) -> list[StudentEnrollmentView]:
    return await query.get_student_enrollments(current_user["organization"]["id"], student_id)
