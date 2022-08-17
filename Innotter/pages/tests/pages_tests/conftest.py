import pytest
from users.models import User
from model_bakery import baker
from pages.models import Page


@pytest.fixture
def page(user: User):
    return baker.make(Page)


@pytest.fixture
def new_page():
    return baker.prepare(Page)
