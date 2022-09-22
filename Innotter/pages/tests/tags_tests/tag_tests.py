import pytest
from unittest import mock
from pages.tests.users_tests.conftest import user
from pages.models import Tag
from rest_framework.test import APIRequestFactory, force_authenticate
from pages.tests.tags_tests.conftest import tag, tags
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

    def test_create_tag(self, user: user, api_factory: APIRequestFactory):
        request = api_factory.post(f"{self.url}", {'name': "test tag"})
        token = generate_access_token(user)
        force_authenticate(request=request, user=user, token=token)
        response = default_viewset(request)

        assert response.status_code == 201 and response.data == TagSerializer(Tag.objects.first()).data

    def test_destroy_tag(self, user: user, tag: tag, api_factory: APIRequestFactory):
        assert len(Tag.objects.all()) == 1 and Tag.objects.first() == tag
        request = api_factory.delete(f"{self.url}{tag.pk}")
        token = generate_access_token(user)
        force_authenticate(request=request, user=user, token=token)
        response = default_viewset(request, pk=tag.pk)

        assert response.status_code == 204 and len(Tag.objects.all()) == 0

    def test_retrieve_tag(self, user: user, tag: tag, api_factory: APIRequestFactory):
        request = api_factory.get(f"{self.url}{tag.pk}")
        token = generate_access_token(user)
        force_authenticate(request=request, user=user, token=token)
        response = default_viewset(request, pk=tag.pk)

        assert response.status_code == 200 and response.data == TagSerializer(tag).data

    def test_list_tags(self, user: user, tags: tags, api_factory: APIRequestFactory):
        request = api_factory.get(f"{self.url}")
        token = generate_access_token(user)
        force_authenticate(request=request, user=user, token=token)
        response = list_viewset(request)

        assert response.status_code == 200 and len(response.data) == len(tags)
        assert response.data == TagSerializer(tags, many=True).data
