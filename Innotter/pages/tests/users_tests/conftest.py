import pytest
from users.models import User
from model_bakery import baker


@pytest.fixture()
def user():
    return baker.make(User, role="admin")


@pytest.fixture()
def new_user():
    return baker.prepare(User)