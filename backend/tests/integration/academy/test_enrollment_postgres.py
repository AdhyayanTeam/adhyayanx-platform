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
