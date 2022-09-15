import pytest
from pages.models import Post
from pages.tests.pages_tests.conftest import page
from model_bakery import baker


@pytest.fixture
def post(page: page):
    return baker.make(Post, page=page)


@pytest.fixture
def posts(page: page):
    return baker.make(Post, page=page, _quantity=150)
