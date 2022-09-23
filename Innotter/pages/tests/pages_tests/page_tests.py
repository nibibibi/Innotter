import datetime

import pytest
from django.urls import reverse
from model_bakery import baker
from rest_framework.test import APIRequestFactory, force_authenticate
from users.auth import generate_access_token
from users.models import User

from pages.models import Page
from pages.serializers.page_serializers import (PageSerializer,
                                                TimeBlockPageSerializer)
from pages.tests.pages_tests.conftest import new_page, page, private_page
from pages.tests.tags_tests.conftest import tag
from pages.tests.users_tests.conftest import user
from pages.views.page_views import PageViewSet

pytestmark = pytest.mark.django_db
default_view = PageViewSet.as_view(
    {"post": "create", "get": "retrieve", "put": "update", "delete": "destroy"}
)
list_view = PageViewSet.as_view({"get": "list"})
toggle_block_view = PageViewSet.as_view({"post": "toggle_permablock"})
toggle_follow_view = PageViewSet.as_view({"post": "toggle_follow"})
toggle_is_private_view = PageViewSet.as_view({"post": "toggle_is_private"})
timeblock_view = PageViewSet.as_view({"put": "timeblock"})
list_requests_view = PageViewSet.as_view({"get": "list_requests"})
accept_follow_request_view = PageViewSet.as_view({"post": "accept"})
reject_follow_request_view = PageViewSet.as_view({"post": "reject"})
reject_all_view = PageViewSet.as_view({"post": "reject_all"})
toggle_tag_view = PageViewSet.as_view({"post": "toggle_tag"})


class TestPageLogic:
    def test_create_page(
        self, user: user, new_page: new_page, api_factory: APIRequestFactory
    ):
        serialized_page = {
            "uuid": new_page.uuid,
            "name": new_page.name,
            "description": new_page.description,
            "is_private": new_page.is_private,
            "owner": user.pk,
        }

        request = api_factory.post(reverse("pages-detail", args=[1]), serialized_page)
        token = generate_access_token(user)
        force_authenticate(request=request, user=user, token=token)

        assert not Page.objects.first()  # No pages exist
        response = default_view(request, serialized_page)
        assert response.status_code == 201
        assert response.data == PageSerializer(Page.objects.first()).data  # New page

    def test_retrieve_page(
        self, user: user, page: page, api_factory: APIRequestFactory
    ):
        request = api_factory.get(reverse("pages-detail", args=[page.pk]))
        token = generate_access_token(user)
        force_authenticate(request=request, user=user, token=token)

        response = default_view(request, pk=page.pk)
        assert response.status_code == 200
        assert response.data == PageSerializer(page).data

    def test_list_pages(self, user: user, api_factory: APIRequestFactory):
        baker.make(Page, _quantity=5)
        request = api_factory.get(reverse("pages-list"))
        token = generate_access_token(user)
        force_authenticate(request=request, user=user, token=token)

        response = list_view(request)
        assert response.status_code == 200
        assert len(response.data) == 5
        for page in response.data:
            assert page == PageSerializer(Page.objects.get(pk=page.get("id"))).data

    def test_page_update(self, user: user, page: page, api_factory: APIRequestFactory):
        request_data = {
            "name": "newName",
            "uuid": "newUUID",
            "description": "newDescription",
        }
        page.owner = user
        page.save()
        request = api_factory.put(reverse("pages-detail", args=[page.pk]), request_data)
        token = generate_access_token(user)
        force_authenticate(request=request, user=user, token=token)

        response = default_view(request, pk=page.pk)
        assert response.status_code == 200
        assert response.data == request_data

    def test_page_destroy(self, page: page, user: user, api_factory: APIRequestFactory):
        page.owner = user
        page.save()
        request = api_factory.delete(reverse("pages-detail", args=[page.pk]))
        token = generate_access_token(user)
        force_authenticate(request=request, user=user, token=token)

        assert Page.objects.filter(pk=page.pk).first()  # Page does exist

        response = default_view(request, pk=page.pk)
        assert not Page.objects.filter(pk=page.pk).first()  # Page does not exist
        assert response.status_code == 204
        assert response.data is None

    def test_toggle_permablock(
        self, page: page, user: user, api_factory: APIRequestFactory
    ):
        assert not Page.objects.get(
            pk=page.pk
        ).is_permamently_blocked  # New page is not blocked

        request = api_factory.post(reverse("pages-toggle-permablock", args=[page.pk]))
        token = generate_access_token(user)
        force_authenticate(request=request, user=user, token=token)

        response = toggle_block_view(request, pk=page.pk)
        assert Page.objects.get(pk=page.pk).is_permamently_blocked  # Page is blocked
        assert response.data.get("status") == "page blocked"

        response = toggle_block_view(request, pk=page.pk)
        assert not Page.objects.get(
            pk=page.pk
        ).is_permamently_blocked  # Page is not blocked
        assert response.data.get("status") == "page unblocked"

    def test_toggle_follow(
        self,
        user: user,
        page: page,
        private_page: private_page,
        api_factory: APIRequestFactory,
    ):
        assert not (user in page.followers.all() or user in page.follow_requests.all())
        assert not (
            user in private_page.followers.all()
            or user in private_page.follow_requests.all()
        )

        token = generate_access_token(user)

        request = api_factory.post(reverse("pages-toggle-follow", args=[page.pk]))
        force_authenticate(request=request, user=user, token=token)

        response = toggle_follow_view(request, pk=page.pk)
        assert user in page.followers.all() and user not in page.follow_requests.all()
        assert (
            response.data.get("status") == "page followed"
            and response.status_code == 200
        )
        response = toggle_follow_view(request, pk=page.pk)
        assert (
            user not in page.followers.all() and user not in page.follow_requests.all()
        )
        assert (
            response.data.get("status") == "page unfollowed"
            and response.status_code == 200
        )

        request = api_factory.post(reverse("pages-toggle-follow", args=[page.pk]))
        force_authenticate(request=request, user=user, token=token)

        response = toggle_follow_view(request, pk=private_page.pk)
        assert (
            user not in private_page.followers.all()
            and user in private_page.follow_requests.all()
        )
        assert (
            response.data.get("status") == "page followed"
            and response.status_code == 200
        )
        response = toggle_follow_view(request, pk=private_page.pk)
        assert (
            user not in private_page.followers.all()
            and user not in private_page.follow_requests.all()
        )
        assert (
            response.data.get("status") == "page unfollowed"
            and response.status_code == 200
        )

    def test_toggle_is_private(
        self, user: user, page: page, api_factory: APIRequestFactory
    ):
        page.owner = user
        page.save()
        assert Page.objects.get(pk=page.pk).is_private is False

        token = generate_access_token(user)
        request = api_factory.post(reverse("pages-toggle-is-private", args=[page.pk]))
        force_authenticate(request=request, user=user, token=token)

        response = toggle_is_private_view(request, pk=page.pk)
        assert response.data.get("status") == "switched to private"
        assert Page.objects.get(pk=page.pk).is_private is True

        response = toggle_is_private_view(request, pk=page.pk)
        assert response.data.get("status") == "switched to public"
        assert Page.objects.get(pk=page.pk).is_private is False

    def test_timeblock(self, user: page, page: page, api_factory: APIRequestFactory):
        assert page.unblock_date is None
        assert page.is_blocked_atm() is False

        put_json = {
            "unblock_date": str(
                datetime.datetime.utcnow() + datetime.timedelta(minutes=1)
            )
            + "+00:00"
        }
        token = generate_access_token(user)
        request = api_factory.put(reverse("pages-timeblock", args=[page.pk]), put_json)
        force_authenticate(request=request, user=user, token=token)

        response = timeblock_view(request, pk=page.pk)
        page = Page.objects.get(pk=page.pk)
        assert response.status_code == 200
        assert str(page.unblock_date) == put_json.get("unblock_date")
        assert page.is_blocked_atm() is True
        assert response.data == TimeBlockPageSerializer(page).data

    def test_list_requests(
        self, user: user, page: page, api_factory: APIRequestFactory
    ):
        page.owner = user
        page.save()
        requests_users = baker.make(User, _quantity=3)
        for request in requests_users:
            page.follow_requests.add(request)
        page.save()

        token = generate_access_token(user)
        request = api_factory.get(reverse("pages-list-requests", args=[page.pk]))
        force_authenticate(request=request, user=user, token=token)

        response = list_requests_view(request, pk=page.pk)
        assert len(response.data.get("follow_requests")) == 3
        for key in response.data.get("follow_requests"):
            assert User.objects.filter(pk=key).first() in page.follow_requests.all()

    def test_accept_follow_request(
        self, user: user, page: page, api_factory: APIRequestFactory
    ):
        page.owner = user
        requesters = baker.make(User, _quantity=2)
        [page.follow_requests.add(requester) for requester in requesters]
        page.save()

        token = generate_access_token(user)
        request = api_factory.post(
            reverse("pages-accept", args=[page.pk]), {"user_id": requesters[0].pk}
        )
        force_authenticate(request=request, user=user, token=token)
        response = accept_follow_request_view(request, pk=page.pk)
        page = Page.objects.get(pk=page.pk)
        assert (
            response.status_code == 200
            and response.data.get("status") == "request accepted"
        )
        assert (
            len(page.followers.all()) == 1
            and len(page.follow_requests.all()) == len(requesters) - 1
        )
        assert page.followers.first() == User.objects.get(pk=requesters[0].pk)

        request = api_factory.post(
            reverse("pages-accept", args=[page.pk]), {"user_id": 421541}
        )
        force_authenticate(request=request, user=user, token=token)
        response = accept_follow_request_view(request, pk=page.pk)
        assert (
            response.status_code == 404
            and response.data.get("status") == "user not found"
        )

    def test_reject_follow_request(
        self, user: user, page: page, api_factory: APIRequestFactory
    ):
        page.owner = user
        requesters = baker.make(User, _quantity=2)
        [page.follow_requests.add(requester) for requester in requesters]
        page.save()

        token = generate_access_token(user)
        request = api_factory.post(
            reverse("pages-reject", args=[page.pk, requesters[0].pk]),
            {"user_id": requesters[0].pk},
        )
        force_authenticate(request=request, user=user, token=token)
        response = reject_follow_request_view(request, pk=page.pk)
        page = Page.objects.get(pk=page.pk)
        assert len(page.followers.all()) == 0 and len(page.follow_requests.all()) == 1
        assert page.follow_requests.first() == requesters[1]
        assert (
            response.status_code == 200
            and response.data.get("status") == "request rejected"
        )

    def test_reject_all(self, user: user, page: page, api_factory: APIRequestFactory):
        page.owner = user
        requesters = baker.make(User, _quantity=150)
        [page.follow_requests.add(requester) for requester in requesters]
        page.save()
        assert len(page.follow_requests.all()) == 150

        token = generate_access_token(user)
        request = api_factory.post(reverse("pages-reject-all", args=[page.pk]))
        force_authenticate(request=request, user=user, token=token)
        response = reject_all_view(request, pk=page.pk)
        page = Page.objects.get(pk=page.pk)
        assert len(page.follow_requests.all()) == 0
        assert (
            response.status_code == 200
            and response.data.get("status") == "requests rejected"
        )

    def test_toggle_tag(
        self, user: user, page: page, tag: tag, api_factory: APIRequestFactory
    ):
        page.owner = user
        page.save()
        assert len(page.tags.all()) == 0

        token = generate_access_token(user)
        request = api_factory.post(
            reverse("pages-toggle-tag", args=[page.pk]), {"tag_name": tag.name}
        )
        force_authenticate(request=request, user=user, token=token)
        response = toggle_tag_view(request, pk=page.pk)
        assert (
            response.data.get("status") == "tag toggled" and response.status_code == 200
        )
        assert Page.objects.get(pk=page.pk).tags.first() == tag
        response = toggle_tag_view(request, pk=page.pk)
        assert len(Page.objects.get(pk=page.pk).tags.all()) == 0
        assert (
            response.data.get("status") == "tag toggled" and response.status_code == 200
        )
