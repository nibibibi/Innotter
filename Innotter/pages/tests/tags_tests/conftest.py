import pytest
from model_bakery import baker

from pages.models import Tag


@pytest.fixture
def tag():
    return baker.make(Tag)


@pytest.fixture
def tags():
    return baker.make(Tag, _quantity=150)
