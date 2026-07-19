from datetime import datetime, UTC, date
from uuid import uuid4

import pytest
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import FastAPI
from httpx import AsyncClient

from tests.integration.academy.test_catalog_postgres import (
    async_client,
    app_with_db,
    real_database,
    real_settings,
)

from app.infrastructure.postgres.database import Database
from app.infrastructure.postgres.tables import OrganizationTable
from app.infrastructure.postgres.academy_tables import (
    CourseTable, BatchTable, SessionTable, StudentTable, BatchAssignmentTable, EnrollmentTable, AttendanceRecordTable
)

DELIVERY_PREFIX = "/api/v1/academy/delivery"

@pytest.fixture
async def setup_query_data(real_database: Database, app_with_db: FastAPI) -> dict:
    org_id = uuid4()
    course_id = uuid4()
    batch_id = uuid4()
    session_id_1 = uuid4()
    session_id_2 = uuid4()
    student_1_id = uuid4()
    student_2_id = uuid4()
    enrollment_1_id = uuid4()
    enrollment_2_id = uuid4()

    async with real_database.session() as session:
        # Create Org with a specific timezone
        await session.execute(
            insert(OrganizationTable).values(
                id=org_id,
                name="Test Org for Queries",
                slug=f"test-queries-org-{org_id}",
                timezone="Asia/Kolkata",
                lifecycle_state="active",
                version=1,
                extra={},
                created_at=datetime.now(UTC),
                updated_at=datetime.now(UTC),
            )
        )
        
        await session.execute(
            insert(CourseTable).values(
                id=course_id, organization_id=org_id, title="Test Course", created_at=datetime.now(UTC), updated_at=datetime.now(UTC)
            )
        )
        await session.execute(
            insert(BatchTable).values(
                id=batch_id, organization_id=org_id, course_id=course_id, name="Test Batch", created_at=datetime.now(UTC), updated_at=datetime.now(UTC)
            )
        )
        await session.execute(
            insert(StudentTable).values([
                {"id": student_1_id, "organization_id": org_id, "name": "Student A", "email": "a@example.com", "created_at": datetime.now(UTC), "updated_at": datetime.now(UTC)},
                {"id": student_2_id, "organization_id": org_id, "name": "Student B", "email": "b@example.com", "created_at": datetime.now(UTC), "updated_at": datetime.now(UTC)},
            ])
        )
        await session.execute(
            insert(EnrollmentTable).values([
                {"id": enrollment_1_id, "organization_id": org_id, "student_id": student_1_id, "course_id": course_id, "created_at": datetime.now(UTC), "updated_at": datetime.now(UTC)},
                {"id": enrollment_2_id, "organization_id": org_id, "student_id": student_2_id, "course_id": course_id, "created_at": datetime.now(UTC), "updated_at": datetime.now(UTC)},
            ])
        )
        past = datetime(2025, 1, 1, 10, 0, tzinfo=UTC)
        await session.execute(
            insert(BatchAssignmentTable).values([
                {"id": uuid4(), "organization_id": org_id, "enrollment_id": enrollment_1_id, "batch_id": batch_id, "assigned_at": past},
                {"id": uuid4(), "organization_id": org_id, "enrollment_id": enrollment_2_id, "batch_id": batch_id, "assigned_at": past},
            ])
        )
        
        now = datetime.now(UTC)
        # Session 1: Today
        await session.execute(
            insert(SessionTable).values(
                id=session_id_1, organization_id=org_id, batch_id=batch_id,
                starts_at=now, ends_at=now, status="scheduled",
                created_at=datetime.now(UTC), updated_at=datetime.now(UTC)
            )
        )
        # Session 2: Past (attendance submitted)
        await session.execute(
            insert(SessionTable).values(
                id=session_id_2, organization_id=org_id, batch_id=batch_id,
                starts_at=past, ends_at=past, status="scheduled",
                attendance_submitted_at=past,
                created_at=past, updated_at=past
            )
        )
        # Attendance records for Session 2
        await session.execute(
            insert(AttendanceRecordTable).values([
                {"session_id": session_id_2, "student_id": student_1_id, "organization_id": org_id, "status": "PRESENT", "created_at": past, "updated_at": past},
                {"session_id": session_id_2, "student_id": student_2_id, "organization_id": org_id, "status": "ABSENT", "created_at": past, "updated_at": past},
            ])
        )

        await session.commit()

    return {
        "org_id": org_id,
        "batch_id": batch_id,
        "session_id_1": session_id_1,
        "session_id_2": session_id_2,
        "student_1": student_1_id,
        "student_2": student_2_id,
    }


@pytest.fixture
def override_auth(app_with_db: FastAPI, setup_query_data: dict):
    from app.api.dependencies import get_current_user
    org_id = setup_query_data["org_id"]
    
    async def mock_current_user():
        return {
            "user": {"id": str(uuid4()), "email": "test@example.com"},
            "organization": {"id": str(org_id), "name": "Test Org", "timezone": "Asia/Kolkata"},
            "roles": [],
        }
    
    app_with_db.dependency_overrides[get_current_user] = mock_current_user
    yield
    app_with_db.dependency_overrides.pop(get_current_user, None)


@pytest.mark.asyncio
async def test_get_todays_sessions(async_client: AsyncClient, setup_query_data: dict, override_auth: None):
    # Pass today's date implicitly
    resp = await async_client.get(f"{DELIVERY_PREFIX}/sessions/today")
    if resp.status_code != 200:
        print(resp.text)
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) >= 1
    session_data = next(s for s in data if s["session_id"] == str(setup_query_data["session_id_1"]))
    assert session_data["course_title"] == "Test Course"
    assert session_data["batch_name"] == "Test Batch"
    assert session_data["assigned_student_count"] == 2
    assert session_data["attendance_submitted_at"] is None


@pytest.mark.asyncio
async def test_get_batch_overview(async_client: AsyncClient, setup_query_data: dict, override_auth: None):
    batch_id = setup_query_data["batch_id"]
    resp = await async_client.get(f"{DELIVERY_PREFIX}/batches/{batch_id}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["batch_id"] == str(batch_id)
    assert data["course_title"] == "Test Course"
    assert data["assigned_student_count"] == 2
    assert data["next_session_id"] == str(setup_query_data["session_id_1"])


@pytest.mark.asyncio
async def test_get_batch_roster(async_client: AsyncClient, setup_query_data: dict, override_auth: None):
    batch_id = setup_query_data["batch_id"]
    resp = await async_client.get(f"{DELIVERY_PREFIX}/batches/{batch_id}/roster")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 2
    names = {s["name"] for s in data}
    assert names == {"Student A", "Student B"}


@pytest.mark.asyncio
async def test_get_session_attendance_sheet(async_client: AsyncClient, setup_query_data: dict, override_auth: None):
    # Session 2 has attendance submitted
    session_id = setup_query_data["session_id_2"]
    resp = await async_client.get(f"{DELIVERY_PREFIX}/sessions/{session_id}/attendance")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 2
    
    student_1_rec = next(s for s in data if s["student_id"] == str(setup_query_data["student_1"]))
    assert student_1_rec["status"] == "PRESENT"

    student_2_rec = next(s for s in data if s["student_id"] == str(setup_query_data["student_2"]))
    assert student_2_rec["status"] == "ABSENT"


@pytest.mark.asyncio
async def test_get_batch_attendance_summary(async_client: AsyncClient, setup_query_data: dict, override_auth: None):
    batch_id = setup_query_data["batch_id"]
    resp = await async_client.get(f"{DELIVERY_PREFIX}/batches/{batch_id}/attendance-summary")
    assert resp.status_code == 200
    data = resp.json()
    
    # Should only return Session 2 because it has attendance_submitted_at
    assert len(data) == 1
    assert data[0]["session_id"] == str(setup_query_data["session_id_2"])
    assert data[0]["present_count"] == 1
    assert data[0]["absent_count"] == 1
    assert data[0]["attendance_submitted_at"] is not None
