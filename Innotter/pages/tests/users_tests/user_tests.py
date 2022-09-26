import pytest
from django.urls import reverse
from model_bakery import baker
from rest_framework.test import APIRequestFactory, force_authenticate
from users.auth import generate_access_token
from users.models import User

from pages.models import Post
from pages.serializers.user_serializers import UserFavouritePostsSerializer
from pages.tests.users_tests.conftest import new_user, user
from pages.views.user_views import UserViewSet

pytestmark = pytest.mark.django_db
toggle_block_unblock_view = UserViewSet.as_view({"post": "toggle_block"})
list_favourite_posts_view = UserViewSet.as_view({"get": "list_favourites"})


class TestUserLogic:
    def test_toggle_block_unblock(
        self, user: user, new_user: new_user, api_factory: APIRequestFactory
    ):
        user_to_block = new_user
        user_to_block.save()

        token = generate_access_token(user)
        request = api_factory.post(
            reverse("users-toggle-block", args=[user_to_block.pk])
        )
        force_authenticate(request, user=user, token=token)

        response = toggle_block_unblock_view(request, pk=user_to_block.pk)
        assert response.data.get("status") == "user blocked"
        assert User.objects.get(pk=user_to_block.pk).is_blocked is True
        response = toggle_block_unblock_view(request, pk=user_to_block.pk)
        assert response.data.get("status") == "user unblocked"
        assert User.objects.get(pk=user_to_block.pk).is_blocked is False

    def test_list_favourites(self, user: user, api_factory: APIRequestFactory):
        posts = baker.make(Post, _quantity=150)
        for post in posts:
            user.favourite_posts.add(post)
        user.save()
        token = generate_access_token(user)
        request = api_factory.get(reverse("users-list-favourites", args=[user.pk]))
        force_authenticate(request, user=user, token=token)
        response = list_favourite_posts_view(request)

        assert (
            response.status_code == 200
            and len(response.data.get("favourite_posts")) == 150
        )
        assert response.data == UserFavouritePostsSerializer(user).data
