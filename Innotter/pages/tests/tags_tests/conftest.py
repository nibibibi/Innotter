import pytest
from model_bakery import baker
from pages.models import Tag

@pytest.fixture
def tag():
    return baker.make(Tag)