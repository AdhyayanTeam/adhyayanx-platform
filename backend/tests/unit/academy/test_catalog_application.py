import pytest
from uuid import uuid4
from fastapi.testclient import TestClient
from pydantic import ValidationError as PydanticValidationError

from app.foundation.exceptions.base import AuthorizationError, ValidationError
from app.modules.blueprints.academy.catalog.domain.models import Course, CourseLifecycleState
from app.modules.blueprints.academy.catalog.api.router import CreateCourseRequest

def test_domain_invariants():
    # Arrange
    course = Course(
        id=uuid4(),
        organization_id=uuid4(),
        title="Test Course",
        description="A course",
        lifecycle_state=CourseLifecycleState.ARCHIVED,
    )

    # Act & Assert
    with pytest.raises(ValidationError, match="Only draft courses can be published"):
        course.publish()
        
    course.lifecycle_state = CourseLifecycleState.DRAFT
    course.publish()
    assert course.lifecycle_state == CourseLifecycleState.PUBLISHED
    
    with pytest.raises(ValidationError, match="Only draft courses can be published"):
        course.publish()

def test_rbac_boundary_for_catalog_service():
    from app.modules.blueprints.academy.catalog.application.service import CatalogService
    
    # We can test the service layer directly for RBAC
    class DummyPublisher:
        pass
        
    class DummyDB:
        pass
        
    service = CatalogService(database=DummyDB(), publisher=DummyPublisher()) # type: ignore
    
    with pytest.raises(AuthorizationError, match="Only owners and admins can manage courses"):
        service._require_admin(roles=["member"])
        
    # Should not raise
    service._require_admin(roles=["admin"])
    service._require_admin(roles=["owner"])

def test_schema_extra_field_rejection():
    # The client payload is strictly validated
    with pytest.raises(PydanticValidationError) as exc:
        CreateCourseRequest(
            title="Python Fundamentals",
            description="Learn Python",
            organization_id="1234-spoofed-org" # type: ignore
        )
        
    assert "Extra inputs are not permitted" in str(exc.value)
