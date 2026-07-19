import pytest
import httpx
from uuid import uuid4
from fastapi import FastAPI
from sqlalchemy import text
from datetime import datetime, UTC, timedelta

from app.infrastructure.postgres.database import Database
from tests.integration.academy.test_catalog_postgres import (
    create_test_organization, 
    set_current_user,
    async_client,
    app_with_db,
    real_database,
    real_settings,
)

PREFIX = "/api/v1/academy"
DELIVERY_PREFIX = "/api/v1/academy/delivery"

@pytest.fixture
async def setup_data(async_client: httpx.AsyncClient, app_with_db: FastAPI, real_database: Database):
    org_id = str(uuid4())
    await create_test_organization(real_database, org_id)
    set_current_user(app_with_db, org_id, ["owner"])

    # Create Course
    c_resp = await async_client.post(f"{PREFIX}/catalog/courses", json={"title": "Test Course"})
    course_id = c_resp.json()["id"]

    # Create Batch
    b_resp = await async_client.post(f"{DELIVERY_PREFIX}/batches", json={"name": "Test Batch", "course_id": course_id})
    batch_id = b_resp.json()["id"]

    # Create 5 Students and Enroll them
    student_ids = []
    for i in range(5):
        s_resp = await async_client.post(f"{PREFIX}/students", json={"name": f"Student {i}", "email": f"s{i}@test.com"})
        sid = s_resp.json()["id"]
        student_ids.append(sid)
        
        e_resp = await async_client.post(f"{PREFIX}/enrollments", json={"student_id": sid, "course_id": course_id})
        assert e_resp.status_code in (200, 201), e_resp.text
        eid = e_resp.json()["id"]
        
        a_resp = await async_client.post(f"{PREFIX}/enrollments/{eid}/assign", json={"batch_id": batch_id})
        assert a_resp.status_code in (200, 201), a_resp.text

    # Create unassigned student (enrolled in course, but not assigned to batch)
    s_resp = await async_client.post(f"{PREFIX}/students", json={"name": "Unassigned", "email": "u@test.com"})
    unassigned_id = s_resp.json()["id"]
    e_resp = await async_client.post(f"{PREFIX}/enrollments", json={"student_id": unassigned_id, "course_id": course_id})

    # Create Session
    now = datetime.now(UTC)
    s_resp = await async_client.post(
        f"{DELIVERY_PREFIX}/batches/{batch_id}/sessions",
        json={
            "starts_at": now.isoformat(),
            "ends_at": (now + timedelta(hours=2)).isoformat()
        }
    )
    session_id = s_resp.json()["id"]

    return {
        "org_id": org_id,
        "course_id": course_id,
        "batch_id": batch_id,
        "session_id": session_id,
        "student_ids": student_ids,
        "unassigned_id": unassigned_id
    }

@pytest.mark.asyncio
async def test_delivery_attendance_happy_path(async_client: httpx.AsyncClient, real_database: Database, setup_data: dict):
    session_id = setup_data["session_id"]
    student_ids = setup_data["student_ids"]
    org_id = setup_data["org_id"]

    # Submit Bulk Attendance
    records = [
        {"student_id": student_ids[0], "status": "PRESENT"},
        {"student_id": student_ids[1], "status": "PRESENT"},
        {"student_id": student_ids[2], "status": "PRESENT"},
        {"student_id": student_ids[3], "status": "ABSENT"},
    ]
    
    # DEBUG
    async with real_database.session() as s:
        res = await s.execute(text("SELECT to_regclass('academy_batch_assignments')"))
        print("TABLE EXISTS CHECK:", res.scalar_one_or_none())
        
    resp = await async_client.post(f"{DELIVERY_PREFIX}/sessions/{session_id}/attendance", json={"records": records})
    assert resp.status_code == 200, resp.text

    # Verify DB
    async with real_database.session() as db_session:
        result = await db_session.execute(
            text("SELECT COUNT(*) FROM academy_attendance_records WHERE session_id = :sid"),
            {"sid": session_id}
        )
        assert result.scalar_one() == 4
        
        # Verify Outbox
        outbox_result = await db_session.execute(
            text("SELECT data FROM event_outbox WHERE aggregate_id = :sid AND event_type = 'academy.delivery.AttendanceSubmitted'"),
            {"sid": session_id}
        )
        payload = outbox_result.scalar_one_or_none()
        assert payload is not None
        assert payload["record_count"] == 4
        assert payload["present_count"] == 3
        assert payload["absent_count"] == 1

    # Correct Attendance
    resp = await async_client.put(f"{DELIVERY_PREFIX}/sessions/{session_id}/attendance/{student_ids[3]}", json={"status": "PRESENT"})
    assert resp.status_code == 200

    # Verify Correction
    async with real_database.session() as db_session:
        result = await db_session.execute(
            text("SELECT status FROM academy_attendance_records WHERE session_id = :sid AND student_id = :stid"),
            {"sid": session_id, "stid": student_ids[3]}
        )
        assert result.scalar_one() == "PRESENT"

        # Verify Correction Outbox
        outbox_result = await db_session.execute(
            text("SELECT data FROM event_outbox WHERE aggregate_id = :sid AND event_type = 'academy.delivery.AttendanceCorrected'"),
            {"sid": session_id}
        )
        payload = outbox_result.scalar_one_or_none()
        assert payload is not None
        assert payload["previous_status"] == "ABSENT"
        assert payload["new_status"] == "PRESENT"


@pytest.mark.asyncio
async def test_delivery_attendance_mixed_validity_rollback(async_client: httpx.AsyncClient, real_database: Database, setup_data: dict):
    session_id = setup_data["session_id"]
    student_ids = setup_data["student_ids"]
    unassigned_id = setup_data["unassigned_id"]

    # Submit Bulk Attendance with one invalid student
    records = [
        {"student_id": student_ids[0], "status": "PRESENT"},
        {"student_id": student_ids[1], "status": "PRESENT"},
        {"student_id": unassigned_id, "status": "PRESENT"},  # Invalid: not in batch
    ]
    resp = await async_client.post(f"{DELIVERY_PREFIX}/sessions/{session_id}/attendance", json={"records": records})
    assert resp.status_code == 422
    assert "not enrolled in the batch" in resp.text

    # Verify Rollback
    async with real_database.session() as db_session:
        result = await db_session.execute(
            text("SELECT COUNT(*) FROM academy_attendance_records WHERE session_id = :sid"),
            {"sid": session_id}
        )
        assert result.scalar_one() == 0  # Entire transaction rolled back
        
        # Verify NO Outbox Events
        outbox_result = await db_session.execute(
            text("SELECT COUNT(*) FROM event_outbox WHERE aggregate_id = :sid"),
            {"sid": session_id}
        )
        assert outbox_result.scalar_one() == 0

@pytest.mark.asyncio
async def test_delivery_attendance_duplicates_rejected(async_client: httpx.AsyncClient, setup_data: dict):
    session_id = setup_data["session_id"]
    student_ids = setup_data["student_ids"]

    records = [
        {"student_id": student_ids[0], "status": "PRESENT"},
        {"student_id": student_ids[0], "status": "ABSENT"},
    ]
    resp = await async_client.post(f"{DELIVERY_PREFIX}/sessions/{session_id}/attendance", json={"records": records})
    assert resp.status_code == 422
    assert "Duplicate attendance submission" in resp.text

@pytest.mark.asyncio
async def test_delivery_attendance_cross_tenant_isolation(async_client: httpx.AsyncClient, app_with_db: FastAPI, real_database: Database, setup_data: dict):
    session_id = setup_data["session_id"]
    student_ids = setup_data["student_ids"]

    # Switch to Org B
    org_b_id = str(uuid4())
    await create_test_organization(real_database, org_b_id)
    set_current_user(app_with_db, org_b_id, ["owner"])

    # Try to access Org A's session
    records = [{"student_id": student_ids[0], "status": "PRESENT"}]
    resp = await async_client.post(f"{DELIVERY_PREFIX}/sessions/{session_id}/attendance", json={"records": records})
    
    assert resp.status_code == 422
    assert "Session not found" in resp.text
