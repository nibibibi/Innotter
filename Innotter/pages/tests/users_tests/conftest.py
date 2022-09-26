import pytest
from model_bakery import baker
from users.models import User


@pytest.fixture()
def user():
    return baker.make(User, role="admin")


@pytest.fixture()
def new_user():
    return baker.prepare(User)
