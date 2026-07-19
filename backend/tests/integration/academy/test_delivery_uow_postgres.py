import pytest
from datetime import datetime, UTC
from uuid import uuid4

from app.modules.blueprints.academy.delivery.infrastructure.postgres_uow import PostgresDeliveryUnitOfWork
from app.modules.blueprints.academy.delivery.domain.events import AttendanceSubmitted
from app.infrastructure.postgres.tables import OutboxTable
from sqlalchemy import select

# We need to import the fixtures from test_catalog_postgres so they are available
from tests.integration.academy.test_catalog_postgres import (
    real_settings, real_database, app_with_db
)

@pytest.fixture
def uow_factory(app_with_db):
    from app.modules.blueprints.academy.delivery.application.uow import DeliveryUnitOfWork
    
    def _factory() -> PostgresDeliveryUnitOfWork:
        return app_with_db.state.container.resolve(DeliveryUnitOfWork)
    return _factory

@pytest.mark.asyncio
async def test_uow_explicit_commit_persists_state_and_events(uow_factory, real_database):
    uow = uow_factory()
    organization_id = uuid4()
    session_id = uuid4()
    
    # Arrange an event
    event = AttendanceSubmitted(
        aggregate_type="academy.delivery.session",
        aggregate_id=session_id,
        organization_id=str(organization_id),
        session_id=str(session_id),
        batch_id=str(uuid4()),
        submitted_by=str(uuid4()),
        record_count=1,
        present_count=1,
        absent_count=0,
        occurred_at=datetime.now(UTC)
    )

    # Act
    async with uow:
        # We don't save full state here to keep it simple, just verifying the transaction mechanisms
        uow.record(event)
        await uow.commit()
        
    # Assert
    async with real_database.session() as db_session:
        stmt = select(OutboxTable).where(OutboxTable.aggregate_id == session_id)
        result = await db_session.execute(stmt)
        rows = result.scalars().all()
        assert len(rows) == 1
        assert rows[0].event_type == "academy.delivery.AttendanceSubmitted"

@pytest.mark.asyncio
async def test_uow_no_commit_results_in_rollback(uow_factory, real_database):
    uow = uow_factory()
    session_id = uuid4()
    
    event = AttendanceSubmitted(
        aggregate_type="academy.delivery.session",
        aggregate_id=session_id,
        organization_id=str(uuid4()),
        session_id=str(session_id),
        batch_id=str(uuid4()),
        submitted_by=str(uuid4()),
        record_count=1,
        present_count=1,
        absent_count=0,
        occurred_at=datetime.now(UTC)
    )

    # Act - NO commit
    async with uow:
        uow.record(event)
        
    # Assert
    async with real_database.session() as db_session:
        stmt = select(OutboxTable).where(OutboxTable.aggregate_id == session_id)
        result = await db_session.execute(stmt)
        assert len(result.fetchall()) == 0

@pytest.mark.asyncio
async def test_uow_exception_results_in_rollback(uow_factory, real_database):
    uow = uow_factory()
    session_id = uuid4()
    
    event = AttendanceSubmitted(
        aggregate_type="academy.delivery.session",
        aggregate_id=session_id,
        organization_id=str(uuid4()),
        session_id=str(session_id),
        batch_id=str(uuid4()),
        submitted_by=str(uuid4()),
        record_count=1,
        present_count=1,
        absent_count=0,
        occurred_at=datetime.now(UTC)
    )

    # Act - Exception before commit
    with pytest.raises(ValueError, match="Business exception"):
        async with uow:
            uow.record(event)
            raise ValueError("Business exception")
            
    # Assert
    async with real_database.session() as db_session:
        stmt = select(OutboxTable).where(OutboxTable.aggregate_id == session_id)
        result = await db_session.execute(stmt)
        assert len(result.fetchall()) == 0

@pytest.mark.asyncio
async def test_uow_cross_module_query_shares_same_session(uow_factory):
    uow = uow_factory()
    
    async with uow:
        assert uow.enrollment_query._session is uow._session
