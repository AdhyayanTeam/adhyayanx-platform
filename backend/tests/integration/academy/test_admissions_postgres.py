import pytest
from uuid import uuid4
from datetime import datetime, UTC

from app.modules.blueprints.academy.admissions.domain.entities import Lead, Enquiry, EnquiryStatus, EnquirySource
from app.modules.blueprints.academy.admissions.application.service import AdmissionsService, AdmitEnquiryCommand
from app.modules.blueprints.academy.admissions.infrastructure.postgres_uow import PostgresAdmissionsUnitOfWork
from app.infrastructure.postgres.academy_tables import StudentTable, EnrollmentTable, LeadModel, EnquiryModel
from sqlalchemy import select

from tests.integration.academy.test_catalog_postgres import real_settings, real_database
from app.infrastructure.postgres.database import Database
from app.infrastructure.postgres.tables import OrganizationTable
from app.infrastructure.postgres.academy_tables import CourseTable

@pytest.fixture
async def real_session(real_database: Database):
    session = real_database.session_factory()
    await session.begin()
    yield session
    await session.rollback()
    await session.close()

@pytest.fixture
def org_id():
    return uuid4()

@pytest.fixture
async def uow(real_database: Database):
    from app.modules.platform.events.publisher import Publisher
    class DummyOutbox:
        async def append(self, entry): pass
    return PostgresAdmissionsUnitOfWork(real_database, Publisher(lambda s: DummyOutbox()))

@pytest.fixture
async def service(uow):
    return AdmissionsService(uow)

async def setup_test_data(session, org_id, course_id):
    org = OrganizationTable(id=org_id, name="Test Org", slug=str(org_id), timezone="UTC")
    session.add(org)
    await session.flush()
    
    course = CourseTable(id=course_id, organization_id=org_id, title="Full Stack", lifecycle_state="active")
    session.add(course)
    await session.flush()

@pytest.mark.asyncio
async def test_new_prospect_admission(real_session, service, uow, org_id):
    lead_id = uuid4()
    enquiry_id = uuid4()
    course_id = uuid4()
    admitted_by = uuid4()

    await setup_test_data(real_session, org_id, course_id)

    lead = LeadModel(id=lead_id, organization_id=org_id, first_name="Alice", phone="1234567890", email="alice@test.com")
    real_session.add(lead)
    await real_session.flush()

    enquiry = EnquiryModel(
        id=enquiry_id,
        organization_id=org_id,
        lead_id=lead_id,
        course_id=course_id,
        status=EnquiryStatus.NEW.value,
        source=EnquirySource.WEBSITE.value
    )
    real_session.add(enquiry)
    await real_session.commit()

    cmd = AdmitEnquiryCommand(
        organization_id=org_id,
        enquiry_id=enquiry_id,
        admitted_by=admitted_by,
    )
    await service.admit_enquiry(cmd)

    real_session.expire_all()

    student = (await real_session.execute(select(StudentTable).where(StudentTable.organization_id == org_id, StudentTable.phone == "1234567890"))).scalar_one()
    assert student.name == "Alice"
    
    # Assert enrollment created
    enrollment = (await real_session.execute(select(EnrollmentTable).where(EnrollmentTable.student_id == student.id))).scalar_one()
    assert enrollment.course_id == course_id

    # Assert enquiry status updated
    enquiry = (await real_session.execute(select(EnquiryModel).where(EnquiryModel.id == enquiry_id))).scalar_one()
    assert enquiry.status == EnquiryStatus.ADMITTED.value
    assert enquiry.admitted_at is not None

@pytest.mark.asyncio
async def test_existing_student_admission(real_session, service, org_id):
    # Setup
    lead_id = uuid4()
    enquiry_id = uuid4()
    course_id = uuid4()
    student_id = uuid4()
    
    await setup_test_data(real_session, org_id, course_id)

    # Existing student
    student = StudentTable(id=student_id, organization_id=org_id, name="Bob", phone="9876543210", email="bob@test.com")
    real_session.add(student)
    await real_session.flush()

    # Lead with same phone
    lead = LeadModel(id=lead_id, organization_id=org_id, first_name="Bob", phone="9876543210", email="bob@test.com")
    real_session.add(lead)
    await real_session.flush()

    enquiry = EnquiryModel(
        id=enquiry_id,
        organization_id=org_id,
        lead_id=lead_id,
        course_id=course_id,
        status=EnquiryStatus.FOLLOW_UP.value,
        source=EnquirySource.WALKIN.value
    )
    real_session.add(enquiry)
    await real_session.commit()

    cmd = AdmitEnquiryCommand(organization_id=org_id, enquiry_id=enquiry_id, admitted_by=uuid4())
    await service.admit_enquiry(cmd)

    real_session.expire_all()

    students = (await real_session.execute(select(StudentTable).where(StudentTable.organization_id == org_id, StudentTable.phone == "9876543210"))).scalars().all()
    assert len(students) == 1
    assert students[0].id == student_id

    # Should create enrollment
    enrollment = (await real_session.execute(select(EnrollmentTable).where(EnrollmentTable.student_id == student_id))).scalar_one()
    assert enrollment.course_id == course_id

@pytest.mark.asyncio
async def test_rollback_on_failure(real_session, uow, org_id):
    # We will simulate a failure during admit_enquiry by raising an exception manually
    # or by injecting a faulty dependency.
    pass

@pytest.mark.asyncio
async def test_duplicate_admission_fails(real_session, service, org_id):
    lead_id = uuid4()
    enquiry_id = uuid4()
    course_id = uuid4()

    await setup_test_data(real_session, org_id, course_id)

    lead = LeadModel(id=lead_id, organization_id=org_id, first_name="Charlie", phone="555", email="charlie@test.com")
    real_session.add(lead)
    await real_session.flush()

    enquiry = EnquiryModel(
        id=enquiry_id,
        organization_id=org_id,
        lead_id=lead_id,
        course_id=course_id,
        status=EnquiryStatus.ADMITTED.value, # Already admitted!
        source=EnquirySource.WEBSITE.value
    )
    real_session.add(enquiry)
    await real_session.commit()

    cmd = AdmitEnquiryCommand(organization_id=org_id, enquiry_id=enquiry_id, admitted_by=uuid4())
    with pytest.raises(ValueError, match="Enquiry cannot be admitted"):
        await service.admit_enquiry(cmd)
