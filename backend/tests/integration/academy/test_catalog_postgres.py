import pytest
import asyncio
from uuid import uuid4
import httpx
from fastapi import FastAPI
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.main import create_app
from app.kernel.config.loader import Settings
from app.infrastructure.postgres.database import Database
from app.api.dependencies import get_current_user
from app.modules.platform.events.publisher import Publisher
from app.infrastructure.postgres.academy_tables import CourseTable

# Fixtures for real DB integration
@pytest.fixture
def real_settings() -> Settings:
    return Settings()

from app.infrastructure.postgres.tables import Base

@pytest.fixture
async def real_database(real_settings: Settings) -> Database:
    db = Database(real_settings)
    
    # Ensure tables are created for tests
    print("TABLES IN METADATA:", Base.metadata.tables.keys())
    async with db.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    yield db
    
    # Optionally drop tables or leave them
    # async with db.engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
async def app_with_db(real_settings: Settings, real_database: Database):
    app = create_app(real_settings)
    app.state.container._instances[Database] = real_database
    
    # We will clear dependency overrides for each test
    app.dependency_overrides = {}
    yield app

@pytest.fixture
async def async_client(app_with_db: FastAPI):
    transport = httpx.ASGITransport(app=app_with_db)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as c:
        yield c

PREFIX = "/api/v1/academy/catalog"

def set_current_user(app: FastAPI, org_id: str, roles: list[str]):
    async def mock_get_current_user():
        return {
            "organization": {"id": org_id, "slug": "test-org"},
            "user": {"id": str(uuid4()), "email": "test@example.com"},
            "roles": roles
        }
    app.dependency_overrides[get_current_user] = mock_get_current_user

async def create_test_organization(db: Database, org_id: str):
    from app.infrastructure.postgres.tables import OrganizationTable
    async with db.session() as session:
        session.add(OrganizationTable(id=org_id, name="Test Org", slug=f"test-org-{org_id}"))

@pytest.mark.asyncio
async def test_lifecycle_and_persistence(async_client: httpx.AsyncClient, app_with_db: FastAPI, real_database: Database):
    org_id = str(uuid4())
    await create_test_organization(real_database, org_id)
    set_current_user(app_with_db, org_id, ["owner"])
    
    # Create
    resp = await async_client.post(f"{PREFIX}/courses", json={"title": "Real PG Course"})
    assert resp.status_code == 200
    course_id = resp.json()["id"]
    
    # List
    resp = await async_client.get(f"{PREFIX}/courses")
    assert resp.status_code == 200
    items = resp.json()
    assert any(c["id"] == course_id for c in items)
    
    # Publish
    resp = await async_client.post(f"{PREFIX}/courses/{course_id}/publish")
    assert resp.status_code == 200
    assert resp.json()["lifecycle_state"] == "published"
    
    # Archive
    resp = await async_client.post(f"{PREFIX}/courses/{course_id}/archive")
    assert resp.status_code == 200
    assert resp.json()["lifecycle_state"] == "archived"


@pytest.mark.asyncio
async def test_tenant_isolation(async_client: httpx.AsyncClient, app_with_db: FastAPI, real_database: Database):
    org_a = str(uuid4())
    org_b = str(uuid4())
    
    await create_test_organization(real_database, org_a)
    await create_test_organization(real_database, org_b)
    
    # User in Org A creates a course
    set_current_user(app_with_db, org_a, ["owner"])
    resp = await async_client.post(f"{PREFIX}/courses", json={"title": "Org A Course"})
    assert resp.status_code == 200
    course_id = resp.json()["id"]
    
    # Switch to User in Org B
    set_current_user(app_with_db, org_b, ["owner"])
    
    # Read Isolation: Org B should not see Org A's course in list
    resp = await async_client.get(f"{PREFIX}/courses")
    assert not any(c["id"] == course_id for c in resp.json())
    
    # Write Isolation / Not-Found Boundary: Org B cannot publish Org A's course
    resp = await async_client.post(f"{PREFIX}/courses/{course_id}/publish")
    assert resp.status_code == 422
    assert "Course not found" in resp.text

@pytest.mark.asyncio
async def test_membership_integration(async_client: httpx.AsyncClient, app_with_db: FastAPI, real_database: Database):
    # This proves that our router explicitly relies on the platform context for both Tenant ID and roles.
    org_id = str(uuid4())
    await create_test_organization(real_database, org_id)
    
    # Membership 1: Member
    set_current_user(app_with_db, org_id, ["member"])
    resp = await async_client.post(f"{PREFIX}/courses", json={"title": "Fail Course"})
    assert resp.status_code == 403
    
    # Membership 2: Admin
    set_current_user(app_with_db, org_id, ["admin"])
    resp = await async_client.post(f"{PREFIX}/courses", json={"title": "Success Course"})
    assert resp.status_code == 200


@pytest.mark.asyncio
async def test_transactional_outbox_atomicity_and_rollback(async_client: httpx.AsyncClient, app_with_db: FastAPI, real_database: Database, monkeypatch: pytest.MonkeyPatch):
    org_id = str(uuid4())
    await create_test_organization(real_database, org_id)
    set_current_user(app_with_db, org_id, ["owner"])
    
    # Atomicity: Success Case
    resp = await async_client.post(f"{PREFIX}/courses", json={"title": "Atomic Success"})
    assert resp.status_code == 200
    course_id = resp.json()["id"]
    
    # Verify DB directly
    async with real_database.session() as session:
        # Check course
        result = await session.execute(select(CourseTable).where(CourseTable.id == course_id))
        assert result.scalar_one_or_none() is not None
        
        # Check outbox
        result = await session.execute(text("SELECT id, aggregate_id, event_type FROM event_outbox WHERE aggregate_id = :agg_id"), {"agg_id": course_id})
        outbox_rows = result.fetchall()
        assert len(outbox_rows) == 1
        assert outbox_rows[0].event_type == "academy.course.created"
        
    
    # Rollback: Failure Case
    # We will monkeypatch Publisher.publish to raise an exception *inside* the transaction block.
    # This proves that if outbox insertion fails, the course is also rolled back.
    
    original_publish = Publisher.publish
    
    async def failing_publish(*args, **kwargs):
        raise RuntimeError("Simulated Database/Outbox Failure")
        
    monkeypatch.setattr(Publisher, "publish", failing_publish)
    
    # Create request that will fail
    with pytest.raises(RuntimeError, match="Simulated Database/Outbox Failure"):
        await async_client.post(f"{PREFIX}/courses", json={"title": "Atomic Fail"})
        
    # Verify DB directly - neither should exist
    async with real_database.session() as session:
        # We don't have the course ID since it failed, but we can check if a course named "Atomic Fail" exists
        result = await session.execute(select(CourseTable).where(CourseTable.title == "Atomic Fail"))
        assert result.scalar_one_or_none() is None
        
        # We can also check that no outbox events exist for that payload (we can't easily query payload json inside sqlite/pg simply here, but the lack of course row is the primary rollback proof)
