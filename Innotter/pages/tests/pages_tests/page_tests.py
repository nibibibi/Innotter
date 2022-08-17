from unittest import mock

from pages.models import Page
from model_bakery import baker
import pytest
from rest_framework.test import APIRequestFactory, force_authenticate
from pages.tests.pages_tests.conftest import new_page, page
from pages.tests.users_tests.conftest import user
from users.auth import generate_access_token
from pages.views.page_views import PageViewSet

pytestmark = pytest.mark.django_db
default_viewset = PageViewSet.as_view(
    {
        'post': "create",
        'get': "retrieve",
        'put': "update",
        'delete': "destroy"
    }
)
list_viewset = PageViewSet.as_view(
    {
        'get': "list"
    }
)


class TestPageLogic:
    url = "resource/pages/"

    @mock.patch("Innotter.settings.SECRET_KEY", "1")
    def test_create_page(self, user: user, new_page: new_page, api_factory: APIRequestFactory):
        serialized_page = {
            'uuid': new_page.uuid,
            'name': new_page.name,
            'description': new_page.description,
            'is_private': new_page.is_private,
            'owner': user.pk
        }

        request = api_factory.post(self.url, serialized_page)
        token = generate_access_token(user)
        force_authenticate(request=request, user=user, token=token)
        response = default_viewset(request)

        assert response.status_code == 201
        assert response.data.get('owner') == user.pk

    @mock.patch("Innotter.settings.SECRET_KEY", "1")
    def test_retrieve_page(self, user: user, page: page, api_factory: APIRequestFactory):
        request = api_factory.get(f"{self.url}{page.pk}/")
        token = generate_access_token(user)
        force_authenticate(request=request, user=user, token=token)
        response = default_viewset(request, pk=page.pk)

        assert response.status_code == 200
        assert response.data.get("id") == page.pk

    @mock.patch("Innotter.settings.SECRET_KEY", "1")
    def test_list_pages(self, user: user, api_factory: APIRequestFactory):
        baker.make(Page, _quantity=150)
        request = api_factory.get(self.url)
        token = generate_access_token(user)
        force_authenticate(request=request, user=user, token=token)
        response = list_viewset(request)
        assert response.status_code == 200
        assert len(response.data) == 150

    @mock.patch("Innotter.settings.SECRET_KEY", "1")
    def test_page_update(self, user: user, page: page, api_factory: APIRequestFactory):
        request_data = {
            'name': "newName",
            'uuid': "newUUID",
            'description': "newDescription"
        }
        page.owner = user
        page.save()
        request = api_factory.put(f"{self.url}{page.pk}", request_data)
        token = generate_access_token(user)
        force_authenticate(request=request, user=user, token=token)
        response = default_viewset(request, pk=page.pk)

        assert response.status_code == 200
        assert response.data == request_data
