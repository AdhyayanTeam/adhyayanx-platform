import asyncio
import uuid
from datetime import datetime, UTC, date
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from app.infrastructure.postgres.tables import Base
import app.infrastructure.postgres.academy_tables

from app.modules.platform.identity.password_policy import PasswordPolicy

DB_URL = "postgresql+asyncpg://postgres:postgres@localhost:5433/adx"

async def seed():
    engine = create_async_engine(DB_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

        # Create Organization
        org_id = uuid.uuid4()
        await conn.execute(
            text("""
                INSERT INTO organizations (id, name, slug, timezone, lifecycle_state)
                VALUES (:id, 'Test Academy', 'test-academy', 'Asia/Kolkata', 'ACTIVE')
            """),
            {"id": org_id}
        )

        # Create User
        user_id = uuid.uuid4()
        pw_hash = PasswordPolicy().hash_password("password123")
        await conn.execute(
            text("""
                INSERT INTO users (id, organization_id, email, password_hash, role)
                VALUES (:id, :org_id, 'admin@test.com', :pw, 'admin')
            """),
            {"id": user_id, "org_id": org_id, "pw": pw_hash}
        )

        # Create Course & Batch
        course_id = uuid.uuid4()
        await conn.execute(
            text("INSERT INTO academy_courses (id, organization_id, title) VALUES (:id, :oid, 'Full Stack Dev')"),
            {"id": course_id, "oid": org_id}
        )
        
        batch_id = uuid.uuid4()
        await conn.execute(
            text("INSERT INTO academy_batches (id, organization_id, course_id, name) VALUES (:id, :oid, :cid, 'June Evening')"),
            {"id": batch_id, "oid": org_id, "cid": course_id}
        )

        # Students and Assignments
        student_ids = []
        for i in range(5):
            sid = uuid.uuid4()
            student_ids.append(sid)
            await conn.execute(
                text("INSERT INTO academy_students (id, organization_id, name, email) VALUES (:id, :oid, :name, :email)"),
                {"id": sid, "oid": org_id, "name": f"Student {i}", "email": f"s{i}@test.com"}
            )
            # Enrollment
            eid = uuid.uuid4()
            await conn.execute(
                text("INSERT INTO academy_enrollments (id, organization_id, student_id, course_id, status) VALUES (:id, :oid, :sid, :cid, 'ACTIVE')"),
                {"id": eid, "oid": org_id, "sid": sid, "cid": course_id}
            )
            # Batch Assignment
            await conn.execute(
                text("INSERT INTO academy_batch_assignments (id, organization_id, enrollment_id, batch_id, assigned_at) VALUES (:id, :oid, :eid, :bid, :at)"),
                {"id": uuid.uuid4(), "oid": org_id, "eid": eid, "bid": batch_id, "at": datetime(2026, 1, 1, tzinfo=UTC)}
            )

        # Session for today
        session_id = uuid.uuid4()
        today = date.today()
        # Set it to happen right now
        starts_at = datetime.combine(today, datetime.now().time()).replace(tzinfo=UTC)
        ends_at = starts_at
        
        await conn.execute(
            text("""
                INSERT INTO academy_sessions (id, organization_id, batch_id, starts_at, ends_at, attendance_submitted_at)
                VALUES (:id, :oid, :bid, :starts_at, :ends_at, NULL)
            """),
            {"id": session_id, "oid": org_id, "bid": batch_id, "starts_at": starts_at, "ends_at": ends_at}
        )
        
        # Outbox table
        await conn.execute(text("""
            CREATE TABLE IF NOT EXISTS event_outbox (
                id UUID PRIMARY KEY,
                aggregate_type VARCHAR,
                aggregate_id UUID,
                event_type VARCHAR,
                payload JSONB,
                published BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            )
        """))

    print("DB Seeded!")
    print(f"Login: admin@test.com / password123")

if __name__ == "__main__":
    asyncio.run(seed())
