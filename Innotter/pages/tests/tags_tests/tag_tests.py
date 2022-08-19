import pytest
from unittest import mock
from pages.tests.users_tests.conftest import user
from pages.models import Tag
from rest_framework.test import APIRequestFactory, force_authenticate
from pages.views.tag_views import TagViewSet
from users.auth import generate_access_token
from pages.serializers.tag_serializers import TagSerializer

pytestmark = pytest.mark.django_db

default_viewset = TagViewSet.as_view(
    {"get": "retrieve", "post": "create", "delete": "destroy"}
)
list_viewset = TagViewSet.as_view({"get": "list"})


class TestTagLogic:
    url = "resource/tags/"

    @mock.patch("Innotter.settings.SECRET_KEY", "1")
    def test_create_tag(self, user: user, api_factory: APIRequestFactory):
        request = api_factory.post(f"{self.url}", {'name': "test tag"})
        token = generate_access_token(user)
        force_authenticate(request=request, user=user, token=token)
        response = default_viewset(request)

        assert response.status_code == 201 and response.data == TagSerializer(Tag.objects.first()).data
