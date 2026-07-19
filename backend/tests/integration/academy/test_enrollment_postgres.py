import pytest
import httpx
from uuid import uuid4
from fastapi import FastAPI
from sqlalchemy import text

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

@pytest.mark.asyncio
async def test_enrollment_happy_path(async_client: httpx.AsyncClient, app_with_db: FastAPI, real_database: Database):
    org_id = str(uuid4())
    await create_test_organization(real_database, org_id)
    set_current_user(app_with_db, org_id, ["owner"])

    # 1. Create Course
    course_resp = await async_client.post(f"{PREFIX}/catalog/courses", json={"title": "Full Stack", "description": "Web Dev"})
    assert course_resp.status_code == 200
    course_id = course_resp.json()["id"]

    # 2. Create Student
    student_resp = await async_client.post(f"{PREFIX}/students", json={"name": "Alice", "email": "alice@example.com"})
    assert student_resp.status_code == 201
    student_id = student_resp.json()["id"]

    # 3. Create Batch
    batch_resp = await async_client.post(f"{PREFIX}/delivery/batches", json={"course_id": course_id, "name": "June Batch"})
    assert batch_resp.status_code == 201
    batch_id = batch_resp.json()["id"]

    # 4. Enroll Student
    enroll_resp = await async_client.post(f"{PREFIX}/enrollments", json={"student_id": student_id, "course_id": course_id})
    assert enroll_resp.status_code == 201
    enrollment_id = enroll_resp.json()["id"]

    # 5. Assign Batch
    assign_resp = await async_client.post(f"{PREFIX}/enrollments/{enrollment_id}/assign", json={"batch_id": batch_id})
    assert assign_resp.status_code == 200
    
    # Verify in DB
    async with real_database.session() as session:
        result = await session.execute(text("SELECT status FROM academy_enrollments WHERE id = :id"), {"id": enrollment_id})
        assert result.scalar_one_or_none() == "active"
        
        assign_result = await session.execute(text("SELECT batch_id FROM academy_batch_assignments WHERE enrollment_id = :id"), {"id": enrollment_id})
        assert str(assign_result.scalar_one_or_none()) == batch_id
        
        # Verify Outbox Events
        outbox_result = await session.execute(
            text("SELECT event_type FROM event_outbox WHERE aggregate_id = :agg_id ORDER BY created_at ASC"), 
            {"agg_id": enrollment_id}
        )
        events = [row.event_type for row in outbox_result.fetchall()]
        assert "academy.enrollment.StudentEnrolled" in events
        assert "academy.enrollment.StudentAssignedToBatch" in events


@pytest.mark.asyncio
async def test_enrollment_wrong_course(async_client: httpx.AsyncClient, app_with_db: FastAPI, real_database: Database):
    org_id = str(uuid4())
    await create_test_organization(real_database, org_id)
    set_current_user(app_with_db, org_id, ["owner"])

    # Courses
    c1_resp = await async_client.post(f"{PREFIX}/catalog/courses", json={"title": "Course A"})
    course_a_id = c1_resp.json()["id"]
    
    c2_resp = await async_client.post(f"{PREFIX}/catalog/courses", json={"title": "Course B"})
    course_b_id = c2_resp.json()["id"]

    # Student
    s_resp = await async_client.post(f"{PREFIX}/students", json={"name": "Bob", "email": "bob@example.com"})
    student_id = s_resp.json()["id"]

    # Batch for Course B
    b_resp = await async_client.post(f"{PREFIX}/delivery/batches", json={"course_id": course_b_id, "name": "Batch B"})
    batch_b_id = b_resp.json()["id"]

    # Enroll in Course A
    e_resp = await async_client.post(f"{PREFIX}/enrollments", json={"student_id": student_id, "course_id": course_a_id})
    enrollment_id = e_resp.json()["id"]

    # Assign to Batch B (Should Fail)
    assign_resp = await async_client.post(f"{PREFIX}/enrollments/{enrollment_id}/assign", json={"batch_id": batch_b_id})
    assert assign_resp.status_code == 422
    assert "different course" in assign_resp.text


@pytest.mark.asyncio
async def test_enrollment_wrong_tenant(async_client: httpx.AsyncClient, app_with_db: FastAPI, real_database: Database):
    org_a = str(uuid4())
    org_b = str(uuid4())
    await create_test_organization(real_database, org_a)
    await create_test_organization(real_database, org_b)

    # Org B sets up a course and batch
    set_current_user(app_with_db, org_b, ["owner"])
    c_resp = await async_client.post(f"{PREFIX}/catalog/courses", json={"title": "Org B Course"})
    course_b_id = c_resp.json()["id"]
    b_resp = await async_client.post(f"{PREFIX}/delivery/batches", json={"course_id": course_b_id, "name": "Org B Batch"})
    batch_b_id = b_resp.json()["id"]

    # Org A sets up a student, course, and enrollment
    set_current_user(app_with_db, org_a, ["owner"])
    c2_resp = await async_client.post(f"{PREFIX}/catalog/courses", json={"title": "Org A Course"})
    course_a_id = c2_resp.json()["id"]
    
    s_resp = await async_client.post(f"{PREFIX}/students", json={"name": "Charlie", "email": "charlie@example.com"})
    student_a_id = s_resp.json()["id"]
    
    e_resp = await async_client.post(f"{PREFIX}/enrollments", json={"student_id": student_a_id, "course_id": course_a_id})
    enrollment_a_id = e_resp.json()["id"]

    # Org A tries to assign their enrollment to Org B's batch
    assign_resp = await async_client.post(f"{PREFIX}/enrollments/{enrollment_a_id}/assign", json={"batch_id": batch_b_id})
    
    # It should fail. Since our BatchQueryContract searches by context's organization_id, 
    # it won't even find Org B's batch!
    assert assign_resp.status_code == 422
    assert "Batch not found" in assign_resp.text

@pytest.mark.asyncio
async def test_enrollment_transactional_outbox_atomicity(async_client: httpx.AsyncClient, app_with_db: FastAPI, real_database: Database, monkeypatch: pytest.MonkeyPatch):
    org_id = str(uuid4())
    await create_test_organization(real_database, org_id)
    set_current_user(app_with_db, org_id, ["owner"])

    # Create prerequisites
    c_resp = await async_client.post(f"{PREFIX}/catalog/courses", json={"title": "Atomic Course"})
    course_id = c_resp.json()["id"]
    s_resp = await async_client.post(f"{PREFIX}/students", json={"name": "Atomic Student", "email": "atomic@example.com"})
    student_id = s_resp.json()["id"]

    from app.modules.platform.events.publisher import Publisher
    original_publish = Publisher.publish
    
    async def failing_publish(*args, **kwargs):
        raise RuntimeError("Simulated Database/Outbox Failure")
        
    monkeypatch.setattr(Publisher, "publish", failing_publish)
    
    # Try enrolling, it should fail
    with pytest.raises(RuntimeError, match="Simulated Database/Outbox Failure"):
        await async_client.post(f"{PREFIX}/enrollments", json={"student_id": student_id, "course_id": course_id})
        
    # Verify rollback
    async with real_database.session() as session:
        result = await session.execute(text("SELECT COUNT(*) FROM academy_enrollments WHERE student_id = :sid AND course_id = :cid"), {"sid": student_id, "cid": course_id})
        assert result.scalar_one() == 0

@pytest.mark.asyncio
async def test_student_and_enrollment_queries(async_client: httpx.AsyncClient, app_with_db: FastAPI, real_database: Database):
    org_id = str(uuid4())
    await create_test_organization(real_database, org_id)
    set_current_user(app_with_db, org_id, ["owner"])

    # 1. Create Course and Batches
    c_resp = await async_client.post(f"{PREFIX}/catalog/courses", json={"title": "Data Analytics"})
    course_id = c_resp.json()["id"]
    
    await async_client.post(f"{PREFIX}/delivery/batches", json={"course_id": course_id, "name": "Batch A"})
    b_resp = await async_client.post(f"{PREFIX}/delivery/batches", json={"course_id": course_id, "name": "Batch B"})
    batch_b_id = b_resp.json()["id"]

    # 2. Get Compatible Batches for Course
    batches_resp = await async_client.get(f"{PREFIX}/delivery/batches?course_id={course_id}")
    assert batches_resp.status_code == 200
    batches = batches_resp.json()
    assert len(batches) == 2
    assert any(b["batch_name"] == "Batch A" for b in batches)

    # 3. Create Student
    s_resp = await async_client.post(f"{PREFIX}/students", json={"name": "Diana", "email": "diana@example.com"})
    student_id = s_resp.json()["id"]

    # Verify Student Profile Query
    profile_resp = await async_client.get(f"{PREFIX}/students/{student_id}")
    assert profile_resp.status_code == 200
    assert profile_resp.json()["name"] == "Diana"

    # 4. Enroll Student
    e_resp = await async_client.post(f"{PREFIX}/enrollments", json={"student_id": student_id, "course_id": course_id})
    enrollment_id = e_resp.json()["id"]

    # Verify Enrollments Query (Not assigned yet)
    enrollments_resp = await async_client.get(f"{PREFIX}/students/{student_id}/enrollments")
    assert enrollments_resp.status_code == 200
    enrollments = enrollments_resp.json()
    assert len(enrollments) == 1
    assert enrollments[0]["course_title"] == "Data Analytics"
    assert enrollments[0]["current_batch_id"] is None

    # 5. Assign to Batch B
    await async_client.post(f"{PREFIX}/enrollments/{enrollment_id}/assign", json={"batch_id": batch_b_id})

    # Verify Enrollments Query (Assigned to Batch B)
    enrollments_resp = await async_client.get(f"{PREFIX}/students/{student_id}/enrollments")
    enrollments = enrollments_resp.json()
    assert enrollments[0]["current_batch_id"] == batch_b_id
    assert enrollments[0]["current_batch_name"] == "Batch B"

@pytest.mark.asyncio
async def test_batch_reassignment_preserves_history(async_client: httpx.AsyncClient, app_with_db: FastAPI, real_database: Database):
    org_id = str(uuid4())
    await create_test_organization(real_database, org_id)
    set_current_user(app_with_db, org_id, ["owner"])

    c_resp = await async_client.post(f"{PREFIX}/catalog/courses", json={"title": "Reassignment Course"})
    course_id = c_resp.json()["id"]
    
    b1_resp = await async_client.post(f"{PREFIX}/delivery/batches", json={"course_id": course_id, "name": "Batch 1"})
    batch_1_id = b1_resp.json()["id"]
    
    b2_resp = await async_client.post(f"{PREFIX}/delivery/batches", json={"course_id": course_id, "name": "Batch 2"})
    batch_2_id = b2_resp.json()["id"]

    s_resp = await async_client.post(f"{PREFIX}/students", json={"name": "Evan", "email": "evan@example.com"})
    student_id = s_resp.json()["id"]
    
    e_resp = await async_client.post(f"{PREFIX}/enrollments", json={"student_id": student_id, "course_id": course_id})
    enrollment_id = e_resp.json()["id"]

    # Assign Batch 1
    await async_client.post(f"{PREFIX}/enrollments/{enrollment_id}/assign", json={"batch_id": batch_1_id})

    # Reassign Batch 2
    await async_client.post(f"{PREFIX}/enrollments/{enrollment_id}/assign", json={"batch_id": batch_2_id})

    # Verify Enrollments Query shows Batch 2 as current
    enrollments_resp = await async_client.get(f"{PREFIX}/students/{student_id}/enrollments")
    assert enrollments_resp.status_code == 200
    enrollments = enrollments_resp.json()
    assert enrollments[0]["current_batch_id"] == batch_2_id
    assert enrollments[0]["current_batch_name"] == "Batch 2"

    # Verify history in DB
    async with real_database.session() as session:
        result = await session.execute(text("SELECT batch_id FROM academy_batch_assignments WHERE enrollment_id = :id ORDER BY assigned_at ASC"), {"id": enrollment_id})
        assignments = result.fetchall()
        assert len(assignments) == 2
        assert str(assignments[0][0]) == batch_1_id
        assert str(assignments[1][0]) == batch_2_id
