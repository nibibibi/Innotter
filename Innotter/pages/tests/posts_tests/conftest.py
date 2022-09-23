import pytest
from model_bakery import baker

from pages.models import Post
from pages.tests.pages_tests.conftest import page


@pytest.fixture
def post(page: page):
    return baker.make(Post, page=page)


@pytest.fixture
def posts(page: page):
    return baker.make(Post, page=page, _quantity=150)
