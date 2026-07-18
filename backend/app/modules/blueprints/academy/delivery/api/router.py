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
