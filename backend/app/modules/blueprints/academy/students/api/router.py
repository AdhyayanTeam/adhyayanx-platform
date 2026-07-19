from typing import Annotated, Any, cast
from uuid import UUID

from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel, ConfigDict

from app.api.dependencies import get_current_user
from app.modules.blueprints.academy.students.application.service import CreateStudentCommand, StudentService

router = APIRouter(prefix="/students", tags=["academy.students"])

def get_student_service(request: Request) -> StudentService:
    container = request.app.state.container
    return cast(StudentService, container.resolve(StudentService))

class CreateStudentRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    name: str
    email: str
    phone: str | None = None

class StudentResponse(BaseModel):
    id: UUID

@router.post("", response_model=StudentResponse, status_code=201)
async def create_student(
    request: CreateStudentRequest,
    current_user: dict[str, Any] = Depends(get_current_user),
    service: StudentService = Depends(get_student_service),
) -> StudentResponse:
    cmd = CreateStudentCommand(
        organization_id=UUID(current_user["organization"]["id"]),
        name=request.name,
        email=request.email,
        phone=request.phone,
    )
    student_id = await service.create_student(cmd)
    return StudentResponse(id=student_id)

from app.modules.blueprints.academy.students.contracts.student_query import StudentQueryContract, StudentDto
from fastapi import HTTPException

def get_student_query(request: Request) -> StudentQueryContract:
    container = request.app.state.container
    return cast(StudentQueryContract, container.resolve(StudentQueryContract))

@router.get("/{student_id}", response_model=StudentDto)
async def get_student(
    student_id: UUID,
    current_user: dict[str, Any] = Depends(get_current_user),
    query: StudentQueryContract = Depends(get_student_query),
) -> StudentDto:
    student = await query.get_student(UUID(current_user["organization"]["id"]), student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student
