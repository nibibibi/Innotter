from unittest import mock

import pytest
from rest_framework.test import APIRequestFactory, force_authenticate
from pages.tests.pages_tests.conftest import new_page, page
from pages.tests.users_tests.conftest import user
from users.auth import generate_access_token
from pages.views.page_views import PageViewSet

pytestmark = pytest.mark.django_db
viewset = PageViewSet.as_view(
    {
        'post': "create",
        'get': "retrieve",
        'put': "update",
        'delete': "destroy"
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
        response = viewset(request)

        assert response.status_code == 201
        assert response.data.get('owner') == user.pk

    @mock.patch("Innotter.settings.SECRET_KEY", "1")
    def rest_retrieve_page(self, user: user, page: page, api_factory: APIRequestFactory):
        request = api_factory.get(f"{self.url}{page.pk}/")
        token = generate_access_token(user)
        force_authenticate(request=request, user=user, token=token)
        response = viewset(request, pk=page.pk)

        assert response.status_code == 200
        assert response.data.get("id") == page.pk
